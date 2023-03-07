gst-launch-1.0 -v autoaudiosrc ! audioconvert ! audioresample ! audio/x-raw, rate=16000, channels=1, format=S16LE ! audiomixer ! udpsink host=224.1.1.1 port=5000

