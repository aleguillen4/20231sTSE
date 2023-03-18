import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '4.0')
from gi.repository import Gst
from gi.repository import Gtk
from gi.repository import GLib

Gst.init(None)
class MyApp(Gtk.Window, Gtk.Widget):
    def __init__(self):
        Gtk.Window.__init__(self, title="Audio y Video Bidireccional")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(vbox)

        # Creamos los elementos de GStreamer
        self.pipeline = Gst.Pipeline()
        self.src = Gst.ElementFactory.make('v4l2src', 'webcam')
        self.vidconvert = Gst.ElementFactory.make('videoconvert', 'vidconvert')
        self.vidcaps = Gst.ElementFactory.make('capsfilter', 'vidcaps')
        self.vidcaps.set_property('caps', Gst.Caps.from_string('video/x-raw, width=640, height=480'))
        self.videosink = Gst.ElementFactory.make('autovideosink', 'videosink')
        self.sink = Gst.ElementFactory.make('alsasink', 'audiosink')
        self.mute = False

        # Agregamos los elementos al pipeline
        self.pipeline.add(self.src)
        self.pipeline.add(self.vidconvert)
        self.pipeline.add(self.vidcaps)
        self.pipeline.add(self.videosink)
        self.pipeline.add(self.sink)

        # Conectamos los elementos
        self.src.link(self.vidconvert)
        self.vidconvert.link(self.vidcaps)
        self.vidcaps.link(self.videosink)
        self.src.link(self.sink)

        # Creamos un botón para mutear el audio
        self.mute_button = Gtk.Button(label="Mute Audio")
        self.mute_button.connect("clicked", self.on_mute_button_clicked)
        vbox.append(self.mute_button)

        # Iniciamos el pipeline
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_mute_button_clicked(self, widget):
        if not self.mute:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.mute_button.set_label("Unmute Audio")
            self.mute = True
        else:
            self.pipeline.set_state(Gst.State.PLAYING)
            self.mute_button.set_label("Mute Audio")
            self.mute = False

win = MyApp()
win.connect("destroy", GLib.MainLoop.quit)
win.show_all()

# Quit the main loop after 60 seconds
GLib.timeout_add_seconds(60, GLib.MainLoop.quit)

# Start the main loop
GLib.MainLoop().run()
