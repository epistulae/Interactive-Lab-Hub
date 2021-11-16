#!/usr/bin/env python3

import adafruit_mpr121
import argparse
import board
import busio
import habit_controls as Habits
import led_controls as Leds
from rpi_ws281x import *
import time
import stars as Stars

import paho.mqtt.client as mqtt
import uuid
import multiprocessing

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
		Leds.STATE.color = str(msg.payload.decode('UTF-8'))
		print(Leds.STATE.color)

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
Leds.initDisplay(STRIP)

# Main Server, Capacity Inputs
try:
    while True:
        if mpr121[0].value:
            print("Lights on off")
            Leds.lightFlip(STRIP)

        # Assume lights are on
        elif mpr121[5].value:
            # Mode change
            Leds.cycleMode(STRIP)
            print("Mode: " + str(Leds.STATE.mode))
        elif mpr121[2].value:
            print("Habit A")
            Habits.flipFirstHabit(STRIP)
        elif mpr121[8].value:
            print("Habit B")
            Habits.flipSecondHabit(STRIP)
	
        Habits.nextDay()
        time.sleep(0.5)
    print("outside" + Leds.STATE.color)
        
except KeyboardInterrupt:
    sub.terminate()
    Leds.fastClearDisplay(STRIP)
