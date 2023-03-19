import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, Gtk

# Initialize GStreamer
Gst.init(None)

# Create a GStreamer pipeline
pipeline = Gst.Pipeline()

# Create elements for the pipeline
src = Gst.ElementFactory.make('v4l2src', 'camera-source')
sink = Gst.ElementFactory.make('ximagesink', 'video-output')

# Add elements to the pipeline
pipeline.add(src)
pipeline.add(sink)

# Link elements
src.link(sink)

pipeline = Gst.parse_launch('filesrc location=video.mp4 ! decodebin ! videoconvert ! autovideosink filesrc location=video.mp4 ! decodebin ! audioconvert ! autoaudiosink')
# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Create a GTK window to show the video
window = Gtk.Window()
window.connect('destroy', Gtk.main_quit)
window.set_default_size(640, 480)
window.set_title('Camera Viewer')

# Create a drawing area to show the video
drawing_area = Gtk.DrawingArea()
window.add(drawing_area)

# Show the window and start the GTK main loop
window.show_all()
Gtk.main()