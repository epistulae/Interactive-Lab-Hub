#!/usr/bin/env python3

import adafruit_mpr121
import argparse
import board
import busio
from enum import Enum
from rpi_ws281x import *
import time

# LED strip configuration:
LED_COUNT      = 200      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class State:
    def __init__(self):
        # True = on, False = off
        self.lights = True
        self.day = time.localtime()[2]

STATE = State()

class Colors(Enum):
    INCOMPLETE = Color(237, 108, 2)
    COMPLETE = Color(20, 164, 217)
    PINPRICK = Color(255, 245, 222)
    RED = Color(235, 52, 52)

# Habit = 0
# Rainbow mood = 1
# Ocean mood = 2
# Cool mood = 3
# Fire mood = 4
MODE_COUNT = 5
MODE = 0 # Always start habit on startup
    
class Star:
    def __init__(self, index, complete=False):
        self.index = index
        self.complete = complete
        # Previous stars: (star, connector)
        self.prior_stars = []

class Habit:
    def __init__(self, constellations):
        self.constellations = constellations
        self.cur_constellation = 0
        self.cur_star = 0
        
pinpricks = [0, 58, 59, 60, 76, 77, 98, 99, 100, 101, 122, 123, 124, 125, 130, 142, 143] 

# Constellation Graphs
hourglass_1 = Star(1)

hourglass_2 = Star(6)
hourglass_2.prior_stars.append((hourglass_1, [2, 3, 4, 5]))

hourglass_3 = Star(10)
hourglass_3.prior_stars.append((hourglass_1, [23, 24]))
hourglass_3.prior_stars.append((hourglass_2, [7, 8, 9]))

hourglass_4 = Star(14)
hourglass_4.prior_stars.append((hourglass_3, [11, 12, 13]))

hourglass_5 = Star(19)
hourglass_5.prior_stars.append((hourglass_3, [20, 21, 22]))
hourglass_5.prior_stars.append((hourglass_4, [15, 16, 17, 18]))

HOURGLASS = [hourglass_1, hourglass_2, hourglass_3, hourglass_4, hourglass_5]

# -------------------------------------------------------

teapot_1 = Star(50)

teapot_2 = Star(46)
teapot_2.prior_stars.append((teapot_1, [47, 48, 49]))

teapot_3 = Star(44)
teapot_3.prior_stars.append((teapot_1, [25,26]))
teapot_3.prior_stars.append((teapot_2, [45]))

teapot_4 = Star(30)
teapot_4.prior_stars.append((teapot_3, [27, 28, 29]))

teapot_5 = Star(33)
teapot_5.prior_stars.append((teapot_3, [41, 42, 43]))
teapot_5.prior_stars.append((teapot_4, [31, 32]))

teapot_6 = Star(35)
teapot_6.prior_stars.append((teapot_5, [34]))

teapot_7 = Star(37)
teapot_7.prior_stars.append((teapot_6, [36]))

teapot_8 = Star(57)
teapot_8.prior_stars.append((teapot_1, [51, 52, 53, 54, 55, 56]))
teapot_8.prior_stars.append((teapot_5, [39, 40]))
teapot_8.prior_stars.append((teapot_7, [38]))

TEAPOT = [teapot_1, teapot_2, teapot_3, teapot_4, teapot_5, teapot_6, teapot_7, teapot_8]

# -------------------------------------------------------

triangle_1 = Star(65)

triangle_2 = Star(61)
triangle_2.prior_stars.append((triangle_1, [62, 63]))

triangle_3 = Star(68)
triangle_3.prior_stars.append((triangle_1, [66, 67]))
triangle_3.prior_stars.append((triangle_2, [69, 70, 71]))

TRIANGLE = [triangle_1, triangle_2, triangle_3]

# -------------------------------------------------------

butterfly_1 = Star(72)

butterfly_2 = Star(97)
butterfly_2.prior_stars.append((butterfly_1, [73]))

