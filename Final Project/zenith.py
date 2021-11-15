#!/usr/bin/env python3

import adafruit_mpr121
import argparse
import board
import busio
from enum import Enum
from rpi_ws281x import *
import time
import stars as Stars

import paho.mqtt.client as mqtt
import uuid

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
        self.lights = True # True = on, False = off
        self.day = time.localtime()[2]
        # Habit = 0
        # Rainbow mood = 1
        # Ocean mood = 2
        # Cool mood = 3
        # Fire mood = 4
        self.mode = 0 
        self.mode_count = 5

STATE = State()

class Colors(Enum):
    INCOMPLETE = Color(237, 108, 2)
    COMPLETE = Color(20, 164, 217)
    PINPRICK = Color(255, 245, 222)
    RED = Color(235, 52, 52)
    
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

def displayMode(strip):
    print("Show display mood")
    # All modes have white pinpricks
    if STATE.mode is 0:
        print("Habits Mode")
        displayHabits(strip)
    elif STATE.mode is 1:
        # Rainbow
        print("Rainbow")
    elif STATE.mode is 2:
        # Ocean
        print("Ocean")
    elif STATE.mode is 3:
        # Cool
        print("Cool")
    elif STATE.modeE is 4:
        # Fire
        print("Fire")

def nextDay():
    day = time.localtime()[2]
    
    if day is not STATE.day:
        STATE.day = day
        # Habit A
        if Stars.HABIT_A.cur_star + 1 is len(Stars.HABIT_A.constellations[Stars.HABIT_A.cur_constellation]):
            # Next constellation (assumes not final star overall, if it was, I'd wipe the state)
            Stars.HABIT_A.cur_constellation += 1
            Stars.HABIT_A.cur_star = 0
        else:
            # Next star
            Stars.HABIT_A.cur_star += 1

        # Habit B
        if Stars.HABIT_B.cur_star + 1 is len(Stars.HABIT_B.constellations[Stars.HABIT_B.cur_constellation]):
            # Next constellation (assumes not final star overall, if it was, I'd wipe the state)
            Stars.HABIT_B.cur_constellation += 1
            Stars.HABIT_B.cur_star = 0
        else:
            # Next star
            Stars.HABIT_B.cur_star += 1
    
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
    for constellation in Stars.HABIT_A.constellations:
        print("Habit A Constellation " + str(count_c))
        count_s = 0
        for star in constellation:
            print("Star " + str(count_s) + " complete: " + str(star.complete))
            count_s += 1
        count_c += 1
    count_c = 0
    for constellation in Stars.HABIT_B.constellations:
        print("Habit B Constellation " + str(count_c))
        count_s = 0
        for star in constellation:
            print("Star " + str(count_s) + " complete: " + str(star.complete))
            count_s += 1
        count_c += 1

# the # wildcard means we subscribe to all subtopics of IDD
topic = 'Colors/#'

def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe(topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(client, userdata, msg):
	print("topic: " + str(msg.topic) + "msg: " + str(msg.payload.decode('UTF-8'))")
	# you can filter by topics
	# if msg.topic == 'IDD/some/other/topic': do thing


# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
# client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('cynthia', 'RoomOfRequirement')
client.on_connect = on_connect
client.connect(
    '100.64.1.201',
    port=7827)

def subscribing():
    client.on_message = on_message
    client.loop_forever()

sub=threading.Thread(target=subscribing)
sub.start()

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
                STATE.mode = 0 # Always turn lights on to habit mode
                displayHabits(STRIP)
                
        # Assume lights are on
        elif mpr121[5].value:
            # Mode change
            STATE.mode = (STATE.mode + 1) % STATE.mode_count
            displayMode(STRIP)
            print("Mode: " + str(STATE.mode))
        elif mpr121[2].value:
            print("Habit A")
            constellation = Stars.HABIT_A.cur_constellation
            star = Stars.HABIT_A.cur_star
            Stars.HABIT_A.constellations[constellation][star].complete = not Stars.HABIT_A.constellations[constellation][star].complete
            updateStar(STRIP, Stars.HABIT_A.constellations[constellation][star])
            debugHabits()
        elif mpr121[8].value:
            print("Habit B")
            constellation = Stars.HABIT_B.cur_constellation
            star = Stars.HABIT_B.cur_star
            Stars.HABIT_B.constellations[constellation][star].complete = not Stars.HABIT_B.constellations[constellation][star].complete
            updateStar(STRIP, Stars.HABIT_B.constellations[constellation][star])
            debugHabits()

        nextDay()
        time.sleep(0.5)
        
except KeyboardInterrupt:
    if args.clear:
        colorWipe(STRIP, Color(0,0,0), 10)
