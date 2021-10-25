#!/usr/bin/python3
import adafruit_mpr121
import board
import busio
import logging
import multiprocessing
import os
import random
import re
import subprocess
import time

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Global process variable control.
manager = multiprocessing.Manager()
Current = manager.Namespace()
Current.pid = ""
Current.name = ""
Current.paused = False

# Helper Functions
def get_pid(pid):
    return re.sub("[^0-9]", "", str(pid))

def ongoing_song():
    return Current.pid is not ""

def cancel_current_song():
    subprocess.run(["kill " + Current.pid], capture_output=False, shell=True)
    # Show that song is now empty
    Current.pid = ""
    Current.name = ""
    Current.paused = False
    logging.info("Stopped song with pid: " + Current.pid)

def same_song(song):
    return Current.name is song

def pause_current_song():
    subprocess.run(["kill -STOP " + Current.pid], capture_output=False, shell=True)
    Current.paused = True
    
def resume_current_song():
    subprocess.run(["kill -CONT " + Current.pid], capture_output=False, shell=True)
    Current.paused = False

def play_music(song):
    if not same_song(song):
        music = subprocess.Popen(["aplay music_files/" + song + " & echo \"$!\""], stdout=subprocess.PIPE, shell=True)
        Current.pid = get_pid(music.stdout.readline())
        Current.name = song
        Current.paused = False
        logging.info("Started playing " + song + " at pid " + Current.pid)

# Get song list. There will always be 11 songs available
songs = os.listdir('music_files/')
logging.info("All songs: " + str(songs))

# Music Box Functionality
while True:
    for i in range(5):
        # Play song buttons
        if mpr121[i].value:
            if ongoing_song():
                cancel_current_song()
            music = multiprocessing.Process(target=play_music, args=(songs[i],))
            music.start()
            break
            
    # Stop everything button
    if mpr121[11].value:
        if ongoing_song():
            if Current.paused:
                resume_current_song()
            else:
                pause_current_song()
        else:
            music = multiprocessing.Process(target=play_music, args=(songs[random.randint(0,4)],))
            music.start()
    time.sleep(0.25)  # Small delay to keep from spamming output messages.
