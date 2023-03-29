import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst, Gdk



class CustomData:
    def init(self):
        self.playbin = None # Our one and only pipeline
        self.slider = None # Slider widget to keep track of current position
        self.streams_list = None # Text widget to display info about the streams
        self.slider_update_signal_id = 0 # Signal ID for the slider update signal
        self.state = Gst.State.NULL # Current state of the pipeline
        self.duration = Gst.CLOCK_TIME_NONE # Duration of the clip, in nanoseconds
    
    def realize_cb(widget, data):
        window = widget.get_window()
        window_handle = 0
        if not window.ensure_native():
            raise Exception("Couldn't create native window needed for GstVideoOverlay!")
        # Retrieve window handler from GDK
        if Gdk.is_wayland_display():
            raise Exception("Wayland display not yet supported")
        if Gdk.is_x11_display():
            window_handle = window.get_xid()
        elif Gdk.is_win32_display():
            window_handle = window.get_handle()
        elif Gdk.is_quartz_display():
            window_handle = window.get_nsview()
        # Pass it to playbin, which implements VideoOverlay and will forward it to the video sink
        data.playbin.set_window_handle(window_handle)

    def play_cb(button, data):
        data.playbin.set_state(Gst.State.PLAYING)

    def pause_cb(button, data):
        data.playbin.set_state(Gst.State.PAUSED)

    def stop_cb(button, data):
        data.playbin.set_state(Gst.State.READY)

    def delete_event_cb(widget, event, data):
        data.playbin.stop_cb(None, data)
        Gtk.main_quit()

    def draw_cb(widget, cr, data):
        if data.state < Gst.State.PAUSED:
            allocation = widget.get_allocation()
        # Cairo is a 2D graphics library which we use here to clean the video window.
        # It is used by GStreamer for other reasons, so it will always be available to us.
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.fill()
        return False
    def slider_cb(range, data):
        value = range.get_value()
        data.playbin.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,int(value * Gst.SECOND))
        Gst.init(None)
        data = CustomData()
        window = Gtk.Window(title="Video Player")
        window.connect()

def create_ui(data):
    main_window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
    main_window.connect("delete-event", delete_event_cb, data)

    video_window = Gtk.DrawingArea.new()
    video_window.set_double_buffered(False)
    video_window.connect("realize", realize_cb, data)
    video_window.connect("draw", draw_cb, data)

    play_button = Gtk.Button.new_from_icon_name("media-playback-start", Gtk.IconSize.SMALL_TOOLBAR)
    play_button.connect("clicked", play_cb, data)

    pause_button = Gtk.Button.new_from_icon_name("media-playback-pause", Gtk.IconSize.SMALL_TOOLBAR)
    pause_button.connect("clicked", pause_cb, data)

    stop_button = Gtk.Button.new_from_icon_name("media-playback-stop", Gtk.IconSize.SMALL_TOOLBAR)
    stop_button.connect("clicked", stop_cb, data)

    data.slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
    data.slider.set_draw_value(False)
    data.slider_update_signal_id = data.slider.connect("value-changed", slider_cb, data)

    data.streams_list = Gtk.TextView.new()
    data.streams_list.set_editable(False)

    controls = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
    controls.pack_start(play_button, False, False, 2)
    controls.pack_start(pause_button, False, False, 2)
    controls.pack_start(stop_button, False, False, 2)
    controls.pack_start(data.slider, True, True, 2)

    main_hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
    main_hbox.pack_start(video_window, True, True, 0)
    main_hbox.pack_start(data.streams_list, False, False, 2)

    main_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
    main_box.pack_start(main_hbox, True, True, 0)
    main_box.pack_start(controls, False, False, 0)

    main_window.add(main_box)
    main_window.set_default_size(640, 480)
    main_window.show_all()

def refresh_ui(data):
    current = -1

    if data.state < Gst.State.PAUSED:
        return True

    if not GstClockTimeIsValid(data.duration):
        res, data.duration = data.playbin.query_duration(Gst.Format.TIME)
        if not res:
            print("Could not query current duration.")
        else:
            # Set the range of the slider to the clip duration, in SECONDS
            data.slider.set_range(0, float(data.duration) / Gst.SECOND)

    res, current = data.playbin.query_position(Gst.Format.TIME)
    if res:
        # Block the "value-changed" signal, so the slider_cb function is not called
        # (which would trigger a seek the user has not requested)
        data.slider.handler_block(data.slider_update_signal_id)
        # Set the position of the slider to the current pipeline position, in SECONDS
        data.slider.set_value(float(current) / Gst.SECOND)
        # Re-enable the signal
        data.slider.handler_unblock(data.slider_update_signal_id)

    return True

def tags_cb(playbin, stream, data):
    # We are possibly in a GStreamer working thread, so we notify the main
    # thread of this event through a message in the bus
    playbin.post_message(
        Gst.Message.new_application(playbin, Gst.Structure.new_empty("tags-changed"))
    )

