import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

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

# Lab 2 Clock Formatting function
def set_next_x(x, string):
    x += font.getsize(string)[0]
    return x

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Lab 2 Clock
    # Read current time.
    cur_date = time.strftime("%m/%d/%Y")
    cur_hour = time.strftime("%H")
    cur_min_sec = time.strftime("%M:%S")

    # Print day
    y = top
    x = font.getsize(" ")[0]*11
    grey = "#e8e8e8"
    draw.text((x,y), cur_date, font=font, fill=grey)
    line_inc = font.getsize(cur_date)[1]
    y += line_inc*2

    #test
    cur_hour = "5"
    # Musical Lyrics: A new lyric for every hour of the day
    x = 0

    # Style by Taylor Swift
    if cur_hour == "0":
      draw.text((x,y), "Midnight,", font=font, fill="#8ca7ff")
      x = set_next_x(x, "Midnight,")
      draw.text((x,y), " you come and", font=font, fill=grey)
      x = 0
      y += line_inc
      draw.text((x,y), "pick me up, no headlights", font=font, fill=grey)

    # 1 AM by Beautiful Creatures
    elif cur_hour == "1":
      draw.text((x,y), "1 A.M.", font=font, fill="#8241f2")
      x = set_next_x(x, "1 A.M.")
      draw.text((x,y), " and I'm cold again", font=font, fill=grey)
      x = 0
      y += line_inc
      draw.text((x,y), "I'm alone again and", font=font, fill=grey)
      y += line_inc
      draw.text((x,y), "I need a friend", font=font, fill=grey)

    # 2:AM by Anthony Russo
    elif cur_hour == "2":
      draw.text((x,y), "And now it's", font=font, fill=grey)
      x = set_next_x(x, "And now it's")
      draw.text((x,y), " 2 A.M.", font=font, fill="#8835cc")
      x = 0
      y += line_inc
      draw.text((x,y), "I'm up, all in my head", font=font, fill=grey)

    # Heartless (Remix) by Kanye West
    elif cur_hour == "3":
      draw.text((x,y), "Why we up ", font=font, fill=grey)
      x = set_next_x(x, "Why we up ")
      draw.text((x,y), " 3 A.M.", font=font, fill="#bd34d9")
      x = set_next_x(x, " 3 A.M.")
      draw.text((x,y), " on the phone?", font=font, fill=grey)
      x = 0
      y += line_inc
      draw.text((x,y), "Why do she be so mad at me for?", font=font, fill=grey)

    # 4 AM and Nothing New by Sugarplum Fairy
    elif cur_hour == "4":
      draw.text((x,y), "4 A.M.", font=font, fill="#eb3dd1")
      x = set_next_x(x, "4 A.M.")
      draw.text((x,y), " and nothing new", font=font, fill=grey)
      x = 0
      y += line_inc
      draw.text((x,y), "You wear your shiny", font=font, fill=grey)
      y += line_inc
      draw.text((x,y), "Sunday shoes", font=font, fill=grey)

    # Before It's Light by Novi Novak
    elif cur_hour == "5":
      draw.text((0,y), "I think about it every night", font=font, fill=grey)
      y += line_inc
      draw.text((x,y), "when I'm up til", font=font, fill=grey)
      x = set_next_x(x, "when I'm up til")
      draw.text((x,y), " Five AM", font=font, fill="#f53699")
      y += line_inc
      draw.text((0,y), "Good life out of sight", font=font, fill=grey)

    # Mafia by SCH
    elif cur_hour == "6":
      x = 0
    elif cur_hour == "7":
      x = 0
    elif cur_hour == "8":
      x = 0
    elif cur_hour == "9":
      x = 0
    elif cur_hour == "10":
      x = 0
    elif cur_hour == "11":
      x = 0
    elif cur_hour == "12":
      x = 0
    elif cur_hour == "13":
      x = 0
    elif cur_hour == "14":
      x = 0
    elif cur_hour == "15":
      x = 0
    elif cur_hour == "16":
      x = 0
    elif cur_hour == "17":
      x = 0
    elif cur_hour == "18":
      x = 0
    elif cur_hour == "19":
      x = 0
    elif cur_hour == "20":
      x = 0
    elif cur_hour == "21":
      x = 0
    elif cur_hour == "22":
      x = 0
    elif cur_hour == "23":
      x = 0

    x = font.getsize(" ")[0]*15
    y += line_inc*2
    draw.text((x,y), cur_min_sec, font=font, fill=grey)

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
