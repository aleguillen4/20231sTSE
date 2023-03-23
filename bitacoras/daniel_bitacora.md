# Bitácora Daniel González - Taller de embebidos

### Domingo 5 de marzo

Se realizan varias pruebas con Gstreamer se logra realizar un sistema de envío de audio por la red, utilizando `gstremaer-launch-1.0` se muestra el pipeline que envía audio y el recibidor:
```
gst-launch-1.0 -v autoaudiosrc ! audioconvert ! audioresample \
! audio/x-raw, rate=16000, channels=1, format=S16LE ! audiomixer \
! udpsink host=224.1.1.1 port=5000 `
```

```
gst-launch-1.0 -v udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! rawaudioparse use-sink-caps=false format=pcm pcm-format=s16le sample-rate=16000 num-channels=1 ! queue ! audioconvert ! audioresample ! autoaudiosink
```


### Jueves 16 de marzo 

Se intenta unificar el enviador de audio con  el enviador de video(proporcionado por RidgeRun) en la red a partir de un código de 1 pipeline en python:

Se muestra el código para el sender, se logra correr en dos terminales separadas en 1 misma computadora.

```
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
```

# Como se puede ver, simplemente se conectó otro pipeline en paralelo que se encarga del envío de audio. 

## Sabado 18 de marzo



Se prueba lo obtenido con pipelines de gstreamer en python en dos computadoras sobre la misma red de la casa de Daniel y se logra enviar el audio y video correctamente.

## Domingo 19 de marzo

#### Imagen inical de yocto con  1 layer

Se empieza a investigar sobre yocto y se realiza un proyecto de yocto con un primer layer.

Se muestra el proyecto de yocto en la carpeta buildgst:

```
(base) daniel@daniel-Latitude-E5450:~/.../buildgst$ tree -L 1
.
├── bitbake-cookerdaemon.log
├── cache
├── conf
├── downloads
├── layergst
├── sstate-cache
└── tmp
 ```
# En la carpeta layergst  se tiene el layer generado, donde se indica la instalación de paquetes para la imagen: 
```
#Add out desired packages 
IMAGE_INSTALL+="psplash dropbear vim git python3 gstreamer1.0-python gstreamer1.0 gstreamer1.0-libav gstreamer1.0-meta-base gstreamer1.0-omx gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-python gstreamer1.0-rtsp-server gstreamer1.0-vaapi "
```
Lo cual se puede ver que incluye paquetes de gstreamer, python, vim, git y otros para ir probando si funciona al utilizar qemu.

Esto en el archivo layersgst/conf/recipes-core/images/layergst-image.bb


```
(base) daniel@daniel-Latitude-E5450:~/.../layergst$ tree -L 3
.
├── conf
│   └── layer.conf
├── COPYING.MIT
├── README
├── recipes-core
│   └── images
│       └── layergst-image.bb
└── recipes-example
    └── example
        └── example_0.1.bb
```

Con esto se logró correr en 1 imagen utilizando el simulador qemu, gst-inspect-1.0  y gst-launch-1.0 sin embargo, no se logra captura audio ni video, tambien se logra correr pyhtom, se tiene problemas para copiar código de al qemu(no se puede). 
También se logra corre un hola mundo en python dentro de la imagen con qemu.


#### Uso de la imagen en virtual box

Se intenta generar un archivo .vmdk del proyecto de yocto, que funciona en virtual box. Para esto se añade al archivo buildgst/conf/local.conf

La línea: `IMAGE_FSTYPES += "wic.vmdk"`

Con esto se  genera en la carpeta: `/buildgst/tmp/deploy/images/qemux86-64`
Un archivo: `layergst-image-qemux86-64-20230320030721.rootfs.wic.vmdk`
El cual puede tener otro nombre según la base de imagen  que se utilice o el layer creado.

Este archivo, se supone funciona en virtual box pero Daniel tiene problemas para correr virtual box por un problema con el kernel, o algún problema de virtualización en la bios. Se pasa a Rachel la tarea de momento.