butterfly_3 = Star(75)
butterfly_3.prior_stars.append((butterfly_2, [74]))

butterfly_4 = Star(93)
butterfly_4.prior_stars.append((butterfly_2, [94, 95, 96]))
butterfly_4.prior_stars.append((butterfly_3, [78, 79, 80]))

butterfly_5 = Star(87)
butterfly_5.prior_stars.append((butterfly_4, [81, 82, 83, 84, 85, 86]))

butterfly_6 = Star(88)
butterfly_6.prior_stars.append((butterfly_4, [89, 90, 91, 92]))

BUTTERFLY = [butterfly_1, butterfly_2, butterfly_3, butterfly_4, butterfly_5, butterfly_6]

# -------------------------------------------------------

orion_1 = Star(102)

orion_2 = Star(105)
orion_2.prior_stars.append((orion_1, [103, 104]))

orion_3 = Star(108)
orion_3.prior_stars.append((orion_2, [106, 107]))

orion_4 = Star(109)

orion_5 = Star(112)
orion_5.prior_stars.append((orion_1, [110, 111]))

orion_6 = Star(114)
orion_6.prior_stars.append((orion_5, [113]))

orion_7 = Star(116)
orion_7.prior_stars.append((orion_6, [115]))

orion_8 = Star(118)
orion_8.prior_stars.append((orion_7, [117]))
orion_8.prior_stars.append((orion_3, [119, 120, 121]))

ORION = [orion_1, orion_2, orion_3, orion_4, orion_5, orion_6, orion_7, orion_8]

# -------------------------------------------------------

serpens_1 = Star(40)

serpens_2 = Star(37)
serpens_2.prior_stars.append((serpens_1, [138, 139]))

serpens_3 = Star(35)
serpens_3.prior_stars.append((serpens_1, [141]))
serpens_3.prior_stars.append((serpens_2, [136]))

serpens_4 = Star(33)
serpens_4.prior_stars.append((serpens_3, [127, 128]))

serpens_5 = Star(29)
serpens_5.prior_stars.append((serpens_4, [131, 132]))

serpens_6 = Star(26)
serpens_6.prior_stars.append((serpens_5, [127, 128]))

SERPENS = [serpens_1, serpens_2, serpens_3, serpens_4, serpens_5, serpens_6]

# -------------------------------------------------------

narwhale_1 = Star(0)

narwhale_2 = Star(0)

narwhale_3 = Star(0)

narwhale_4 = Star(0)

narwhale_5 = Star(0)

narwhale_6 = Star(0)

NARWHALE = [narwhale_1, narwhale_2, narwhale_3, narwhale_4, narwhale_5, narwhale_6]

# -------------------------------------------------------

draco_1 = Star(0)

draco_2 = Star(0)

draco_3 = Star(0)

draco_4 = Star(0)

draco_5 = Star(0)

draco_6 = Star(0)

draco_7 = Star(0)

draco_8 = Star(0)

draco_9 = Star(0)

draco_10 = Star(0)

draco_11 = Star(0)

draco_12 = Star(0)

draco_13 = Star(144)
draco_13.prior_stars.append((draco_12, [145]))

DRACO = [draco_1, draco_2, draco_3, draco_4, draco_5, draco_6, draco_7, draco_8, draco_9, draco_10, draco_11, draco_12, draco_13]

# -------------------------------------------------------

shield_1 = Star(0)

shield_2 = Star(0)

shield_3 = Star(0)

shield_4 = Star(0)

shield_5 = Star(0)

SHIELD = [shield_1, shield_2, shield_3, shield_4, shield_5]

# Habit Constants
HABIT_A = Habit([SERPENS, BUTTERFLY]) # narwhale, serpens, draco, shield
HABIT_B = Habit([HOURGLASS, TEAPOT, TRIANGLE, ORION, BUTTERFLY])

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
    for led in pinpricks:
        strip.setPixelColor(led, Colors.PINPRICK.value)

    # Habit A
    for constellation in HABIT_A.constellations:
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
    for constellation in HABIT_B.constellations:
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

