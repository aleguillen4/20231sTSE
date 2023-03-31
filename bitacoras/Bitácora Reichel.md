# Reichel Morales Sánchez - Taller de embebidos

### Lunes 27 de Febrero

Se instala Yocto y se crea la primera imagen minima. 
Para la instalación de Yoctoc se deben usar el siguiente comando:

```
$ sudo apt install gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev pylint3 xterm python3-subunit mesa-common-dev zstd liblz4-tool

```
Se debe clonar el archivo de poky.

```
$ git clone git://git.yoctoproject.org/poky
$ cd poky

```
Tenemos que definir el entorno cada vez que vayamos a construir una  imagen, y eso se realiza con el siguiente comando:
```
$ source oe-init-build-env
```
Debemos ir al conf/local.conf y quirale el comentario a las siguinetes lineas, para acelerar y evitar errores
```
BB_SIGNATURE_HANDLER = "OEEquivHash"
BB_HASHSERVE = "auto"
BB_HASHSERVE_UPSTREAM = "hashserv.yocto.io:8687"
SSTATE_MIRRORS ?= "file://.* https://sstate.yoctoproject.org/all/PATH;downloadfilename=PATH"
```
Se debe tomar en cuenta que el Machine que debe tenerse es el qemux86-64

Una vez modificado el local.conf, se procede a construir la imagen, con el siguiente comando:
```
$  bitbake -k core-image-minimal
```
Para simular la imagen en se utiliza QEMU, este es un emulador, tener en cuenta que para salir de este se usa ctrl-c.
```
$ runqemu qemux86-64
```
Al instalar los paquetes surgieron varios errores:

1.Con el paquete linux-libc-dev, se solucionó con " sudo apt-get update" para actualizar la lista de paquetes disponibles en el repositorio y luego intentar volver a instalar el paquete.

2. También que no estaban instaladas las variables de entorno "PATH".
Estas herramientas son "chrpath", "diffstat", "make", "pzstd" y "zstd" , 
se verificó que estuvieran en el con echo $PATH, 
unas se solucionaron con " sudo apt-get update", 
y make se solucionó con descargando el make desde 
```
wget https://ftp.gnu.org/gnu/make/make-<VERSION>.tar.gz, 

```
se descomprimió con tar -xvzf make-<VERSION>.tar.gz,
y se fue a la dirección con cd make-<VERSION>, 
se instaló con  ./configure  make  sudo make install 
Se verificó la instalación con make --version
La versión es la 3.7

### Domingo 12 de Marzo

Se intentó hacer las pruebas de audio por red que investigó Daniel:
```
gst-launch-1.0 -v autoaudiosrc ! audioconvert ! audioresample \
! audio/x-raw, rate=16000, channels=1, format=S16LE ! audiomixer \
! udpsink host=224.1.1.1 port=5000 `
```
```
gst-launch-1.0 -v udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! rawaudioparse use-sink-caps=false format=pcm pcm-format=s16le sample-rate=16000 num-channels=1 ! queue ! audioconvert ! audioresample ! autoaudiosink
```


### Viernes 17 de marzo 

Se empieza a investigar sobre la estructura de Yocto Project y como funcionan los layers y las recetas, y se encontró la siguiente información.

El proyecto Yocto tiene una estructura de directorios bien definida que es importante conocer para trabajar con él. A continuación, se describe brevemente cada uno de los directorios principales:

build: Este directorio es donde se realiza la construcción de la imagen. Contiene los archivos de configuración de la imagen, así como los archivos generados durante el proceso de construcción.

meta: Este directorio es donde se encuentran las capas de metadatos que definen el comportamiento del sistema. Incluye metadatos para el núcleo de Linux, el sistema de inicio, los paquetes y las configuraciones.

poky: Este directorio contiene el núcleo de Yocto, incluyendo el código fuente y los scripts necesarios para construir la imagen.

downloads: Este directorio es donde se descargan los archivos necesarios para construir la imagen, como el código fuente de los paquetes y las herramientas.

sstate-cache: Este directorio es donde se almacenan las versiones preconstruidas de los paquetes y las herramientas para acelerar el proceso de construcción.

tmp: Este directorio contiene archivos temporales generados durante el proceso de construcción, como los archivos de objeto y los registros.

La estructura de directorios de Yocto es altamente personalizable y puede ser adaptada a las necesidades específicas de cada proyecto. Además de los directorios mencionados anteriormente, se pueden agregar capas adicionales, que contienen metadatos personalizados, y se pueden especificar rutas de búsqueda adicionales para los archivos necesarios para la construcción.

 Fuente: https://docs.yoctoproject.org/current/ref-manual/index.html
 
 

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
