# Bitácora Alejandro Guillen Vargas - Taller de embebidos

### 6 de Marzo

Se crea el repositorio en GitHub para el control de versiones del proyecto

## 15 de Marzo
Primeros esfuerzos para la integración del pipeline desarrollado por Daniel a una interfaz gráfica. 

```
   def __init__(self):
        Gtk.Window.__init__(self, title="Audio y Video Bidireccional")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Creamos los elementos de GStreamer
        self.pipeline = Gst.Pipeline()

        ....

win = MyApp()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
```

## 17 de Marzo
Se sigue trabajando en la implementación de una interfaz gráfica, tipo zoom, para mostrar el video y los botones en una sola ventana. Se prueban diferentes métodos utilizando gtk, tkinter o PyQt5. Se itera sobre diferentes scripts dentro de testingpy, como videotest.py, videotest2.py, videotest3.py, vid4.py.... Sin embargo no se llega a una interfaz convincente, el video y los botones salen en lugares separados. 


## 19 de Marzo
Se descarta la idea de una interfaz gráfica luego de muchos intentos, y problemas a la hora de integrar bibliotecas a la imagen mínima. Se decide que para efectos del proyecto poder manejar el muteo del audio y la función de quit como botones aparte de la ventana de video, cumplen con la función. mute5.py queda como opción viable. 

```
import gi

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
            "udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5001 ! application/x-rtp ! rtph264depay ! h264parse ! queue ! decodebin ! videoconvert ! autovideosink"
           )
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
```

## 24 de Marzo
Se vuelve a intentar una interfaz gráfica basada en el código que existe en gstreamer https://gstreamer.freedesktop.org/documentation/tutorials/basic/toolkit-integration.html
Este código se encuentra en C, la idea inicial es traspasar el código a python con la finalidad de ser modificado para obtener una interfaz gráfica donde se integre el video y diferentes botones. 
Los avances se pueden observar en el python testingpy/basic-tutorial5.py
A pesar de avanzar en la transcripción del código, se opta por priorizar la integración del script a Yocto. 

## 29 de Marzo
Se deciden los códigos "finales" para la implementación en la imgen mínima.
script2/video_audio_sender.py
script2/mute5.py

Luego de esto se desarrolla un nuevo pipeline en el que se utilizan plug ins de OpenCV para detectar movimiento. 

```
           "udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5001 ! application/x-rtp ! rtph264depay ! h264parse ! queue ! decodebin ! videoconvert ! cvtracker object-initial-x=175 object-initial-y=40 object-initial-width=300 object-initial-height=150 algorithm=1 ! videoconvert ! xvimagesink"
```