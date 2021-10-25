#!/usr/bin/python3
import time
import board
import busio
import os
import multiprocessing
import subprocess
import re

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Global process variable control.
manager = multiprocessing.Manager()
Process = manager.Namespace()
Process.music_process = 0

def get_pid(pid):
    return str(re.sub("[^0-9]", "", pid))

def play_music(song_name):
    print(f"music thread " + song_name)
    # Process.music_process_id = os.getpid()
    music = subprocess.Popen(["aplay music_files/let-the-living-beware.wav & echo \"$!\""], stdout=subprocess.PIPE, shell=True)
    print("pid " + str(music.pid) + "\n")
    print("music pid " + get_pid(music.stdout.readline()))
    print("stdout already in? " + str(Process.music_process))

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    if mpr121[7].value:
        Process.music_process_id = subprocess.run(["aplay music_files/rex-incognito.wav", "&"], capture_output=True, shell=True)
        print(f"Thread started rex")
        print(Process.music_process_id)
    if mpr121[9].value:
        music = multiprocessing.Process(target=play_music, args=("let-the-living-beware.wav",))
        music.start()
        print(f"Thread started living")
    if mpr121[11].value:
        print(Process.music_process)
        if (Process.music_process is not 0):
            print(f"hello")
            subprocess.run(["kill " + str(Process.music_process)], capture_output=False, shell=True)
        else:
            print(f"there")
    time.sleep(0.5)  # Small delay to keep from spamming output messages.
