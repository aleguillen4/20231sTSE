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
 
Existen varios conjuntos de herramientas para Yoctoc Proyect que dependen de las necesidades y requisitos del proyecto según ChatGPT, y hay unos especificos para audio.

GCC: GNU Compiler Collection es un conjunto de compiladores y herramientas de programación que es compatible con una amplia variedad de plataformas y arquitecturas.

Clang/LLVM: Clang es un compilador de C/C++ que utiliza la infraestructura LLVM para compilar código fuente. LLVM también proporciona herramientas adicionales como el analizador estático de código y el optimizador de código.

Intel C++ Compiler: El compilador C++ de Intel es un conjunto de herramientas de desarrollo que proporciona un conjunto completo de características de optimización y es compatible con plataformas Intel x86.

OpenEmbedded Build System: OpenEmbedded es un sistema de compilación automatizado que se utiliza junto con Yocto Project. Incluye una variedad de herramientas de compilación y scripts de automatización que permiten compilar y crear imágenes de sistema operativo personalizadas.

Buildroot: Buildroot es un sistema de compilación basado en make que se utiliza para crear sistemas operativos embebidos pequeños y ligeros.

CMake: CMake es una herramienta de construcción de código abierto que se utiliza para controlar el proceso de compilación de aplicaciones.

En general, Yocto Project es una herramienta de construcción muy flexible que permite a los desarrolladores elegir y personalizar el conjunto de herramientas que se utilizarán en sus proyectos, según sus necesidades y requisitos específicos.
 
Los paquetes de herramientas que son para audio y video son:

GStreamer: GStreamer es un marco de trabajo de procesamiento multimedia que permite la creación de flujos de trabajo para el procesamiento de audio y video. GStreamer está disponible como un conjunto de herramientas en Yocto Project y se puede utilizar para crear aplicaciones de multimedia personalizadas.

FFmpeg: FFmpeg es una biblioteca de software libre que se utiliza para grabar, convertir y transmitir audio y video en varios formatos. FFmpeg se puede integrar fácilmente en aplicaciones multimedia en Yocto Project.

ALSA: Advanced Linux Sound Architecture (ALSA) es una biblioteca de software libre que proporciona soporte para audio en Linux. ALSA proporciona controladores de dispositivos de audio para una amplia variedad de hardware de audio y se puede utilizar para crear aplicaciones de audio en Yocto Project.

Jack Audio Connection Kit: Jack Audio Connection Kit es un sistema de audio profesional para Linux que permite la conexión de aplicaciones de audio y la manipulación en tiempo real de flujos de audio.

OpenCV: OpenCV (Open Source Computer Vision Library) es una biblioteca de visión por computadora y procesamiento de imágenes que se puede utilizar para aplicaciones de procesamiento de video y visión artificial.

Estos son solo algunos ejemplos de los conjuntos de herramientas disponibles en Yocto Project para el desarrollo de aplicaciones de audio y video. Cada conjunto de herramientas tiene sus propias características y ventajas, y la elección dependerá de las necesidades específicas del proyecto.
 

## Sabado 18 de marzo
 
 ChatGPT, me hizo un mini resumen de como era una receta :
 
En el contexto de Yocto Project, una receta de construcción (build recipe) es un archivo de metadatos que define cómo se debe construir y empacar un componente de software. Las recetas de construcción se utilizan para especificar las dependencias de software, la configuración de compilación, la instalación de archivos y la creación de paquetes para el componente de software.

Las recetas de construcción se escriben en un lenguaje llamado BitBake, que es el sistema de compilación utilizado por Yocto Project. Una receta de construcción típica consta de varias secciones que especifican diferentes aspectos de la construcción del componente de software. Algunas de las secciones comunes incluyen:

Descripción: Información general sobre el componente de software.
Fuentes: Dónde se pueden encontrar las fuentes del software.
Dependencias: Lista de dependencias necesarias para construir el software.
Configuración de compilación: Opciones de configuración para el proceso de compilación.
Instalación: Cómo se deben instalar los archivos del software.
Paquetización: Cómo se deben crear los paquetes para el software.
Aquí hay un ejemplo de una receta de construcción para el paquete de software "hello-world":


