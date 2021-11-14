#!/usr/bin/env python3

import adafruit_mpr121
import argparse
import board
import busio
from enum import Enum
from rpi_ws281x import *
import time

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Colors
class Colors(Enum):
    INCOMPLETE = Color(237, 108, 2)
    COMPLETE = Color(20, 164, 217)
    PINPRICK = Color(255, 245, 222)
    RED = Color(235, 52, 52)

class Star:
    def __init__(self, index, complete=False):
        self.index = index
        self.complete = complete
        self.next_star = None
        # Previous stars: (star, connector)
        self.prior_stars = []

pinpricks = [0, 58, 59, 60, 76, 77, 98, 99, 100, 101, 122, 123, 124, 125, 130, 142, 143] 

# Constellation Graphs
hourglass = Star(1)

hourglass_2 = Star(6)
hourglass.next_star = hourglass_2
hourglass_2.prior_stars.append((hourglass, [2, 3, 4, 5]))

hourglass_3 = Star(10)
hourglass_2.next_star = hourglass_3
hourglass_3.prior_stars.append((hourglass, [23, 24]))
hourglass_3.prior_stars.append((hourglass_2, [7, 8, 9]))

hourglass_4 = Star(14)
hourglass_3.next_star = hourglass_4
hourglass_4.prior_stars.append((hourglass_3, [11, 12, 13]))

hourglass_final = Star(19)
hourglass_5.final = True
hourglass_4.next_star = hourglass_5
hourglass_5.prior_stars.append((hourglass_3, [20, 21, 22]))
hourglass_5.prior_stars.append((hourglass_4, [15, 16, 17, 18]))

# -------------------------------------------------------

teapot = Star(50)

teapot_2 = Star(46)
teapot.next_star = teapot_2
teapot_2.prior_stars.append((teapot, [47, 48, 49]))

teapot_3 = Star(44)
teapot_2.next_star = teapot_3
teapot_3.prior_stars.append((teapot, [25,26]))
teapot_3.prior_stars.append((teapot_2, [45]))

teapot_4 = Star(30)
teapot_3.next_star = teapot_4
teapot_4.prior_stars.append((teapot_3, [27, 28, 29]))

teapot_5 = Star(33)
teapot_4.next_star = teapot_5
teapot_5.prior_stars.append((teapot_3, [41, 42, 43]))
teapot_5.prior_stars.append((teapot_4, [31, 32]))

teapot_6 = Star(35)
teapot_5.next_star = teapot_6
teapot_6.prior_stars.append((teapot_5, [34]))

teapot_7 = Star(37)
teapot_6.next_star = teapot_7
teapot_7.prior_stars.append((teapot_6, [36]))

teapot_final = Star(57)
teapot_final.final = True
teapot_7.next_star = teapot_final
teapot_final.prior_stars.append((teapot, [51, 52, 53, 54, 55, 56]))
teapot_final.prior_stars.append((teapot_5, [39, 40]))
teapot_final.prior_stars.append((teapot_7, [38]))

# -------------------------------------------------------

triangle = Star(65)

triangle_2 = Star(61)
triangle.next_star = triangle_2
triangle_2.prior_stars.append((triangle, [62, 63]))

triangle_3 = Star(68)
triangle_3.final = True
triangle_2.next_star = triangle_3
triangle_3.prior_stars.append((triangle, [66, 67]))
triangle_3.prior_stars.append((triangle_2, [69, 70, 71]))

# -------------------------------------------------------

butterfly = Star(72)

butterfly_2 = Star(97)
butterfly.next_star = butterfly_2
butterfly_2.prior_stars.append((butterfly, [73]))

butterfly_3 = Star(75)
butterfly_2.next_star = butterfly_3
butterfly_3.prior_stars.append((butterfly_2, [74]))

butterfly_4 = Star(93)
butterfly_3.next_star = butterfly_4
butterfly_4.prior_stars.append((butterfly_2, [94, 95, 96]))
butterfly_4.prior_stars.append((butterfly_3, [78, 79, 80]))

butterfly_5 = Star(87)
butterfly_4.next_star = butterfly_5
butterfly_5.prior_stars.append((butterfly_4, [81, 82, 83, 84, 85, 86]))

butterfly_6 = Star(88)
butterfly_6.final = True
butterfly_5.next_star = butterfly_6
butterfly_6.prior_stars.append((butterfly_4, [89, 90, 91, 92]))

# -------------------------------------------------------

orion = Star(102)

orion_2 = Star(105)
orion.next_star = orion_2
orion_2.prior_stars.append((orion, [103, 104]))

orion_3 = Star(108)
orion_2.next_star = orion_3
orion_3.prior_stars.append((orion_2, [106, 107]))

orion_4 = Star(109)
orion_3.next_star = orion_4

orion_5 = Star(112)
orion_4.next_star = orion_5
orion_5.prior_stars.append((orion, [110, 111]))

orion_6 = Star(114)
orion_5.next_star = orion_6
orion_6.prior_stars.append((orion_5, [113]))

orion_7 = Star(116)
orion_6.next_star = orion_7
orion_7.prior_stars.append((orion_6, [115]))

orion_8 = Star(118)
orion_8.final = True
orion_7.next_star = orion_8
orion_8.prior_stars.append((orion_7, [117]))
orion_8.prior_stars.append((orion_3, [119, 120, 121]))

