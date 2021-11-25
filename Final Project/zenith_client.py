#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import uuid
import time
import tkinter as tk

HOST = '100.64.1.201'
PORT = 7827
USER = 'cynthia'
PASS = 'RoomOfRequirement'

topics = ['remote/habits/info', 'remote/lights', 'remote/habits/first', 'remote/habits/second']

class State:
    def __init__(self, lights=True, first_habit=False, second_habit=False):
        self.lights = lights
        # Habit state for today
        self.first_habit = first_habit
        self.second_habit = second_habit

def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    for topic in topics:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    incoming_topic = str(msg.topic)
    message = str(msg.payload.decode('UTF-8'))

    if incoming_topic == topics[0]:
        info = message.split(",")
        STATE.lights = bool(int(info[0]))
        STATE.first_habit = bool(int(info[1]))
        STATE.second_habit = bool(int(info[2]))
        
        print(str(STATE.lights))
        print(str(STATE.first_habit))
        print(str(STATE.second_habit))

        lights_label.set("On" if STATE.lights else "Off")
        lights_button_text.set("Turn Off" if STATE.lights else "Turn On")

        h1_label.set("Complete" if STATE.first_habit else "Incomplete")
        h1_button_text.set("Make Incomplete" if STATE.first_habit else "Mark Complete")

        h2_label.set("Complete" if STATE.second_habit else "Incomplete")
        h2_button_text.set("Make Incomplete" if STATE.second_habit else "Mark Complete")
                
    elif incoming_topic == topics[1]:
        print("Lights flipped")
        STATE.lights = not STATE.lights
    
    elif incoming_topic == topics[2]:
        print("habit first flipped")
        STATE.first_habit = not STATE.first_habit
        
    elif incoming_topic == topics[2]:
        print("habit second flipped")
        STATE.second_habit = not STATE.second_habit

def subscribing():
    client.on_message = on_message
    client.loop_start()

def stop():
    client.loop_stop()

def flipLights():
    STATE.lights = not STATE.lights
    client.publish("pi/lights","flip")

def flipFirstHabit():
    STATE.first_habit = not STATE.first_habit
    client.publish("pi/habits/first","flip")

def flipSecondHabit():
    STATE.second_habit = not STATE.second_habit
    client.publish("pi/habits/second","flip")

def stateDisplay(window):
    lights = tk.Frame(window)
    lights.pack(side=tk.LEFT, padx=5, pady=5)

    h1 = tk.Frame(window)
    h1.pack(side=tk.LEFT, padx=5, pady=5)

    h2 = tk.Frame(window)
    h2.pack(side=tk.LEFT, padx=5, pady=5)

    heading0 = tk.Label(
            lights,
            text = "Lights",
            fg = "white",
            bg = "gray",
            width = 20,
            height = 2,
    )
    heading0.pack(side=tk.TOP)
    heading1 = tk.Label(
            h1,
            text = "First Habit",
            fg = "white",
            bg = "gray",
            width = 26,
            height = 2,
    )
    heading1.pack(side=tk.TOP)
    heading2 = tk.Label(
            h2,
            text = "Second Habit",
            fg = "white",
            bg = "gray",
            width = 26,
            height = 2,
    )
    heading2.pack(side=tk.TOP)

    L = tk.Label(
            lights,
            textvariable = lights_label,
            fg = "white",
            bg = "gray",
            width = 10,
            height = 5,
    )
    L.pack(side=tk.LEFT)
    H1 = tk.Label(
            h1,
            textvariable = h1_label,
            fg = "white",
            bg = "gray",
            width = 10,
            height = 5,
    )
    H1.pack(side=tk.LEFT)
    H2 = tk.Label(
            h2,
            textvariable = h2_label,
            fg = "white",
            bg = "gray",
            width = 10,
            height = 5,
    )
    H2.pack(side = tk.LEFT)

    LButton = tk.Button(
            lights,
            textvariable = lights_button_text,
            fg = "black",
            command = flipLights,
    )
    LButton.pack(side=tk.LEFT)

    H1Button = tk.Button(
            h1,
            textvariable = h1_button_text,
            fg= "black",
            command = flipFirstHabit,
    )
    H1Button.pack(side=tk.LEFT)

    H2Button = tk.Button(
            h2,
            textvariable = h2_button_text,
            fg= "black",
            command = flipSecondHabit,
    )
    H2Button.pack(side=tk.LEFT)

STATE = State()
client = mqtt.Client(str(uuid.uuid1()))
client.username_pw_set(USER, PASS)
client.on_connect = on_connect
client.connect(HOST, port=PORT)

# Spawn listener
subscribing()

# Display setup
window = tk.Tk()
window.geometry("700x350")
lights_label = tk.StringVar()
lights_button_text = tk.StringVar()
h1_label = tk.StringVar()
h1_bg = tk.StringVar()
h1_button_text = tk.StringVar()
h2_label = tk.StringVar()
h2_bg = tk.StringVar()
h2_button_text = tk.StringVar()

lights_label.set("On" if STATE.lights else "Off")
lights_button_text.set("Turn Off" if STATE.lights else "Turn On")
h1_label.set("Complete" if STATE.first_habit else "Incomplete")
h1_button_text.set("Make Incomplete" if STATE.first_habit else "Mark Complete")
h2_label.set("Complete" if STATE.first_habit else "Incomplete")
h2_button_text.set("Make Incomplete" if STATE.first_habit else "Mark Complete")

try:
    # Get current state
    client.publish("pi/habits","info")
    
    # State display
    stateDisplay(window)

    # Publishers
    print("publishers")
    
    window.mainloop()
    
except KeyboardInterrupt:
    stop()
