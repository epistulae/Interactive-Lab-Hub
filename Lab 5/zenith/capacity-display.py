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

# # Screen setup
# oled.fill(0)
# oled.show()

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

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
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Display day to track
# Note: In final, will store and read in external file
tracking_day = 1

while True:
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    # Write two lines of text.

    draw.text((x, top+8),       "Tracking Day: ",  font=font, fill=255)
    draw.text((x, top+16),     str(tracking_day), font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
  
#     # undraw the previous circle
#     draw_circle(center_x, center_y, radius, col=0)

#     # if bouncing off right
#     if center_x + radius >= oled.width:
#         # start moving to the left
#         x_inc = -1
#     # if bouncing off left
#     elif center_x - radius < 0:
#         # start moving to the right
#         x_inc = 1

#     # if bouncing off top
#     if center_y + radius >= oled.height:
#         # start moving down
#         y_inc = -1
#     # if bouncing off bottom
#     elif center_y - radius < 0:
#         # start moving up
#         y_inc = 1

#     # go more in the current direction
#     center_x += x_inc
#     center_y += y_inc

#     # draw the new circle
#     draw_circle(center_x, center_y, radius)
#     # show all the changes we just made
#     oled.show()
