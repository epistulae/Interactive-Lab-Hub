import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565
from random import randrange
import numpy as np

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
date_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
menu_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

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

# Common vars
grey = "#E5E5E5"

def main_screen():
    cur_date = time.strftime("%m/%d/%Y", time.localtime())
    cur_hour = time.localtime()[3]
    
    # Print day
    y = top
    x = font.getsize(" ")[0]*11
    draw.text((x,y), cur_date, font=date_font, fill=grey)
    line_inc = font.getsize(cur_date)[1]
    y += line_inc*1.7
    x = 0
    
    # Enumerate the 7 buckets.
    if (cur_hour == 24) or ((cur_hour >= 1) and (cur_hour < 6)):
        draw.text((x,y), "All the world's asleep.", font=font, fill="#5981D5")
        y += line_inc
        draw.text((x,y), "You should sleep too!", font=font, fill="#5981D5")
    elif (cur_hour >= 6) and (cur_hour < 9):
        draw.text((x,y), "Early bird gets the", font=font, fill="#59D5AF")
        y += line_inc
        draw.text((x,y), "worm. Go you!", font=font, fill="#59D5AF")
    elif (cur_hour >= 9) and (cur_hour < 12):
        draw.text((x,y), "I need coffee...", font=font, fill="#5DD559")
        y += line_inc
        draw.text((x,y), "☕ ☕ ☕", font=font, fill="#5DD559")
    elif (cur_hour >= 12) and (cur_hour < 15):
        draw.text((x,y), "Food time! Go eat!", font=font, fill="#FD9106")
        y += line_inc
        draw.text((x,y), "Seriously, go!", font=font, fill="#FD9106")
    elif (cur_hour >= 15) and (cur_hour < 18):
        draw.text((x,y), "Let's get some", font=font, fill="#BDFD06")
        y += line_inc
        draw.text((x,y), "afternoon tea. Matcha?", font=font, fill="#BDFD06")
    elif (cur_hour >= 18) and (cur_hour < 21):
        draw.text((x,y), "Dinner time!", font=font, fill="#FF3E2E")
        y += line_inc
        draw.text((x,y), "Let's get cookin'!", font=font, fill="#FF3E2E")
    elif (cur_hour >= 21) and (cur_hour < 24):
        draw.text((x,y), "The day is almost done.", font=font, fill="#FF2E80")
        y += line_inc
        draw.text((x,y), "Enjoy your evening :)", font=font, fill="#FF2E80")
    y += line_inc*2.3
    draw.text((x,y), "↑ inspiration and time", font=menu_font, fill=grey)
    y += line_inc*1
    draw.text((x,y), "↓ take a break", font=menu_font, fill=grey)
   
    # Display image.
    disp.image(image, rotation)
    
# Preselect a quote in the beginning.
selected_quote = randrange(10)
selected_color = randrange(10)

# Populated 10 quotes
quotes = ["No pressure, no diamonds."]
quotes.append("Stay foolish to stay sane.")
quotes.append("Dream big and dare to fail.")
quotes.append("Leave no stone unturned.")
quotes.append("No guts, no story.")
quotes.append("Begin anywhere.")
quotes.append("Live your dreams.")
quotes.append("You get what you give.")
quotes.append("What we think, we become.")
quotes.append("And still, I rise.")

# Populated 10 color options
colors = ["#FB5F4C"]
colors.append("#FBB34C")
colors.append("#DBFB4C")
colors.append("#71FB4C")
colors.append("#4CFBAB")
colors.append("#4CE3FB")
colors.append("#4C9EFB")
colors.append("#727DFC")
colors.append("#AF72FC")
colors.append("#FE53CA")

