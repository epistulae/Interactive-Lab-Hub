# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
import time, sys
import multiprocessing, signal

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import adafruit_ssd1306

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
tracking_file = open("tracking.txt","r")

tracking_day = int(tracking_file.readline())
habit_a = list(map(int, tracking_file.readline().split(" ")))
habit_b = list(map(int, tracking_file.readline().split(" ")))

tracking_file.close()

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

# Note: in retrospec, not going to keep spending time on this. I don't have a display big enough 
# to really do this properly as I envisioned. Otherwise, it's just a bit confusing to use.

while True:
    try:
        display_stats()
        time.sleep(0.5)
    except KeyboardInterrupt:
        # Write to file only when program exits to limit file writes.
        tracking_file = open("tracking.txt","w")
        tracking_file.write(str(tracking_day)+"\n")
        tracking_file.write(' '.join([str(day) for day in habit_a])+"\n")
        tracking_file.write(' '.join([str(day) for day in habit_b]))
        sys.exit()

