#!/usr/bin/env python3

import global_vars as Globals
import habit_controls as Habits
import led_controls as Leds
import paho.mqtt.client as mqtt
import time
import uuid

topics = ["pi/color/", "pi/animation/", "pi/lights/", "pi/habits/", "pi/habits/first", "pi/habits/second", "pi/debug/nextday"]

def on_connect(client, userdata, flags, rc):
    if Globals.DEBUG:
        print("connected with result code " + str(rc))
    for topic in topics:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    incoming_topic = str(msg.topic)
    message = str(msg.payload.decode('UTF-8'))
    
    # Color 
    # Input is the same Leds module's Colors enum. 
    # Directly goes to solid color mood mode.
    if incoming_topic == topics[0]:
        Globals.leds.mode = 1
        Globals.leds.color = message
        Leds.displayMode(Globals.STRIP, Globals.leds, Globals.pinpricks, Globals.DEBUG)

    # Animation
    # Directly goes to animated mood mode.
    elif incoming_topic == topics[1]:
	Leds.fastClearDisplay(Globals.STRIP, Globals.leds)
	Globals.leds.lights = True

        # Already animating
        if Globals.leds.mode is 2:
            Globals.leds.intercept = True

        Globals.leds.mode = 2
        animation_vars = message.split(",")
        Globals.leds.animation = Leds.Animation(animation_vars[0], animation_vars[1], animation_vars[2])

        Leds.displayMode(Globals.STRIP, Globals.leds, Globals.pinpricks, Globals.DEBUG)
	
    # Lights
    # Any message to the topic means to flip lights.
    elif incoming_topic == topics[2]:
        if (Globals.leds.mode is 2) and Globals.leds.lights:
            Globals.leds.intercept = True
            time.sleep(5)
        Leds.lightFlip(Globals.STRIP, Globals.leds, Globals.DEBUG)
	
    # Habits
    # Any message to the topic means to turn on habits.
    elif incoming_topic == topics[3]:
        if message == "info":
            # Request habit state data
            val = str(int(Globals.leds.lights)) + " " + str(int(Globals.habits.first_complete)) + " " + str(int(Globals.habits.second_complete))
            client.publish('remote/habits/info', val)
        elif Leds.leds.mode is not 0:
            Globals.leds.mode = 0
            Leds.displayMode(Globals.STRIP, Globals.leds, Globals.pinpricks, Globals.DEBUG)
        
    # First habit
    elif incoming_topic == topics[4]:
        if message == "flip":
            Habits.flipFirstHabit(Globals.STRIP, Globals.habits, Globals.leds, Globals.DEBUG)
        elif message == "clear":
            Habits.resetFirstHabit(Globals.STRIP, Globals.habits, Globals.leds, Globals.DEBUG)

    # Second habit
    elif incoming_topic == topics[5]:
        if message == "flip":
            Habits.flipSecondHabit(Globals.STRIP, Globals.habits, Globals.leds, Globals.DEBUG)
        elif message == "clear":
            Habits.resetSecondHabit(Globals.STRIP, Globals.habits, Globals.leds, Globals.DEBUG)  
        
    # Next day for debugging only
    elif incoming_topic == topics[6]:
        Habits.debugToNextDay(Globals.habits)
        
client = mqtt.Client(str(uuid.uuid1()))
# client.tls_set()
client.username_pw_set(Globals.USER, Globals.PASS)
client.on_connect = on_connect
client.connect(Globals.HOST, port=Globals.PORT)

def subscribing():
    client.on_message = on_message
    client.loop_start()

def stop():
    client.loop_stop()
