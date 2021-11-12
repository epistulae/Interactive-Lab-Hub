#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
from enum import Enum

# LED strip configuration:
LED_COUNT      = 25      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Colors
class Colors(Enum):
    INCOMPLETE = Color(237, 108, 2)
    COMPLETE = Color(20, 164, 217)
    BACKGROUND = Color(255, 245, 222)

class Star_Type(Enum):
    START = 1
    MIDDLE = 2
    END = 3

class Connector:
    def __init__(self, leds):
        self.leds = leds

class Star:
    def __init__(self, index, type=Star_Type.START, complete=False):
        self.index = index
        self.complete = complete
        self.next_star = None
        self.type = type
        # Previous stars: (star, connector)
        self.prior_stars = []

# Constellation Trees
narwhale = Star(0)
serpens = Star(0)
draco = Star(0)
shield = Star(0)

# Hourglass
hourglass = Star(1, Star_Type.START)

hourglass_2 = Star(6, Star_Type.MIDDLE)
hourglass.next_star = hourglass_2
connector_12 = Connector([2, 3, 4, 5])
hourglass_2.prior_stars.append((hourglass, connector_12))

hourglass_3 = Star(10, Star_Type.MIDDLE)
hourglass_2.next_star = hourglass_3
connector_13 = Connector([23, 24])
connector_23 = Connector([7, 8, 9])
hourglass_3.prior_stars.append((hourglass, connector_13))
hourglass_3.prior_stars.append((hourglass_2, connector_23))

hourglass_4 = Star(14, Star_Type.MIDDLE)
hourglass_3.next_star = hourglass_4
connector_34 = Connector([11, 12, 13])
hourglass_4.prior_stars.append((hourglass_3, connector_34))

hourglass_5 = Star(19, Star_Type.END)
hourglass_4.next_star = hourglass_5
connector_35 = Connector([15, 16, 17, 18])
connector_45 = Connector([20, 21, 22])
hourglass_3.prior_stars.append((hourglass_3, connector_35))
hourglass_3.prior_stars.append((hourglass_4, connector_45))

hourglass_3.complete = True
hourglass_5.complete = True

# Teapot
teapot = Star(0)
triangle = Star(0)
orion = Star(0)
butterfly = Star(0)

# Habit Lists in fill order
habit_a = [narwhale, serpens, draco, shield]
habit_b = [hourglass, teapot, triangle, orion, butterfly]

# Show state of one constellation (habit)
def displayHabitConstellation(strip, star):
    # All stars
    while True:
        led_color = Colors.INCOMPLETE.value
        if star.complete:
            led_color = Colors.COMPLETE.value
        # Star
        strip.setPixelColor(star.index, led_color)
        # Connectors
        for prior in star.prior_stars:
            if star.complete:
                led_color = Colors.COMPLETE.value if prior[0].complete else Colors.INCOMPLETE.value
            leds = prior[1].leds
            for led in leds:
                strip.setPixelColor(led, led_color)
        if star.type is Star_Type.END:
            break
        star = star.next_star

    # Send to display
    strip.show()

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

 # Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

print ('Press Ctrl-C to quit.')
if not args.clear:
    print('Use "-c" argument to clear LEDs on exit')

try:
    while True:
        displayHabitConstellation(strip, hourglass)

except KeyboardInterrupt:
    if args.clear:
        colorWipe(strip, Color(0,0,0), 10)
