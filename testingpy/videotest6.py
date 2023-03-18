import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gst, GObject

GObject.threads_init()
Gst.init(None)

class GstreamerPipeline:
    def __init__(self, video_window):
        self.pipeline = Gst.Pipeline()
        try:
            self.video_source = Gst.ElementFactory.make("v4l2src", None)
            self.video_source.set_property("device", "/dev/video0")

            self.video_filter = Gst.ElementFactory.make("capsfilter", None)
            self.video_caps = Gst.Caps.from_string("video/x-raw,width=640,height=480")
            self.video_filter.set_property("caps", self.video_caps)

            self.video_convert = Gst.ElementFactory.make("videoconvert", None)
            self.video_sink = Gst.ElementFactory.make("gtksink", None)
            self.video_sink.set_property("widget", video_window)

            self.audio_source = Gst.ElementFactory.make("autoaudiosrc", None)
            self.audio_filter = Gst.ElementFactory.make("audioconvert", None)
            self.audio_sink = Gst.ElementFactory.make("autoaudiosink", None)

            self.pipeline.add(self.video_source)
            self.pipeline.add(self.video_filter)
            self.pipeline.add(self.video_convert)
            self.pipeline.add(self.video_sink)
            self.pipeline.add(self.audio_source)
            self.pipeline.add(self.audio_filter)
            self.pipeline.add(self.audio_sink)

            self.video_source.link(self.video_filter)
            self.video_filter.link(self.video_convert)
            self.video_convert.link(self.video_sink)

            self.audio_source.link(self.audio_filter)
            self.audio_filter.link(self.audio_sink)

            self.pipeline.set_state(Gst.State.PLAYING)
    
        except Exception as e:
            print("Error: ", e)

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)
"""
class ApplicationWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.set_title("Python-GStreamer Video Test")
        self.set_default_size(800, 600)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.get_content_area().add(vbox)
        #self.add(vbox)

        video_window = Gtk.DrawingArea()
        video_window.set_size_request(640, 480)
        vbox.pack_start(video_window, True, True, 0)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(button_box, False, False, 0)

        mute_button = Gtk.Button(label="Mute Audio")
        mute_button.connect("clicked", self.on_mute_button_clicked)
        button_box.pack_start(mute_button, False, False, 0)

        self.pipeline = GstreamerPipeline(video_window.get_window())

        self.connect("destroy", self.on_destroy)

    def on_destroy(self, widget):
        self.pipeline.stop()
        Gtk.main_quit()

    def on_mute_button_clicked(self, widget):
        pass
"""

class ApplicationWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.set_title("Python-GStreamer Video Test")
        self.set_default_size(800, 600)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self.add(vbox)

        video_window = Gtk.DrawingArea()
        video_window.set_size_request(640, 480)
        vbox.pack_start(video_window, True, True, 0)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(button_box, False, False, 0)

        mute_button = Gtk.Button(label="Mute Audio")
        mute_button.connect("clicked", self.on_mute_button_clicked)
        button_box.pack_start(mute_button, False, False, 0)

        self.pipeline = GstreamerPipeline(video_window.get_window())

        self.connect("destroy", self.on_destroy)

    def on_destroy(self, widget):
        self.pipeline.stop()
        Gtk.main_quit()

    def on_mute_button_clicked(self, widget):
        pass

win = ApplicationWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
