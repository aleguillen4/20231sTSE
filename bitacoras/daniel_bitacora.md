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

# Domingo 26 y Lunes 27 de marzo

Empieza el juego

Descargar a la par de la carpeta poky los siguientes repos: 

```
git clone -b langdale https://github.com/openembedded/meta-openembedded.git
git clone -b langdale https://github.com/openembedded/openembedded-core.git
```

Incluir los layers que se acaban de descargar en el `conf/bblayers.conf`

```
# POKY_BBLAYERS_CONF_VERSION is increased each time build/conf/bblayers.conf
# changes incompatibly
POKY_BBLAYERS_CONF_VERSION = "2"

BBPATH = "${TOPDIR}"
BBFILES ?= ""

BBLAYERS ?= " \
  /home/daniel/yocto/poky/meta-poky \
  /home/daniel/yocto/poky/meta-yocto-bsp \
  /home/daniel/yocto/openembedded-core/meta\ 
  /home/daniel/yocto/meta-openembedded/meta-multimedia \
  /home/daniel/yocto/meta-openembedded/meta-perl \
  /home/daniel/yocto/meta-openembedded/meta-python \
  /home/daniel/yocto/meta-openembedded/meta-xfce \
  /home/daniel/yocto/meta-openembedded/meta-initramfs \
  /home/daniel/yocto/meta-openembedded/meta-networking \
  /home/daniel/yocto/meta-openembedded/meta-oe \
  /home/daniel/yocto/meta-openembedded/meta-gnome \
  /home/daniel/yocto/meta-openembedded/meta-filesystems \
"
```


Note que se elimino poky/meta pues da errores de cosas repetidas con meta openembedded-core/meta creo.

Según chatGPT las cosas que están en estos layers no se instalan en la imagen, hay que poner los paquetes también en el local.conf. Lo cual se hizo y se logró obtener las funcionalidades deseadas en la imagen.

Lo que se añadió al `local.conf`

```
IMAGE_FSTYPES += "wic.vmdk"
IMAGE_INSTALL+="python3-pygobject netplan inetutils tree apt  psplash dropbear vim git python3 gstreamer1.0-python gstreamer1.0 gstreamer1.0-libav gstreamer1.0-meta-base gstreamer1.0-omx gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-python gstreamer1.0-rtsp-server gstreamer1.0-vaapi"

MACHINE_FEATURES +=" ethernet"

LICENSE_FLAGS_ACCEPTED="commercial"

IMAGE_INSTALL +="iproute2"

```


Note que se incluye la línea para los archivos .vmdk, no sé si añadirla dos veces sea problema, pero si ya la puso no creo que sea necesario.

Actualmente corriento el bitbake con los cambios recientes en el local.conf que se acaban de explicar y con la esperanza de que funciona el pipeline de video streaming por la red en el x11, el cual no funcionó en sato.

### Correr el bitbake de x11

`bitbake core-image-x11`

### Asuntos de red

Tras mucha investigación e intentos se logró correr un pipeline sencillo recibidor de video en la image x11. Se muestran los pasos para lograr esto en virtual box y la imagen. Este proceso no es en yocto, aunque se añadieron algunas cosas al local.conf de networking y/o redes que no sabemos realmente si hayan servido o no, pero las dejamos ahí por si acaso.

Paso 1: Ajustar la configuración adecuada en el virtual box para que nuestra máquina virtual pueda ser vista con una ip propia en la red.

Ir a configuración(settings) -> redes(network) -> hacer el adaptador 1 bridge adapter
No parece ser necesario, pero puede añadir en advanced -> cambiar deny por allow all

Paso 2: Una vez encendida la vm en virtual box, correr los siguientes comandos:

# OJO, al parecer estas dos líneas debe ponerlas en 1 script(red.sh) bash y correr el script con `bash red.sh`

Si corre línea por línea no funciona como se espera.

```
ifconfig eth0 up
udhcpc -i eth0
```

Luego de esto debería aparecer una ip que puede utilizar para hacer `ping` la vm desde su host si desea comprobar que se puede enviar información del host a la vm.

### Miercoles y Jueves 29 y 31 de marzo

Se realiza investigación mínima sobre audio, para intentar reproducir el pipeline básico de prueba de gstreamer dentro de virtual box, pues el mismo corre pero no se logra escuchar nada, se muestra el pipeline:

`gst-launch-1.0 audiotestsrc ! audioconvert ! autoaudiosink`

Se realiza investigación tratando de apoyar a Rachel pues Daniel se quedo sin computadora...
Se realiza investigación sobre otros errores obtenidos con la imagen y los programas implementados.
Se trabaja añadiendo a nuestro documento guía en un overleaf,  explicaciones sobre yocto y pipelines de gstreamer entre otras explicaciones sobre el trabajo desarrollado.


