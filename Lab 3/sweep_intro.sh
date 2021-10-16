#https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)

#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }

aplay jingle.wav
say "Hello! I am Sweep, your new cleaning companion. I can help you keep your home super clean all the time!"
say "On my first cleaning through your home, I will map out the floor plan so you can assign room names and tell me to clean specific rooms."
say "I can also schedule cleaning routines to make spotless floors a breeze."
say "To get started, just say: Sweep, clean my house."
