#!/usr/bin/env python3

import adafruit_mpr121
import argparse
import board
import busio
import global_vars as Globals
import habit_controls as Habits
import led_controls as Leds
import mqtt_controls as Mqtt
import multiprocessing
from rpi_ws281x import *
import time

# Configs and inits
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='print debugging statements')
args = parser.parse_args()

if args.debug:
    Globals.DEBUG = True

LED_COUNT      = 229      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

STRIP = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
STRIP.begin()
Globals.STRIP = STRIP

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Spawns listener thread
Mqtt.subscribing()

#
# Main Server: Capacity Inputs
#
try:
    Leds.initDisplay(Globals.STRIP, Globals.leds, Globals.habits)
    while True:
        if mpr121[0].value:
            Leds.lightFlip(Globals.STRIP, Globals.leds, Globals.habits, Globals.DEBUG)
            Mqtt.client.publish('remote/lights', "0")
        elif mpr121[5].value:
            Leds.cycleMode(Globals.STRIP, Globals.leds, Globals.habits, Globals.DEBUG)
        elif mpr121[11].value:
            Leds.cycleColor(Globals.STRIP, Globals.leds, Globals.habits, Globals.DEBUG)
        elif mpr121[2].value:
            Habits.flipFirstHabit(Globals.STRIP, Globals.habits, Globals.leds, Globals.DEBUG)
            Mqtt.client.publish('remote/habits/first', "0")
        elif mpr121[8].value:
            Habits.flipSecondHabit(Globals.STRIP, Globals.habits, Globals.leds, Globals.DEBUG)
            Mqtt.client.publish('remote/habits/second', "0")

        Habits.nextDay(Globals.habits)
        time.sleep(0.5) # Prevent multiple triggers for one touch
        
except KeyboardInterrupt:
    Mqtt.stop()
    Leds.slowClearDisplay(STRIP, Globals.leds)
