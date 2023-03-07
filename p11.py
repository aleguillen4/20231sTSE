from time import sleep
from threading import Thread

import gi

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib


Gst.init()

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

pipeline = Gst.parse_launch("audiomixer name=mixer ! autoaudiosink  filesrc location=Maxence_Cyrin_-_Where_Is_My_Mind.ogg ! oggdemux !  vorbisdec ! audioconvert ! mixer.sink_%u   filesrc location=David_Bowie_-_Starman.ogg ! oggdemux ! vorbisdec ! audioconvert ! mixer.sink_%u")
pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
