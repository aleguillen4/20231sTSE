gst-launch-1.0 audiomixer name=mixer ! autoaudiosink  filesrc location=Maxence_Cyrin_-_Where_Is_My_Mind.ogg ! oggdemux !  vorbisdec ! audioconvert ! mixer.sink_%u   filesrc location=David_Bowie_-_Starman.ogg ! oggdemux ! vorbisdec ! audioconvert ! mixer.sink_%u 



#gst-launch-1.0 filesrc location=Unlike_Pluto_-_EverythingBlack.ogg ! oggdemux ! vorbisdec ! autoaudiosink


#gst-launch-1.0 textoverlay name=overlay ! videoconvert ! videoscale ! autovideosink

#filesrc location=movie.avi ! decodebin2 !  videoconvert ! overlay.video_sink

#filesrc location=movie.srt ! subparse ! overlay.text_sink
