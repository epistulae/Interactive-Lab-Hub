#https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
#!/bin/bash

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav recorded_mono.wav
command=$(python3 sweep_responses.py recorded_mono.wav)

if [[ $command == *"clean"* ]]; then
  ./battery_low.sh
else
  ./do_nothing.sh
  exit 0
fi

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav recorded_mono.wav
command=$(python3 sweep_responses.py recorded_mono.wav)

if [[ $command == *"yes"* ]]; then
  ./battery_schedule.sh
else
  ./do_nothing.sh
fi
