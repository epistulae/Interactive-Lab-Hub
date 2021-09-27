import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

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

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Lab 2 Clock Formatting function
def set_next_x(x, string):
    x += font.getsize(string)[0]
    return x

# Clock states:
# State = 0 -> Base welcome screen (Non-exact time)
#              Buckets (7): Midnight to 6 am, 6 am to 9 am, 9 am to noon
#              noon to 3 pm, 3 pm to 6 pm, 6 pm to 9 pm, 9 pm to midnight.
# State = 1 -> Top button from state 0, show exact time. With random
#              inspirational quote. (Selected from set of 10.)
#              Use top button refresh quote.
#              Botton button to return to main.
# State = 2 -> Bottom button from state 0, mental health break.
#              Top button to adjust how long: 1 to 5 minutes.
#              Bottom button to return to main.
#              Top and bottom button to start mental break countdown.
#              TODO: maybe brighten and dim following breaths. 

# Initial state on main
state = 0

def main_screen():
    cur_date = time.strftime("%m/%d/%Y")
    cur_hour = time.localtime()[3]
    
    # Print day
    y = top
    x = font.getsize(" ")[0]*11
    grey = "#e8e8e8"
    draw.text((x,y), cur_date, font=font, fill=grey)
    line_inc = font.getsize(cur_date)[1]
    y += line_inc*2
    x = 0
    
    # Enumerate the 7 buckets.
    if (cur_hour == 24) or ((cur_hour >= 1) and (cur_hour < 6)):
        draw.text((x,y), "All the world's asleep.", font=font, fill="#5981D5")
        y += line_inc
        draw.text((x,y), "You should sleep too! Zzz.", font=font, fill="#5981D5")
    elif (cur_hour >= 6) and (cur_hour < 9):
        draw.text((x,y), "Early bird gets the worm.", font=font, fill="#59D5AF")
        y += line_inc
        draw.text((x,y), "Go you!", font=font, fill="#59D5AF")
    elif (cur_hour >= 9) and (cur_hour < 12):
        draw.text((x,y), "I need coffee...", font=font, fill="#5DD559")
        y += line_inc
        draw.text((x,y), "☕ ☕ ☕", font=font, fill="#5DD559")
    elif (cur_hour >= 12) and (cur_hour < 15):
        draw.text((x,y), "Food time! Go eat!", font=font, fill="#FD9106")
        y += line_inc
        draw.text((x,y), "Seriously, go!", font=font, fill="#FD9106")
    elif (cur_hour >= 15) and (cur_hour < 18):
        draw.text((x,y), "Let's get some afternoon tea.", font=font, fill="#BDFD06")
        y += line_inc
        draw.text((x,y), "Matcha or earl grey?", font=font, fill="#BDFD06")
    elif (cur_hour >= 18) and (cur_hour < 21):
        draw.text((x,y), "Dinner time!", font=font, fill="#FF3E2E")
        y += line_inc
        draw.text((x,y), "Let's get cookin'!", font=font, fill="#FF3E2E")
    elif (cur_hour >= 21) and (cur_hour < 24):
        draw.text((x,y), "The day is almost done...", font=font, fill="#FF2E80")
        y += line_inc
        draw.text((x,y), "Enjoy your evening :)", font=font, fill="#FF2E80")
    y += line_inc
    draw.text((x,y), "↑ inspiration; ↓ take a break", font=font, fill="#E5E5E5")
    # Display image.
    disp.image(image, rotation)
        
        
while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    # Main screen
    if state == 0:
        main_screen()

    # Inspiration screen (static)
    elif state == 1:
        disp.fill(color565(255, 255, 255))

    # Mental health break (static)
    elif state == 2:
        disp.fill(color565(255, 255, 255))
    
    if buttonB.value and not buttonA.value:
        if setting == 0:
           print("hello")
           state = 1
        else:
           state = 0
           print("there")
    time.sleep(1)
