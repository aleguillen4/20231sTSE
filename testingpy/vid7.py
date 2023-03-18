import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import tkinter as tk
from threading import Thread

Gst.init(None)

class VideoPlayer():
    def __init__(self):
        self.pipeline = None
        self.playing = False

    def start_pipeline(self):
        self.pipeline = Gst.Pipeline.new("mypipeline")

        # Create elements
        self.videosrc = Gst.ElementFactory.make("v4l2src", "videosrc")
        self.videoconvert1 = Gst.ElementFactory.make("videoconvert", "videoconvert1")
        self.videoscale = Gst.ElementFactory.make("videoscale", "videoscale")
        self.videoconvert2 = Gst.ElementFactory.make("videoconvert", "videoconvert2")
        self.x264enc = Gst.ElementFactory.make("x264enc", "x264enc")
        self.rtph264pay = Gst.ElementFactory.make("rtph264pay", "rtph264pay")
        self.udpsink = Gst.ElementFactory.make("udpsink", "udpsink")

        # Add elements to pipeline
        self.pipeline.add(self.videosrc)
        self.pipeline.add(self.videoconvert1)
        self.pipeline.add(self.videoscale)
        self.pipeline.add(self.videoconvert2)
        self.pipeline.add(self.x264enc)
        self.pipeline.add(self.rtph264pay)
        self.pipeline.add(self.udpsink)

        # Set properties
        self.videosrc.set_property("device", "/dev/video0")
        self.videoscale.set_property("method", 0)
        self.udpsink.set_property("host", "127.0.0.1")
        self.udpsink.set_property("port", 5000)

        # Link elements
        self.videosrc.link(self.videoconvert1)
        self.videoconvert1.link(self.videoscale)
        self.videoscale.link(self.videoconvert2)
        self.videoconvert2.link(self.x264enc)
        self.x264enc.link(self.rtph264pay)
        self.rtph264pay.link(self.udpsink)

        self.pipeline.set_state(Gst.State.PLAYING)
        self.playing = True

    def stop_pipeline(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.playing = False


    def toggle_mute(self):
        bin = self.pipeline.get_by_name("mypipeline")
        bin.set_property("mute", not bin.get_property("mute"))

class MainWindow():
    def __init__(self):
        self.window = tk.Tk()
        self.videoplayer = VideoPlayer()
        self.mute_button = tk.Button(self.window, text="Mute", command=self.videoplayer.toggle_mute)

        self.mute_button.pack()

    def run(self):
        self.videoplayer.start_pipeline()
        self.window.mainloop()

        self.videoplayer.stop_pipeline()

if __name__ == "__main__":
    mainwindow = MainWindow()
    mainwindow.run()
