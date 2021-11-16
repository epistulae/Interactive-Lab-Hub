#!/usr/bin/env python3

from enum import Enum
from rpi_ws281x import *
import stars as Stars
import time

import habit_controls as Habits

class State:
    def __init__(self):
        self.lights = True # True = on, False = off
        # Habit = 0
	    # Mood lighting = 1
	    # More can be added. Update mode_count to match and add appropriate handlers.
        self.mode = 0 
        self.mode_count = 2
        self.color = "Rainbow"

STATE = State()
        
class Colors(Enum):
    INCOMPLETE = Color(237, 108, 2)
    COMPLETE = Color(20, 164, 217)
    PINPRICK = Color(255, 245, 222)
    RED = Color(235, 52, 52)

#
#    
# HABIT MODE FUNCTIONS
#
#
def updateStar(strip, star):
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
    strip.show()

# Show state of habits
def displayHabits(strip):
    for led in Stars.PINPRICKS:
        strip.setPixelColor(led, Colors.PINPRICK.value)

    star_count = 1
    # Habit A
    for constellation in Stars.HABIT_A.constellations:
        for star in constellation:
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

    # Habit B
    for constellation in Stars.HABIT_B.constellations:
        for star in constellation:
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

def initDisplay(strip):
	# Display always inits to display habits.
    STATE.mode = 0
    displayHabits(strip)
    STATE.lights = True
    
def slowClearDisplay(strip):
    blank = Color(0,0,0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, blank)
        strip.show()
        time.sleep(10/1000.0)
    STATE.lights = False

def fastClearDisplay(strip):
    blank = Color(0,0,0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, blank)
    strip.show()
    STATE.lights = False
