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

# Setup
i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Load songs
songs = os.listdir('music_files/')
logging.info("All songs: " + str(songs))

# Crossprocess variable control
manager = multiprocessing.Manager()
Box = manager.Namespace()
Box.current_song_name = ""
Box.current_song_pid = ""
Box.current_song_index = -1
Box.shuffle = False
Box.mode = 0

# Helper Functions
def get_pid(pid):
    return re.sub("[^0-9]", "", str(pid))

def ongoing_song():
    return Box.current_song_pid is not ""

def cancel_current_song():
    subprocess.run(["kill " + Box.current_song_pid], capture_output=False, shell=True)
    # Show that song is now empty
    Box.current_song_pid = ""
    Box.current_song_name = ""
    Box.current_song_index = -1
    logging.info("Stopped song with pid: " + Box.current_song_pid + "\nBox reset.")
    Box.shuffle = False
    Box.mode = 0

def same_song(song):
    return Box.current_song_name is song

def play_music(song):
    # Looping
    if Box.mode is not 0:
        if Box.shuffle: 
            # Allowing repeats
            Box.current_song_index = random.randint(0,6)
            song = songs[Box.current_song_index]
        else:
            if Box.mode is 1:
                # Single song loop
                song = Box.current_song_name
            if Box.mode is 2:
                # Multi song loop, linear
                song = songs[Box.current_song_index+1]
    
    if not same_song(song) or Box.mode is 1:
        music = subprocess.Popen(["aplay music_files/" + song + " & echo \"$!\""], stdout=subprocess.PIPE, shell=True)
        Box.current_song_pid = get_pid(music.stdout.readline())
        Box.current_song_name = song
        logging.info("Started playing " + song + " at pid " + Box.current_song_pid)         

def shuffle():
    Box.shuffle = not Box.shuffle
    print(f"shuffle state " + str(Box.shuffle))
    if not ongoing_song:
        Box.current_song_index = random.randint(0,6)
        music = multiprocessing.Process(target=play_music, args=(songs[Box.current_song_index],))
        music.start()

def mode_change():
    # Modes available: 
    # Note: if shuffle is on, loop single works the same as loop playlist
    # - Loop off (0)
    # - Loop single (1)
    # - Loop playlist (2)
    Box.mode = (Box.mode + 1) % 3
    print(f"box mode " + str(Box.mode))
    
# Unused pausing functionality. Perhaps I can add something for this if I iterate on the physical design.
# def pause_current_song():
#     subprocess.run(["kill -STOP " + Box.current_song_pid], capture_output=False, shell=True)
#     Current.paused = True
    
# def resume_current_song():
#     subprocess.run(["kill -CONT " + Box.current_song_pid], capture_output=False, shell=True)
#     Current.paused = False

def update_display():
    x = 1
    

# Music Box Functionality (10 sensors)
while True:
    update_display()

    # Loop off
    if Box.mode is 0: 
        # Play one song
        for i in range(7):
            if mpr121[i].value:
                if ongoing_song():
                    cancel_current_song()
                music = multiprocessing.Process(target=play_music, args=(songs[i],))
                Box.current_song_index = i
                Box.song_process = music
                music.start()
                # Ensure we only register one touch at a time
                break

        if mpr121[9].value:
            shuffle()

        if mpr121[10].value:
            mode_change()

        # Reset box
        if mpr121[11].value:
            if ongoing_song():
                cancel_current_song()
    else:
        music = multiprocessing.Process(target=play_music, args=("",))
        music.start()
                
    time.sleep(0.25)  # Small delay to keep from spamming output messages.
