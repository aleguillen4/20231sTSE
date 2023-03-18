import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk



gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkX11, Gdk
import sys


GObject.threads_init()
Gst.init(None)

class GstreamerPipeline:
    def __init__(self):
        self.pipeline = Gst.Pipeline()
        self.video_src = Gst.ElementFactory.make('v4l2src', None)
        self.video_conv = Gst.ElementFactory.make('videoconvert', None)
        self.video_enc = Gst.ElementFactory.make('x264enc', None)
        self.video_pay = Gst.ElementFactory.make('rtph264pay', None)
        self.audio_src = Gst.ElementFactory.make('alsasrc', None)
        self.audio_conv = Gst.ElementFactory.make('audioconvert', None)
        self.audio_enc = Gst.ElementFactory.make('opusenc', None)
        self.audio_pay = Gst.ElementFactory.make('rtpopuspay', None)
        self.video_sink = Gst.ElementFactory.make('udpsink', None)
        self.audio_sink = Gst.ElementFactory.make('udpsink', None)

        self.video_src.set_property('device', '/dev/video0')
        self.video_sink.set_property('host', '127.0.0.1')
        self.video_sink.set_property('port', 5000)
        self.audio_src.set_property('device', 'hw:0')
        self.audio_sink.set_property('host', '127.0.0.1')
        self.audio_sink.set_property('port', 5001)

        self.pipeline.add(self.video_src)
        self.pipeline.add(self.video_conv)
        self.pipeline.add(self.video_enc)
        self.pipeline.add(self.video_pay)
        self.pipeline.add(self.audio_src)
        self.pipeline.add(self.audio_conv)
        self.pipeline.add(self.audio_enc)
        self.pipeline.add(self.audio_pay)
        self.pipeline.add(self.video_sink)
        self.pipeline.add(self.audio_sink)

        self.video_src.link(self.video_conv)
        self.video_conv.link(self.video_enc)
        self.video_enc.link(self.video_pay)
        self.audio_src.link(self.audio_conv)
        self.audio_conv.link(self.audio_enc)
        self.audio_enc.link(self.audio_pay)
        self.video_pay.link(self.video_sink)
        self.audio_pay.link(self.audio_sink)

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)
"""
class ApplicationWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Audio/Video Chat")

        self.set_default_size(600, 400)
        self.set_position(Gtk.WindowPosition.CENTER)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        video_window = Gtk.DrawingArea()
        video_window.set_size_request(400, 300)
        vbox.pack_start(video_window, True, True, 0)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox.pack_start(button_box, False, False, 0)

        mute_button = Gtk.Button(label="Mute Audio")
        mute_button.connect("clicked", self.on_mute_button_clicked)
        button_box.pack_start(mute_button, False, False, 0)

        self.pipeline = GstreamerPipeline()
        bus = self.pipeline.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self.on_eos)
        bus.connect("message::error", self.on_error)
    def on_mute_button_clicked(self, button):
        audio_sink = self.pipeline.audio_sink
        is_muted = audio_sink.get_property("mute")
        audio_sink.set_property("mute", not is_muted)
        button_label = "Mute Audio" if is_muted else "Unmute Audio"
        button.set_label(button_label)

    def on_eos(self, bus, message):
        print("End of stream")
        self.pipeline.stop()
        Gtk.main_quit()

    def on_error(self, bus, message):
        error, debug_info = message.parse_error()
        print(f"Error: {error.message}, Debug info: {debug_info}")
        self.pipeline.stop()
        Gtk.main_quit()
"""
class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Python-GStreamer Video Test")

        self.set_default_size(800, 600)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
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

    def on_mute_button_clicked(self, button):
        audio_sink = self.pipeline.audio_sink
        is_muted = audio_sink.get_property("mute")
        audio_sink.set_property("mute", not is_muted)
        button_label = "Mute Audio" if is_muted else "Unmute Audio"
        button.set_label(button_label)


if __name__ == "__main__":
    win = ApplicationWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()

    win.pipeline.start()

    Gtk.main()




"""
class ApplicationWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Python-GStreamer Video Test")

        self.set_default_size(800, 600)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
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

    def on_mute_button_clicked(self, button):
        audio_sink = self.pipeline.audio_sink
        is_muted = audio_sink.get_property("mute")
        audio_sink.set_property("mute", not is_muted)
        button_label = "Mute Audio" if is_muted else "Unmute Audio"
        button.set_label(button_label)
"""