# -------------------------------------------------------

serpens = Star(40)

serpens_2 = Star(37)
serpens.next_star = serpens_2
serpens_2.prior_stars.append((serpens, [138, 139]))

serpens_3 = Star(35)
serpens_2.next_star = serpens_3
serpens_3.prior_stars.append((serpens, [141]))
serpens_3.prior_stars.append((serpens_2, [136]))

serpens_4 = Star(33)
serpens_3.next_star = serpens_4
serpens_4.prior_stars.append((serpens_3, [127, 128]))

serpens_5 = Star(29)
serpens_4.next_star = serpens_5
serpens_5.prior_stars.append((serpens_4, [131, 132]))

serpens_6 = Star(26)
serpens_6.final = True
serpens_5.next_star = serpens_6
serpens_6.prior_stars.append((serpens_5, [127, 128]))

# -------------------------------------------------------

narwhale = Star(0)

narwhale_2 = Star(0)
narwhale.next_star = narwhale_2

narwhale_3 = Star(0)
narwhale_2.next_star = narwhale_3

narwhale_4 = Star(0)
narwhale_3.next_star = narwhale_4

narwhale_5 = Star(0)
narwhale_4.next_star = narwhale_5

narwhale_6 = Star(0)
narwhale_6.final = True
narwhale_5.next_star = narwhale_6

# -------------------------------------------------------

draco = Star(0)

draco_2 = Star(0)
draco.next_star = draco_2

draco_3 = Star(0)
draco_2.next_star = draco_3

draco_4 = Star(0)
draco_3.next_star = draco_4

draco_5 = Star(0)
draco_4.next_star = draco_5

draco_6 = Star(0)
draco_5.next_star = draco_6

draco_7 = Star(0)
draco_6.next_star = draco_7

draco_8 = Star(0)
draco_7.next_star = draco_8

draco_9 = Star(0)
draco_8.next_star = draco_9

draco_10 = Star(0)
draco_9.next_star = draco_10

draco_11 = Star(0)
draco_10.next_star = draco_11

draco_12 = Star(0)
draco_11.next_star = draco_12

draco_13 = Star(144)
draco_13.final = True
draco_12.next_star = draco_13
draco_13.prior_stars.append((draco_12, [145]))

# -------------------------------------------------------

shield = Star(0)

shield_2 = Star(0)

shield_3 = Star(0)

shield_4 = Star(0)

shield_5 = Star(0)
shield_5.final = True

# Habit Lists in fill order
habit_a = [serpens] # narwhale, serpens, draco, shield
habit_b = [hourglass, teapot, triangle, orion, butterfly]

# Show state of one constellation (habit)
def displayHabitConstellation(strip, star):
    # All stars
    while True:
        led_color = Colors.COMPLETE.value if star.complete else Colors.INCOMPLETE.value
        # Star
        strip.setPixelColor(star.index, led_color)
        update = star.complete 
        # Connectors
        for prior in star.prior_stars:
            if update:
                led_color = Colors.COMPLETE.value if prior[0].complete else Colors.INCOMPLETE.value
            leds = prior[1]
            for led in leds:
                strip.setPixelColor(led, led_color)
        if star.final:
            break
        star = star.next_star

    # Send to display
    strip.show()

def displayPinpricks(strip):
    for led in pinpricks:
        strip.setPixelColor(led, Colors.PINPRICK.value)
    
def fillRemaining(strip, index):
    while index < LED_COUNT:
        strip.setPixelColor(index, Colors.RED.value)
        index += 1
    
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

# def testing(strip):
#     strip.setPixelColor(0, BACKGROUND)
#     strip.setPixelColor(1, COMPLETE)
#     strip.setPixelColor(2, COMPLETE)
#     strip.setPixelColor(3, COMPLETE)
#     strip.setPixelColor(4, COMPLETE)
#     strip.setPixelColor(5, COMPLETE)
#     strip.setPixelColor(6, COMPLETE)
#     for i in range(7, 25):
#         strip.setPixelColor(i, INCOMPLETE)
#     strip.show()
        
# def rainbowCycle(strip, wait_ms=20, iterations=5):
#     """Draw rainbow that uniformly distributes itself across all pixels."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)
        

# def theaterChaseRainbow(strip, wait_ms=50):
#     """Rainbow movie theater light style chaser animation."""
#     for j in range(256):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, wheel((i+j) % 255))
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)


# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

 # Setup
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)


print ('Press Ctrl-C to quit.')
if not args.clear:
    print('Use "-c" argument to clear LEDs on exit')

hourglass_2.complete = True
hourglass.complete = True
hourglass_5.complete = True
hourglass_3.complete = True

# Leds
displayPinpricks(strip)
displayHabitConstellation(strip, hourglass)
displayHabitConstellation(strip, teapot)
fillRemaining(strip, 59)

try:
    while True:
        # Inputs
        if mpr121[0].value:
            print("Lights on off")
        elif mpr121[5].value:
            print("Mode cycle")
        elif mpr121[2].value:
            print("Habit A")
        elif mpr121[8].value:
            print("Habit B")
        time.sleep(0.5)
        
except KeyboardInterrupt:
    if args.clear:
        colorWipe(strip, Color(0,0,0), 10)