```
SUMMARY = "Hello World Example"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=0636e73ff0215e8d672dc4c32c317bb3"

SRC_URI = "http://example.com/hello-world-1.0.tar.gz"
SRC_URI[md5sum] = "0123456789abcdef0123456789abcdef"

DEPENDS = "virtual/libc"

S = "${WORKDIR}/hello-world-1.0"

do_configure() {
    ./configure --prefix=${prefix}
}

do_compile() {
    make
}

do_install() {
    install -d ${D}${prefix}/bin
    install -m 0755 hello-world ${D}${prefix}/bin
}

PACKAGES = "${PN}"
FILES_${PN} = "${prefix}/bin/hello-world"
 
```
Esta receta define a "Hello-world" , la fuente de esta receta es la siguiente : http://example.com/hello-world-1.0.tar.gz
 
- La receta también especifica que el paquete depende de la biblioteca C virtual, "virtual/libc". 
- La sección "do_configure" especifica la configuración de compilación.
- La sección "do_compile" especifica cómo compilar el código fuente.
- La sección "do_install" especifica cómo instalar los archivos del software en el sistema de archivos de destino.
- La sección "PACKAGES" especifica que el paquete debe incluirse en la imagen final.
- La sección "FILES_${PN}" especifica qué archivos deben incluirse en el paquete.
 
Aun no entiendo muy bien que son las dependencias de una receta.

## Miercoles 22 de Marzo
 
Se investiga sobre las dependencias: 
 
En Yocto Project, las dependencias se refieren a otros componentes de software que son necesarios para construir un componente de software específico. Las dependencias pueden ser bibliotecas compartidas, herramientas de compilación, paquetes de software y otros componentes necesarios para la construcción y ejecución del componente de software.

Las dependencias se especifican en las recetas de construcción de Yocto Project mediante la variable "DEPENDS". Esta variable se utiliza para especificar una lista de componentes de software necesarios para construir el componente de software actual. Si una de las dependencias no está presente, el sistema de construcción de Yocto Project intentará construirla antes de continuar con el componente de software actual.

Se empieza a investigar sobre como poder usar python con Yoctoc, chatGPT ofrece la siguiente información:
 
Yocto Project ofrece varias herramientas para trabajar con Python. Algunas de estas herramientas incluyen:

- python3: Yocto Project incluye soporte para Python 3, lo que permite a los desarrolladores escribir recetas de construcción utilizando Python 3. También se incluye una amplia gama de módulos de Python estándar y paquetes adicionales.

- pip: Pip es un administrador de paquetes de Python que se utiliza para instalar y administrar paquetes adicionales de Python. Pip está disponible en Yocto Project y se puede utilizar para instalar paquetes de Python adicionales en el sistema de destino.

- setuptools: Setuptools es una biblioteca de Python que se utiliza para desarrollar y distribuir paquetes de Python. Yocto Project incluye setuptools y se puede utilizar para construir y distribuir paquetes de Python personalizados.

- virtualenv: Virtualenv es una herramienta que se utiliza para crear entornos virtuales de Python aislados. Esto permite a los desarrolladores instalar y trabajar con diferentes versiones de Python y diferentes paquetes de Python en el mismo sistema sin interferir con otros paquetes o versiones de Python. Yocto Project incluye virtualenv y se puede utilizar para crear entornos virtuales de Python aislados en el sistema de destino.

- pyro: Pyro es un marco de trabajo de Python que se utiliza para desarrollar aplicaciones distribuidas y sistemas de middleware. Yocto Project incluye pyro y se puede utilizar para desarrollar aplicaciones distribuidas y sistemas de middleware en el sistema de destino.

Estas son solo algunas de las herramientas de Python disponibles en Yocto Project. Con estas herramientas, los desarrolladores pueden trabajar con Python y construir aplicaciones de Python personalizadas para el sistema de destino.
 
 Fuente: https://docs.yoctoproject.org/current/ref-manual/index.html

#### Se crea una Imagen inical de yocto con  1 layer

Para crear un layer primero debemos ejecutar el comando:
 
```
bitbake-layers create-layer meta-newlayer

```
Ahora esta layer va tener archivos dentro entre esos recipes-example/examples, cuando llegamos ahí solo vamos a tener un .bb qu es donde vamos a mandar a buscar los paquetes que necesitamos

```
├── conf
│   └── layer.conf
├── COPYING.MIT
├── README
├── recipes-example
    └── example
       └── example_0.1.bb
```

 ## Miercoles 25 de Marzo
 
 Se investiga como se pueden tener los archivos de python de la aplicación , en yocto y se puedan correr.

 Primero se crea un archivo llamado files, por medio del comando :
 
```
mkdir files
```
```
├── conf
│   └── layer.conf
├── COPYING.MIT
├── README
├── recipes-example
    └── example
       └── example_0.1.bb
```

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
