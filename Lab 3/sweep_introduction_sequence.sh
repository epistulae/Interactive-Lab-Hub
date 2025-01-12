#https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
#!/bin/bash

./sweep_intro.sh

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav recorded_mono.wav
command=$(python3 sweep_responses.py recorded_mono.wav)

if [[ $command == *"clean"* ]]; then
  ./sweep_begin.sh
else
  ./do_nothing.sh
fi

echo $command
