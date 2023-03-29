from time import sleep
from threading import Thread

import gi

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib


Gst.init()

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

pipeline_video = Gst.parse_launch("v4l2src ! videoconvert ! x264enc speed-preset=ultrafast key-int-max=30 tune=zerolatency ! h264parse ! rtph264pay config-interval=-1 ! udpsink host=224.1.1.1 port=5001 auto-multicast=true sync=false")
pipeline_audio = Gst.parse_launch("autoaudiosrc ! audioconvert ! audioresample ! audio/x-raw, rate=16000, channels=1, format=S16LE ! audiomixer ! udpsink host=224.1.1.1 port=5000")
pipeline_video.set_state(Gst.State.PLAYING)

pipeline_audio.set_state(Gst.State.PLAYING)

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass
pipeline_video.set_state(Gst.State.NULL)
pipeline_audio.set_state(Gst.State.NULL)
main_loop.quit()

