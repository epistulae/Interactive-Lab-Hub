#!/usr/bin/python3
# Box Imports
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

#Display Imports
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565
from random import randrange
import numpy as np

# Setup
i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Display
grey = "#E5E5E5"
cyan = "#47d6be"
blue = "#2e9aff"

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

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

def current_done():
    # Nothing to check
    if Box.current_song_pid is "":
            return
    try:
        os.kill(int(Box.current_song_pid), 0)
    except OSError:
        Box.current_song_pid = ""
        Box.current_song_name = ""
        Box.current_song_index = -1
        return True
    return False

def play_music(song):
    play = False
    # Looping
    if Box.mode is not 0:
        play = current_done()
        if play:
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
        if song is not "loop":
            play = True
    else:
        play = not same_song(song)
        
    if play:
        music = subprocess.Popen(["aplay music_files/" + song + " & echo \"$!\""], stdout=subprocess.PIPE, shell=True)
        Box.current_song_pid = get_pid(music.stdout.readline())
        Box.current_song_name = song
        logging.info("Started playing " + song + " at pid " + Box.current_song_pid)    
    update_display()

def shuffle():
    Box.shuffle = not Box.shuffle
    if not ongoing_song():
        Box.current_song_index = random.randint(0,6)
        music = multiprocessing.Process(target=play_music, args=(songs[Box.current_song_index],))
        music.start()
    update_display()

def mode_change():
    # Modes available: 
    # Note: if shuffle is on, loop single works the same as loop playlist
    # - Loop off (0)
    # - Loop single (1)
    # - Loop playlist (2)
    Box.mode = (Box.mode + 1) % 3
    update_display()
    
# Unused pausing functionality. Perhaps I can add something for this if I iterate on the physical design.
# def pause_current_song():
#     subprocess.run(["kill -STOP " + Box.current_song_pid], capture_output=False, shell=True)
#     Current.paused = True
    
# def resume_current_song():
#     subprocess.run(["kill -CONT " + Box.current_song_pid], capture_output=False, shell=True)
#     Current.paused = False

def check_input():
    # Play one song
    for i in range(7):
        if mpr121[i].value:
            if ongoing_song():
                cancel_current_song()
            music = multiprocessing.Process(target=play_music, args=(songs[i],))
            Box.current_song_index = i
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

def update_display():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    disp.image(image, rotation)
    
    song = Box.current_song_name.split(".",1)[0].replace("-", " ").title()
    if song is "":
        song = "Nothing playing"
    
    mode = "Mode: "
    if Box.mode is 0:
        mode += "Single Song"
    elif Box.mode is 1:
        mode += "Loop one song"
    elif Box.mode is 2:
        mode += "Loop playlist"
    
    shuffle = "Shuffle "
    if Box.shuffle:
        shuffle += "on"
    else:
        shuffle += "off"
    
    # Screen
    line_inc = font.getsize(song)[1]
    y = top + line_inc*0.8
    draw.text((0,y), song, font=font, fill=grey)
    y += line_inc*1.7
    draw.text((0,y), mode, font=font, fill=cyan)
    y += line_inc*1.7
    draw.text((0,y), shuffle, font=font, fill=blue)
    
    disp.image(image, rotation)

# Music Box Functionality (10 sensors)
update_display()
while True:
    current_done()
    check_input()
    # Loop
    if Box.mode is not 0: 
        music = multiprocessing.Process(target=play_music, args=("loop",))
        music.start()
                
    time.sleep(0.25)  # Small delay to keep from spamming output messages.