# This function is called when an End-Of-Stream message is posted on the bus.
# We just set the pipeline to READY (which stops playback)
def eos_cb(bus, msg, data):
    print("End-Of-Stream reached.")
    data.playbin.set_state(Gst.State.READY)

# This function is called when the pipeline changes states. We use it to
# keep track of the current state.
def state_changed_cb(bus, msg, data):
    old_state, new_state, pending_state = msg.parse_state_changed()
    if msg.src == data.playbin:
        data.state = new_state
        print("State set to", Gst.Element.state_get_name(new_state))
        if old_state == Gst.State.READY and new_state == Gst.State.PAUSED:
            # For extra responsiveness, we refresh the GUI as soon as we reach the PAUSED state
            refresh_ui(data)

# Extract metadata from all the streams and write it to the text widget in the GUI
def analyze_streams(data):
    text = data.streams_list.get_buffer()

    # Clean current contents of the widget
    text.set_text("")

    # Read some properties
    n_video = data.playbin.get_property("n-video")
    n_audio = data.playbin.get_property("n-audio")
    n_text = data.playbin.get_property("n-text")

    for i in range(n_video):
        tags = None
        # Retrieve the stream's video tags
        data.playbin.emit("get-video-tags", i, tags)
        if tags:
            total_str = "video stream %d:\n" % i
            text.insert_at_cursor(total_str)
            gst_tag_list_get_string(tags, Gst.TAG_VIDEO_CODEC, str)
            total_str = "  codec: %s\n" % (str if str else "unknown")
            text.insert_at_cursor(total_str)
            gst_tag_list_free(tags)

    for i in range(n_audio):
        tags = None
        # Retrieve the stream's audio tags
        data.playbin.emit("get-audio-tags", i, tags)
        if tags:
            total_str = "\naudio stream %d:\n" % i
            text.insert_at_cursor(total_str)
            if gst_tag_list_get_string(tags, Gst.TAG_AUDIO_CODEC, str):
                total_str = "  codec: %s\n" % str
                text.insert_at_cursor(total_str)
                g_free(str)
            if gst_tag_list_get_string(tags, Gst.TAG_LANGUAGE_CODE, str):
                total_str = "  language: %s\n" % str
                text.insert_at_cursor(total_str)
                g_free(str)
            if gst_tag_list_get_uint(tags, Gst.TAG_BITRATE, rate):
                total_str = "  bitrate: %d\n" % rate
                text.insert_at_cursor(total_str)
            gst_tag_list_free(tags)

    for i in range(n_text):
        tags = None
        # Retrieve the stream's subtitle tags
        data.playbin.emit("get-text-tags", i, tags)
        if tags:
            total_str = "\nsubtitle stream %d:\n" % i
            text.insert_at_cursor(total_str)
            if gst_tag_list_get_string(tags, Gst.TAG_LANGUAGE_CODE, str):
                total_str = "  language: %s\n" % str
                text.insert_at_cursor(total_str)
                g_free(str)
            gst_tag_list_free(tags)

import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, Gtk, GObject

# CustomData struct definition
class CustomData:
    def __init__(self):
        self.duration = Gst.CLOCK_TIME_NONE
        self.playbin = None
        self.slider = None
        self.streams_list = None
        self.tags_changed = False

# application_cb function
def application_cb(bus, message, data):
    if (message.get_structure().get_name() == "tags-changed"):
        data.tags_changed = True
        GObject.idle_add(analyze_streams, data)

# main function
def main():
    # Initialize GTK
    Gtk.init(None)

    # Initialize GStreamer
    Gst.init(None)

    # Initialize our data structure
    data = CustomData()

    # Create the elements
    data.playbin = Gst.ElementFactory.make("playbin", "playbin")

    if data.playbin is None:
        print("Not all elements could be created.")
        return -1

    # Set the URI to play
    data.playbin.set_property("uri", "https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm")

    # Connect to interesting signals in playbin
    data.playbin.connect("video-tags-changed", tags_cb, data)
    data.playbin.connect("audio-tags-changed", tags_cb, data)
    data.playbin.connect("text-tags-changed", tags_cb, data)

    # Create the GUI
    create_ui(data)

    # Instruct the bus to emit signals for each received message, and connect to the interesting signals
    bus = data.playbin.get_bus()
    bus.add_signal_watch()
    bus.connect("message::error", error_cb, data)
    bus.connect("message::eos", eos_cb, data)
    bus.connect("message::state-changed", state_changed_cb, data)
    bus.connect("message::application", application_cb, data)
    del bus

    # Start playing
    ret = data.playbin.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Unable to set the pipeline to the playing state.")
        data.playbin.set_state(Gst.State.NULL)
        del data.playbin
        return -1

    # Register a function that GLib will call every second
    GObject.timeout_add_seconds(1, refresh_ui, data)

    # Start the GTK main loop. We will not regain control until Gtk.main_quit is called.
    Gtk.main()

    # Free resources
    data.playbin.set_state(Gst.State.NULL)
    del data.playbin
    return 0

if __name__ == "__main__":
    main()
