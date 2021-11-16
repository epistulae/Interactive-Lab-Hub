#!/usr/bin/env python3

import globals as Globals
import habit_controls as Habits
import led_controls as Leds
import paho.mqtt.client as mqtt
import uuid


HOST = '100.64.1.201'
PORT = 7827
USER = 'cynthia'
PASS = 'RoomOfRequirement'

DEBUG = False
STRIP = None

topics = ["pi/color/", "pi/animation/", "pi/lights/", "pi/habits/", "pi/habits/first", "pi/habits/second", "pi/info"]

def on_connect(client, userdata, flags, rc):
    if DEBUG:
        print("connected with result code " + str(rc))
    for topic in topics:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    incoming_topic = str(msg.topic)
    
    # Color 
    # Input is the same Leds module's Colors enum. 
    # Directly goes to solid color mood mode.
    if incoming_topic == topics[0]:
        Leds.leds.mode = 1
        Leds.leds.color = str(msg.payload.decode('UTF-8'))
        Leds.displayMode(STRIP, DEBUG)

    # Animation
    # Directly goes to animated mood mode.
    elif incoming_topic == topics[1]:
        Leds.leds.mode = 2
        Leds.leds.animation = str(msg.payload.decode('UTF-8'))
        Leds.displayMode(STRIP, DEBUG)
	
    # Lights
    # Any message to the topic means to flip lights.
    elif incoming_topic == topics[2]:
        Leds.lightFlip(STRIP, DEBUG)
	
    # Habits
    # Any message to the topic means to turn on habits.
    elif incoming_topic == topics[3]:
        if Leds.leds.mode is not 0:
            Leds.leds.mode = 0
            Leds.displayMode(STRIP, DEBUG)
        
    # Flip first habit (any message)
    elif incoming_topic == topics[4]:
        Habits.flipFirstHabit(STRIP, DEBUG)

    # Flip second habit (any message)
    elif incoming_topic == topics[5]:
        Habits.flipSecondHabit(STRIP, DEBUG)
    
    # Request remote state data
    elif incoming_topic == topics[6]:
        val = str(int(Leds.leds.lights)) + " " + str(int(Habits.habits.first_complete)) + " " + str(int(Habits.habits.second_complete))
        client.publish('remote/info', val)

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
# client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set(USER, PASS)
client.on_connect = on_connect
client.connect(HOST, port=PORT)

def subscribing():
    client.on_message = on_message
    client.loop_forever()
