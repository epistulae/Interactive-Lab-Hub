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
Process = manager.Namespace()
Process.music_process = ""

def play_music(song_name):
    print(f"music thread " + song_name)
    # Process.music_process_id = os.getpid()
    music = subprocess.Popen(["aplay music_files/let-the-living-beware.wav &"], shell=True)
    time.sleep(1)
    print(music.pid)
    print(Process.music_process.Popen.pid())

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
        pid = subprocess.run(["echo '$!'"], capture_output=True, shell=True)
        print(pid)
        if (Process.music_process.Popen.pid() is not 0):
            print(f"hello")
            subprocess.run(["kill " + str(Process.music_process_id)], capture_output=False, shell=True)
        else:
            print(f"there")
    time.sleep(0.5)  # Small delay to keep from spamming output messages.
