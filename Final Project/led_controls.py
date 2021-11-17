#!/usr/bin/env python3

from enum import Enum
from rpi_ws281x import *
import stars as Stars
import time

# Tracks state of LED lights
class State:
    def __init__(self):
        self.lights = True # True = on, False = off
        # Habit = 0
        # Mood lighting: Solid = 1
        # Mood lighting: Animated = 2
        self.mode = 0 
        self.mode_count = 3
        self.color = "rose"
        self.animation = "cool"

# All color values
class Colors(Enum):
    incomplete = Color(219, 150, 0)
    complete = Color(20, 164, 217)
    pinprick = Color(255, 245, 222)
    rose = Color(255, 20, 20)
    sunset = Color(237, 108, 2)
    creamsicle = Color(235, 137, 52)
    buttercup = Color(255, 191, 28)
    spring = Color(168, 235, 52)
    forest = Color(27, 153, 23)
    aqua = Color(21, 187, 183)
    royal = Color(98, 0, 255)
    amethyst = Color(168, 57, 237)
    sakura = Color(245, 120, 189)
    blank = Color(0, 0, 0)

# 
# HABIT MODE FUNCTIONS
#
# Light up LEDs for both habits.
def displayHabits(strip, habits, debug=False):

    # First
    for constellation in habits.first.constellations:
        for star in constellation:
            led_color = Colors.complete.value if star.complete else Colors.incomplete.value
            # Star
            strip.setPixelColor(star.index, led_color)
            update = star.complete 
            # Connectors
            for prior in star.prior_stars:
                if update:
                    led_color = Colors.complete.value if prior[0].complete else Colors.incomplete.value
                leds = prior[1]
                for led in leds:
                    strip.setPixelColor(led, led_color)

    # Second habit
    for constellation in habits.second.constellations:
        for star in constellation:
            led_color = Colors.complete.value if star.complete else Colors.incomplete.value
            # Star
            strip.setPixelColor(star.index, led_color)
            update = star.complete 
            # Connectors
            for prior in star.prior_stars:
                if update:
                    led_color = Colors.complete.value if prior[0].complete else Colors.incomplete.value
                leds = prior[1]
                for led in leds:
                    strip.setPixelColor(led, led_color)
    strip.show()
    
    if debug:
        debugLeds()
    
#    
# COLORING FUNCTIONS
#
# Define functions which light LEDs in various ways.
def solidColor(strip, leds):
    color = Colors[leds.color].value
    for i in range(strip.numPixels()):
        #if i not in Stars.PINPRICKS:
        strip.setPixelColor(i, color)
    strip.show()

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

#
# GENERAL FUNCTIONS
#
# Display just the pinpricks.
def displayPinpricks(strip):
    for led in Stars.PINPRICKS:
        strip.setPixelColor(led, Colors.pinprick.value)
    strip.show()

# Close LEDs in a slow snake. For aestetics.
def slowClearDisplay(strip, leds):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Colors.blank.value)
        strip.show()
        time.sleep(10/1000.0)
    leds.lights = False

# Close LEDs all at once. For debugging.6
def fastClearDisplay(strip, leds):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Colors.blank.value)
    strip.show()
    leds.lights = False

# Habit = 0
# Mood lighting: Solid = 1
# Mood lighting: Animated = 2
# More can be added. Update mode_count to match and add appropriate handler here.
def displayMode(strip, leds, habits, debug=False):
    # All modes have white pinpricks.
    leds.lights = True
    displayPinpricks(strip)
    if leds.mode is 0:
        displayHabits(strip, habits)
    elif leds.mode is 1:
        solidColor(strip, leds)
    elif leds.mode is 2:
        A = 1

    if debug:
        debugLeds(leds)

# Cycle through available modes. 
def cycleMode(strip, leds, habits, debug=False):
    # All modes have white pinpricks.
    leds.mode = (leds.mode + 1) % leds.mode_count
    displayMode(strip, leds, habits, debug)

# Start display.
def initDisplay(strip, leds, habits, debug=False):
    displayPinpricks(strip)
    displayMode(strip, leds, habits, debug)
    leds.lights = True

# Switch LED display on and off.
def lightFlip(strip, leds, habits, debug=False):
    if leds.lights:
        # Close lights
        fastClearDisplay(strip, leds)
    else:
        # Turn on lights
        initDisplay(strip, leds, habits, debug)
        
    if debug:
        debugLeds(leds)

def debugLeds(leds):
    print("========================================")
    print("LEDs Debugging")
    print("========================================")
    print("Light on: " + str(leds.lights))
    print("Mode: " + str(leds.mode))
    print("Color: " + str(leds.color))
    print("Animation: " + str(leds.animation))
    print("\n")
