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

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Lab 2 Clock Formatting function
def set_next_x(x, string):
    x += font.getsize(string)[0]
    return x

setting = 0

while True:
    if buttonB.value and not buttonA.value:
        setting = 1
        
    if setting == 0:
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
        x = 0

        # Musical Lyrics: A new lyric for every hour of the day
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
          draw.text((0,y), "Demain, les bleus pètent", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "la porte vers", font=font, fill=grey)
          x = set_next_x(x, "la porte vers")
          draw.text((x,y), " six AM", font=font, fill="#f5336d")

        # Transformation by Hey-Zooz
        elif cur_hour == "7":
          x = 0
          draw.text((0,y), "7 o'clock", font=font, fill="#fa2a3f")
          x = set_next_x(x, "7 o'clock")
          draw.text((x,y), " on the dot", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "Like you got it bad", font=font, fill=grey)

        # I Asked God by Quelle Chris
        elif cur_hour == "8":
          draw.text((0,y), "8 in the morning", font=font, fill="#fa4d2a")
          y += line_inc
          draw.text((0,y), "woke up prayed for", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "the lord", font=font, fill=grey)

        # Charged Up by Always Never
        elif cur_hour == "9":
          x = 0
          draw.text((0,y), "Push to start and I hear me", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "on the radio", font=font, fill=grey)
          x = set_next_x(x, "on the radio")
          draw.text((x,y), " 9 AM", font=font, fill="#f76d28")

        # Bands by White Dave
        elif cur_hour == "10":
          draw.text((0,y), "And I've been on 10 since", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "10 in the morning", font=font, fill="#fc9d28")

        # Mornings Eleven by The Magic Numbers
        elif cur_hour == "11":
          x = 0
          draw.text((0,y), "Mornings eleven", font=font, fill="#facc28")
          x = set_next_x(x, "Mornings eleven")
          draw.text((x,y), ", the", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "feelings are severed", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "I can't feel anything at all", font=font, fill=grey)

        # Noon by Estère
        elif cur_hour == "12":
          x = 0
          draw.text((0,y), "And crumple at the", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "height of", font=font, fill=grey)
          x = set_next_x(x, "height of")
          draw.text((x,y), " noon", font=font, fill="#fcf526")

        # Sunday morning by Wolficide
        elif cur_hour == "13":
          x = 0
          draw.text((0,y), "1 pm", font=font, fill="#72ff26")
          x = set_next_x(x, "1 pm")
          draw.text((x,y), " it's about time", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "to clock in", font=font, fill=grey)

        # Hooray by Minus the Bear
        elif cur_hour == "14":
          x = 0
          draw.text((0,y), "It's", font=font, fill=grey)
          x = set_next_x(x, "It's")
          draw.text((x,y), " 2pm", font=font, fill="#19e01c")
          x = set_next_x(x, " 2pm")
          draw.text((x,y), " and our snow", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "is falling still", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "As our good city lay still", font=font, fill=grey)

        # A Public thing by Hit Me TV
        elif cur_hour == "15":
          x = 0
          draw.text((0,y), "Very long time since", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "I got up at", font=font, fill=grey)
          x = set_next_x(x, "I got up at")
          draw.text((x,y), " three PM", font=font, fill="#24f270")

        # Carousel Love by warrenisyellow
        elif cur_hour == "16":
          x = 0
          draw.text((0,y), "Let's make it to rodeo", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "On an avenue, from 8", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "till", font=font, fill=grey)
          x = set_next_x(x, "till")
          draw.text((x,y), " 4 in the afternoon", font=font, fill="#27f59f")

        # Somewhere In The World It's Midnight by Street Sweeper Social Club
        elif cur_hour == "17":
          x = 0
          draw.text((0,y), "Somewhere in the world", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "it's", font=font, fill=grey)
          x = set_next_x(x, "it's")
          draw.text((x,y), " 5pm", font=font, fill="#30f2cb")

        # Beautiful Girls (Remix) by Sean Kingston
        elif cur_hour == "18":
          draw.text((0,y), "We fight all day till", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "6 at night", font=font, fill="#48e7f0")

        # Sock Drawer Blues by Glue
        elif cur_hour == "19":
          draw.text((0,y), "All of this while eating", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "dinner every night at", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "7 pm", font=font, fill="#33bbf5")

        # 8pm by sadeyes
        elif cur_hour == "20":
          x = 0
          draw.text((0,y), "I've got 3 missed calls,", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "it's only", font=font, fill=grey)
          x = set_next_x(x, "it's only")
          draw.text((x,y), " 8 PM", font=font, fill="#2885f7")

        # Dallas by The Flatlanders
        elif cur_hour == "21":
          x = 0
          draw.text((0,y), "Did you ever see Dallas", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "from a DC-", font=font, fill=grey)
          x = set_next_x(x, "from a DC-")
          draw.text((x,y), "9 at night?", font=font, fill="#2e5bff")

        # 10pm by Underscore
        elif cur_hour == "22":
          x = 0
          draw.text((0,y), "It's", font=font, fill=grey)
          x = set_next_x(x, "It's")
          draw.text((x,y), " 10pm", font=font, fill="#2626fc")
          x = set_next_x(x, " 10pm")
          draw.text((x,y), " and I", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "haven't talked to you yet", font=font, fill=grey)

        # Since I've Been Loving You by Led Zeppelin
        elif cur_hour == "23":
          draw.text((0,y), "I've been working from 7", font=font, fill=grey)
          y += line_inc
          draw.text((0,y), "to", font=font, fill=grey)
          x = set_next_x(x, "to")
          draw.text((x,y), " eleven every night", font=font, fill="#6823fc")

        x = font.getsize(" ")[0]*15
        y += line_inc*2
        draw.text((x,y), cur_min_sec, font=font, fill=grey)

        # Display image.
        disp.image(image, rotation)
    else:
        display.fill(color565(255, 255, 255))
    time.sleep(1)
