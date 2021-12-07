#!/usr/bin/env python3

import habit_controls as Habits
import led_controls as Leds
import stars as Stars

HOST = '10.56.135.100'
PORT = 7827
USER = 'cynthia'
PASS = 'RoomOfRequirement'

DEBUG = False
STRIP = None

leds = Leds.State()
habits = Habits.State()

pinpricks = Stars.PINPRICKS