def displayMode(strip):
    print("Show display mood")
    # All modes have white pinpricks
    if MODE is 0:
        print("Habits Mode")
        displayHabits(strip)
    elif MODE is 1:
        # Rainbow
        print("Rainbow")
    elif MODE is 2:
        # Ocean
        print("Ocean")
    elif MODE is 3:
        # Cool
        print("Cool")
    elif MODE is 4:
        # Fire
        print("Fire")

def nextDay():
    day = time.localtime()[2]
    
    # Debugging
    day = int(input("Enter test date: "))
    
    print("Cur day " + str(STATE.day))
    
    if day is not State.day:
        STATE.day = day
        print("New day " + str(STATE.day))
        # Habit A
        if HABIT_A.cur_star + 1 is len(HABIT_A.constellations[HABIT_A.cur_constellation]):
            # Next constellation (assumes final final star overall, if it was, I'd wipe the state)
            HABIT_A.cur_constellation += 1
        else:
            # Next star
            HABIT_A.cur_star += 1

        # Habit B
        if HABIT_B.cur_star + 1 is len(HABIT_B.constellations[HABIT_B.cur_constellation]):
            # Next constellation (assumes final final star overall, if it was, I'd wipe the state)
            HABIT_B.cur_constellation += 1
        else:
            # Next star
            HABIT_B.cur_star += 1
    
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
def debugHabits():
    print("========================================")
    print("Habits debugging")
    count_c = 0
    for constellation in HABIT_A.constellations:
        print("Habit A Constellation " + str(count_c))
        count_s = 0
        for star in constellation:
            print("Star " + str(count_s) + " complete: " + str(star.complete))
            count_s += 1
        count_c += 1
    for constellation in HABIT_B.constellations:
        print("Habit B Constellation " + str(count_c))
        count_s = 0
        for star in constellation:
            print("Star " + str(count_s) + " complete: " + str(star.complete))
            count_s += 1
        count_c += 1

# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

 # Setup
STRIP = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
STRIP.begin()

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

print ('Press Ctrl-C to quit.')
if not args.clear:
    print('Use "-c" argument to clear LEDs on exit')

# Leds
displayHabits(STRIP)

try:
    while True:
        # Inputs
        if mpr121[0].value:
            print("Lights on off")
            if STATE.lights:
                print("Closing lights")
                # Close lights
                colorWipe(STRIP, Color(0,0,0), 10)
                STATE.lights = False
                print("New state: " + str(STATE.lights))
            else:
                # Turn on lights
                print("turning on lights")
                STATE.lights = True
                print("New state: " + str(STATE.lights))
                MODE = 0 # Always turn lights on to habit mode
                displayHabits(STRIP)
                
        # Assume lights are on
        elif mpr121[5].value:
            # Mode change
            MODE = (MODE + 1) % MODE_COUNT
            displayMode(STRIP)
            print("Mode: " + str(MODE))
        elif mpr121[2].value:
            print("Habit A")
            constellation = HABIT_A.cur_constellation
            star = HABIT_A.cur_star
            HABIT_A.constellations[constellation][star].complete = not HABIT_A.constellations[constellation][star].complete
            updateStar(STRIP, HABIT_A.constellations[constellation][star])
            debugHabits()
        elif mpr121[8].value:
            print("Habit B")
            constellation = HABIT_B.cur_constellation
            star = HABIT_B.cur_star
            HABIT_B.constellations[constellation][star].complete = not HABIT_B.constellations[constellation][star].complete
            updateStar(STRIP, HABIT_A.constellations[constellation][star])
            debugHabits()

        #nextDay()
        if mpr121[11].value:
            nextDay()
            
        time.sleep(0.5)
        
except KeyboardInterrupt:
    if args.clear:
        colorWipe(STRIP, Color(0,0,0), 10)
