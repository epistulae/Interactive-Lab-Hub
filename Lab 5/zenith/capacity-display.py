# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
import time
import multiprocessing, signal

import adafruit_ssd1306
import adafruit_mpr121

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Screen setup
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -5
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 10

# Load default font.
font = ImageFont.load_default()

# Display tracking.
# Note: In final, will store and read in external file
tracking_day = 1
habit_a = [0] * 30
habit_b = [0] * 30

habit_a_status = "incomplete"
habit_b_status = "incomplete"
     
# Helper Functions
def display_stats():
     # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    # Write stats.
    if habit_a[tracking_day-1] is 0:
        habit_a_status = "incomplete"
    else:
        habit_a_status = "complete"
     
    if habit_b[tracking_day-1] is 0:
        habit_b_status = "incomplete"
    else:
        habit_b_status = "complete"

    draw.text((x, top+8),      "Tracking Day: " + str(tracking_day),  font=font, fill=255)
    draw.text((x, top+16),     "Habit A: " + habit_a_status, font=font, fill=255)
    draw.text((x, top+24),     "Habit B: " + habit_b_status, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(.1)

while True:
    for i in range(4):
        if mpr121[0].value:
            if tracking_day is not 1:
                tracking_day -= 1
            print(f"Twizzler 0 touched!")
            break
        if mpr121[1].value:
            if tracking_day is not 30:
                tracking_day += 1
            print(f"Twizzler 1 touched!")
            break
        if mpr121[2].value:
            print(f"Twizzler 2 touched!")
            break
        if mpr121[3].value:
            print(f"Twizzler 3 touched!")
            break
    display_stats()
    time.sleep(0.5)
  
