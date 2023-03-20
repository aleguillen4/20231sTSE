from time import sleep
from threading import Thread

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

Gst.init()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.mute_state = False

        self.video_pipeline = Gst.parse_launch("udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5001 ! application/x-rtp  ! rtph264depay ! h264parse ! queue ! decodebin ! videoconvert ! autovideosink")
        self.audio_pipeline = Gst.parse_launch("udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! rawaudioparse use-sink-caps=false format=pcm pcm-format=s16le sample-rate=16000 num-channels=1 ! queue ! audioconvert ! audioresample ! autoaudiosink")

        self.video_pipeline.set_state(Gst.State.PLAYING)
        self.audio_pipeline.set_state(Gst.State.PLAYING)

        main_widget = QPushButton('Mute/Unmute', self)
        main_widget.setGeometry(10, 10, 100, 50)
        main_widget.clicked.connect(self.toggle_mute)

        self.setCentralWidget(main_widget)

    def toggle_mute(self):
        if self.mute_state:
            self.audio_pipeline.set_property('mute', False)
            self.mute_state = False
        else:
            self.audio_pipeline.set_property('mute', True)
            self.mute_state = True

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()

    main_loop = GLib.MainLoop()
    thread = Thread(target=main_loop.run)
    thread.start()

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass

    window.video_pipeline.set_state(Gst.State.NULL)
    window.audio_pipeline.set_state(Gst.State.NULL)

    main_loop.quit()
