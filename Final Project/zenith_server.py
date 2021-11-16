#!/usr/bin/env python3

import adafruit_mpr121
import argparse
import board
import busio
import led_controls as Leds
from rpi_ws281x import *
import time
import stars as Stars

import paho.mqtt.client as mqtt
import uuid
import multiprocessing

class State:
    def __init__(self):
        self.lights = True # True = on, False = off
        self.day = time.localtime()[2]
        # Habit = 0
	# Mood lighting = 1
	# More can be added. Update mode_count to match and add appropriate handlers.
        self.mode = 0 
        self.mode_count = 2
        self.color = "Rainbow"

# Configs and inits
LED_COUNT      = 200      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

STRIP = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
STRIP.begin()
STATE = State()

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

topic = 'Colors/#'
topic_color = 'Colors/'
topic_mode = 'Mode/'
topic_lights = 'Lights/'

def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe(topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')

# this is the callback that gets called each time a message is recived
def on_message(client, userdata, msg):
	print("topic: " + str(msg.topic) + "msg: " + str(msg.payload.decode('UTF-8')))
	# you can filter by topics
	print(str(msg.topic))
	print(str(str(msg.topic) is "Colors/"))
	if str(msg.topic) is not "Colors/":
		STATE.color = str(msg.payload.decode('UTF-8'))
		print(STATE.color)

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

sub = multiprocessing.Process(target=subscribing, args=())
sub.start()

 # Setup
STRIP = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
STRIP.begin()

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Leds
Leds.displayHabits(STRIP)

try:
    while True:
        # Inputs
        if mpr121[0].value:
            print("Lights on off")
            if STATE.lights:
                print("Closing lights")
                # Close lights
                Leds.colorWipe(STRIP, Color(0,0,0), 10)
                STATE.lights = False
                print("New state: " + str(STATE.lights))
            else:
                # Turn on lights
                print("turning on lights")
                STATE.lights = True
                print("New state: " + str(STATE.lights))
                STATE.mode = 0 # Always turn lights on to habit mode
                Leds.displayHabits(STRIP)
                
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
            Leds.updateStar(STRIP, Stars.HABIT_A.constellations[constellation][star])
            debugHabits()
        elif mpr121[8].value:
            print("Habit B")
            constellation = Stars.HABIT_B.cur_constellation
            star = Stars.HABIT_B.cur_star
            Stars.HABIT_B.constellations[constellation][star].complete = not Stars.HABIT_B.constellations[constellation][star].complete
            Leds.updateStar(STRIP, Stars.HABIT_B.constellations[constellation][star])
            debugHabits()

        nextDay()
        time.sleep(0.5)
    print("outside" + STATE.color)
        
except KeyboardInterrupt:
    sub.terminate()
    Leds.colorWipe(STRIP, Color(0,0,0), 10)
