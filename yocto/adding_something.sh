#Añadir un paquete o aplicacion a la imagen no estoy seguro
#Editar el archivo local.conf en 
yocto/poky/build/conf

#añadir algo con
IMAGE_INSTALL+ = "libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio vim grep sudo apt"

#copié todo lo de gstreamer y vim, grep, sudo y apt, luego bitbake y qemu, pero estando dentro del bicho no servía vim, entonces ni idea de si se esta instalando apps o como funciona esa madre



#Algo para que funciona la vara luego en virtual box
#Esto es para hacer que el bicho haga en:
/poky/build/tmp/deploy/images.
#un archivo .vmdk que se supone se puede utilizar en virtual box pero aún no lo logro. creditos a Javier
#para que lo haga hay que añadir al local.conf también:
IMAGE_FSTYPES += "wic.vmdk"