def inspiration():
    cur_min_sec = time.strftime("%M:%S", time.localtime())
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    # Print time
    y = top + 8
    x = font.getsize(" ")[0]*15
    draw.text((x,y), cur_min_sec, font=date_font, fill=grey)
    line_inc = font.getsize(cur_min_sec)[1]
    y += line_inc*2.5
    x = 0
    
    # Print quote
    draw.text((x,y), quotes[selected_quote], font=font, fill=colors[selected_color])
    
    # Menu
    y += line_inc*2.5
    draw.text((x,y), "↑ randomize!", font=menu_font, fill=grey)
    y += line_inc*1
    draw.text((x,y), "↓ back to main", font=menu_font, fill=grey)
    
    # Display image.
    disp.image(image, rotation)
    
    
# Brightness array black to white to black in 10 steps
brightness = [20]
brightness.append(60)
brightness.append(100)
brightness.append(165)
brightness.append(225)
brightness.append(245)
brightness.append(225)
brightness.append(165)
brightness.append(100)
brightness.append(60)
 
def mental_minute_menu():
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    line_inc = font.getsize(" ")[1]
    y = line_inc*2
    x = font.getsize(" ")[0]*2
    
    draw.text((x,y), "Shall we take a break?", font=font, fill=colors[selected_color])
    
    # Menu
    y += line_inc*2.5
    draw.text((0,y), "↑ take that break~", font=menu_font, fill=grey)
    y += line_inc*1
    draw.text((0,y), "↓ back to main", font=menu_font, fill=grey)
       
    # Display image.
    disp.image(image, rotation)
    
def mental_minute():
    mental_minute_starting()
    breathe_minute(60)
    mental_minute_complete()  
    
# Ready for mental minute?
def mental_minute_starting():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    line_inc = font.getsize(" ")[1]
    y = line_inc*2
    x = font.getsize(" ")[0]*2
    selected_color = randrange(10)
    
    draw.text((x,y), "Let's take a minute...", font=font, fill=colors[selected_color])
    y += line_inc*1.7
    draw.text((x,y), "Breathe in", font=font, fill=grey)
    y += line_inc
    draw.text((x,y), "as the light brightens", font=font, fill=grey)
    y += line_inc
    draw.text((x,y), "and out as it dims.", font=font, fill=grey)
    
    # Display image.
    disp.image(image, rotation)
    
    time.sleep(5)

# Mental minute complete
def mental_minute_complete():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    line_inc = font.getsize(" ")[1]
    y = line_inc*2
    x = font.getsize(" ")[0]*2
    selected_color = randrange(10)
    
    draw.text((x,y), "Great job!", font=font, fill=colors[selected_color])
    
    y += line_inc*2.5
    draw.text((x,y), "Returning to main...", font=menu_font, fill=grey)
    
    # Display image.
    disp.image(image, rotation)
    
    time.sleep(5)
    
def breathe_minute(seconds):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    disp.image(image, rotation)
    while seconds > 0:
        i = seconds % 10
        print(i)
        draw.rectangle((0, 0, width, height), outline=0, fill=(brightness[i], brightness[i], brightness[i]))
        disp.image(image, rotation)
        #disp.fill(color565(bright, bright, bright))
        time.sleep(1)
        seconds -= 1

# Lab 2 Clock
while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    # Main screen
    if state == 0:
        main_screen()
        # Top: state 1: inspiration
        if buttonB.value and not buttonA.value:
            state = 1
        # Bottom: state 2: mental break
        elif not buttonB.value and buttonA.value:
            state = 2

    # Inspiration screen
    elif state == 1:
        inspiration()
        
        # Top: randomize
        if buttonB.value and not buttonA.value:
            selected_quote = randrange(10)
            selected_color = randrange(10)
        # Bottom: return to main
        elif not buttonB.value and buttonA.value:
            state = 0

    # Mental health break
    elif state == 2:
        mental_minute_menu()
        
        # Top: start mental minute and return to main when complete
        if buttonB.value and not buttonA.value:
            mental_minute()
            state = 0
        # Bottom: return to main
        elif not buttonB.value and buttonA.value:
            state = 0

    time.sleep(1)
