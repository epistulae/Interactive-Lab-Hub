#!/usr/bin/env python3

import habit_controls as Habits
import led_controls as Leds

HOST = '100.64.1.201'
PORT = 7827
USER = 'cynthia'
PASS = 'RoomOfRequirement'

DEBUG = False
STRIP = None

leds = Leds.leds
habits = Habits.habits
