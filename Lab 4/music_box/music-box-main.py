#!/usr/bin/python3
import adafruit_mpr121
import board
import busio
import logging
import multiprocessing
import re
import subprocess
import time

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Global process variable control.
manager = multiprocessing.Manager()
Current = manager.Namespace()
Current.pid = ""

def get_pid(pid):
    return re.sub("[^0-9]", "", str(pid))

def ongoing_song():
    return Current.pid is not ""

def stop_current_song():
    subprocess.run(["kill " + Current.pid], capture_output=False, shell=True)
    # Show that song is now empty
    Current.pid = ""
    logging.info("Stopped song with pid: " + Current.pid)
    
def play_music(song):
    music = subprocess.Popen(["aplay music_files/" + song + " & echo \"$!\""], stdout=subprocess.PIPE, shell=True)
    Current.pid = get_pid(music.stdout.readline())
    logging.info("Started playing " + song + " at pid " + Current.pid)

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    if mpr121[7].value:
        Process.music_process_id = subprocess.run(["aplay music_files/rex-incognito.wav", "&"], capture_output=True, shell=True)
        print(f"Thread started rex")
        print(Current.pid)
    if mpr121[9].value:
        music = multiprocessing.Process(target=play_music, args=("let-the-living-beware.wav",))
        music.start()
        print(f"Thread started living")
    if mpr121[11].value:
        print(Current.pid)
        if (ongoing_song()):
            print(f"hello")
            stop_current_song()
        else:
            print(f"there")
    time.sleep(0.5)  # Small delay to keep from spamming output messages.
