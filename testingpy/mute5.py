import gi
import cv2
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Gst, Gtk, GObject


Gst.init(None)


class ZoomGUI:
    def __init__(self):
        self.window = Gtk.Window(title="Zoom Clone")
        self.window.connect("destroy", self.quit)
        self.video_box = Gtk.Box()
        self.audio_box = Gtk.Box()
        self.mute_button = Gtk.Button(label="Mute")
        self.mute_button.connect("clicked", self.toggle_mute)
        self.quit_button = Gtk.Button(label="Quit")
        self.quit_button.connect("clicked", self.quit)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.main_box.pack_start(self.video_box, True, True, 0)
        self.main_box.pack_start(self.audio_box, True, True, 0)
        self.main_box.pack_start(self.mute_button, False, False, 0)
        self.main_box.pack_start(self.quit_button, False, False, 0)
        self.window.add(self.main_box)
        self.window.show_all()
        self.pipeline_video = Gst.parse_launch(
            "udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5001 ! application/x-rtp ! rtph264depay ! h264parse ! queue ! decodebin ! videoconvert ! cvtracker object-initial-x=175 object-initial-y=40 object-initial-width=300 object-initial-height=150 algorithm=1 ! videoconvert ! xvimagesink"
           )
        """
        self.pipeline_video = Gst.parse_launch(
            "udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5001 ! application/x-rtp ! rtph264depay ! h264parse ! queue ! decodebin ! videoconvert ! cvtracker box-x=50 box-y=50 box-wdith=50 box-height=50 ! videoconvert ! xvimagesink"
        )

        """
        self.pipeline_audio = Gst.parse_launch(
            "udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! rawaudioparse use-sink-caps=false format=pcm pcm-format=s16le sample-rate=16000 num-channels=1 ! queue ! audioconvert ! audioresample ! autoaudiosink"
           )
        bus = self.pipeline_video.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self.quit)
        bus.connect("message::error", self.on_error)
        self.pipeline_video.set_state(Gst.State.PLAYING)
        self.pipeline_audio.set_state(Gst.State.PLAYING)
        
    def toggle_mute(self, button):
        self.pipeline_audio.set_state(Gst.State.PAUSED)
        self.mute_button.set_label("Unmute")
        self.mute_button.disconnect_by_func(self.toggle_mute)
        self.mute_button.connect("clicked", self.toggle_unmute)
        
    def toggle_unmute(self, button):
        self.pipeline_audio.set_state(Gst.State.NULL)  # reset the state
        self.pipeline_audio.set_state(Gst.State.PLAYING)
        self.mute_button.set_label("Mute")
        self.mute_button.disconnect_by_func(self.toggle_unmute)
        self.mute_button.connect("clicked", self.toggle_mute)
        
    def quit(self, *args):
        self.pipeline_video.set_state(Gst.State.NULL)
        self.pipeline_audio.set_state(Gst.State.NULL)
        Gtk.main_quit()
    
    def on_error(self, bus, message):
        error = message.parse_error()[1]
        print(f"Error: {error.message}")
        self.quit()

if __name__ == "__main__":
    gui = ZoomGUI()
    GObject.threads_init()
    Gtk.main()