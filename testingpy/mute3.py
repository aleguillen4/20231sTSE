from time import sleep
from threading import Thread

import gi

gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Gst, GLib, Gtk


class VideoWindow(Gtk.Window):
    def _init_(self):
        super()._init_(title="Video Window")
        self.set_default_size(800, 600)

        self.button = Gtk.Button(label="Mute")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        if self.button.get_label() == "Mute":
            pipeline_audio.set_state(Gst.State.PAUSED)
            self.button.set_label("Unmute")
        else:
            pipeline_audio.set_state(Gst.State.PLAYING)
            self.button.set_label("Mute")


Gst.init()

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

pipeline_video = Gst.parse_launch(
    "udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5001 ! application/x-rtp  ! rtph264depay ! h264parse ! queue ! decodebin ! videoconvert ! autovideosink"
)
pipeline_audio = Gst.parse_launch(
    "udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! rawaudioparse use-sink-caps=false format=pcm pcm-format=s16le sample-rate=16000 num-channels=1 ! queue ! audioconvert ! audioresample ! autoaudiosink"
)
pipeline_video.set_state(Gst.State.PLAYING)

pipeline_audio.set_state(Gst.State.PLAYING)

window = VideoWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass
pipeline_video.set_state(Gst.State.NULL)
pipeline_audio.set_state(Gst.State.NULL)
main_loop.quit()