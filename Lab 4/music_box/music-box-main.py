#!/usr/bin/python3
import time
import board
import busio
import os
import multiprocessing
import subprocess

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Global process variable control.
manager = multiprocessing.Manager()
processes = manager.Namespace()
processes.music_process_id = 0

def play_music(song_name):
    print(f"music thread " + song_name)
    processes.music_process_id = os.getpid()
    print(processes.music_process_id)
    processes.music_process_id = subprocess.run(["aplay music_files/" + song_name + " &"], capture_output=True, shell=True)
    print(processes.music_process_id)

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    if mpr121[7].value:
        Global.music_process_id = subprocess.run(["aplay music_files/rex-incognito.wav &"], capture_output=True, shell=True)
        print(f"Thread started rex")
    if mpr121[9].value:
        music = multiprocessing.Process(target=play_music, args=("let-the-living-beware.wav",))
        music.start()
        print(f"Thread started living")
    if mpr121[11].value:
        print(processes.music_process_id)
        if (processes.music_process_id is not 0):
            print(f"hello")
        else:
            print(f"there")
    time.sleep(0.5)  # Small delay to keep from spamming output messages.
