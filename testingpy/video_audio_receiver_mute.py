from time import sleep
from threading import Thread

import gi

gi.require_version("Gst", "1.0")
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, GLib, Gtk


def mute_audio(button):
    pipeline_audio.set_state(Gst.State.PAUSED)

Gst.init()

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

pipeline_video = Gst.parse_launch("udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5001 ! application/x-rtp  ! rtph264depay ! h264parse ! queue ! decodebin ! videoconvert ! autovideosink")
pipeline_audio = Gst.parse_launch("udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! rawaudioparse use-sink-caps=false format=pcm pcm-format=s16le sample-rate=16000 num-channels=1 ! queue ! audioconvert ! audioresample ! autoaudiosink")
pipeline_video.set_state(Gst.State.PLAYING)

pipeline_audio.set_state(Gst.State.PLAYING)

win = Gtk.Window(title="Mute Audio")

button = Gtk.Button.new_with_label("Mute Audio")
button.connect("clicked", mute_audio)

win.add(button)
win.show_all()

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass
pipeline_video.set_state(Gst.State.NULL)
pipeline_audio.set_state(Gst.State.NULL)
main_loop.quit()

Gtk.main()
