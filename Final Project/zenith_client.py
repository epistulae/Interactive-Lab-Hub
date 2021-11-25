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
colors = ['rose', 'fire', 'meadow', 'spring', 'forest', 'ocean', 'aqua', 'royal', 'quartz', 'sakura']
animations = ['twinkle,solid,starlight', 'twinkle,solid,teal_petal', 'twinkle,solid,citrus',
            'twinkle,solid,tropical', 'twinkle,solid,ocean',
            'twinkle,varied,starlight', 'twinkle,varied,teal_petal', 'twinkle,varied,citrus',
            'twinkle,varied,tropical', 'twinkle,varied,ocean',
            'twinkle,syncopated,starlight', 'twinkle,syncopated,teal_petal', 'twinkle,syncopated,citrus',
            'twinkle,syncopated,tropical', 'twinkle,syncopated,ocean',
            'rainbow,solid,rose']

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

        lights_label.set("On" if STATE.lights else "Off")
        lights_button_text.set("Turn Off" if STATE.lights else "Turn On")
        L.configure(bg = "green" if STATE.lights else "red")
        LButton.configure(fg = "red" if STATE.lights else "green")

        h1_label.set("Complete" if STATE.first_habit else "Incomplete")
        h1_button_text.set("Make Incomplete" if STATE.first_habit else "Mark Complete")
        H1.configure(bg = "blue" if STATE.first_habit else "orange")
        H1Button.configure(fg = "orange" if STATE.second_habit else "blue")

        h2_label.set("Complete" if STATE.second_habit else "Incomplete")
        h2_button_text.set("Make Incomplete" if STATE.second_habit else "Mark Complete")
        H2.configure(bg = "blue" if STATE.second_habit else "orange")
        H2Button.configure(fg = "orange" if STATE.second_habit else "blue")
                
    elif incoming_topic == topics[1]:
        STATE.lights = not STATE.lights
        lights_label.set("On" if STATE.lights else "Off")
        lights_button_text.set("Turn Off" if STATE.lights else "Turn On")
        L.configure(bg = "green" if STATE.lights else "red")
        LButton.configure(fg = "red" if STATE.lights else "green")
    
    elif incoming_topic == topics[2]:
        STATE.first_habit = not STATE.first_habit
        h1_label.set("Complete" if STATE.first_habit else "Incomplete")
        h1_button_text.set("Mark Incomplete" if STATE.first_habit else "Mark Complete")
        H1.configure(bg = "blue" if STATE.first_habit else "orange")
        H1Button.configure(fg = "orange" if STATE.first_habit else "blue")
        
    elif incoming_topic == topics[2]:
        STATE.second_habit = not STATE.second_habit
        h2_label.set("Complete" if STATE.second_habit else "Incomplete")
        h2_button_text.set("Mark Incomplete" if STATE.second_habit else "Mark Complete")
        H2.configure(bg = "blue" if STATE.second_habit else "orange")
        H2Button.configure(fg = "orange" if STATE.second_habit else "blue")

def subscribing():
    client.on_message = on_message
    client.loop_start()

def stop():
    client.loop_stop()

def flipLights():
    STATE.lights = not STATE.lights
    client.publish("pi/lights","flip")
    lights_label.set("On" if STATE.lights else "Off")
    lights_button_text.set("Turn Off" if STATE.lights else "Turn On")
    L.configure(bg = "green" if STATE.lights else "red")
    LButton.configure(fg = "red" if STATE.lights else "green")

def flipFirstHabit():
    STATE.first_habit = not STATE.first_habit
    client.publish("pi/habits/first","flip")
    h1_label.set("Complete" if STATE.first_habit else "Incomplete")
    h1_button_text.set("Mark Incomplete" if STATE.first_habit else "Mark Complete")
    H1.configure(bg = "blue" if STATE.first_habit else "orange")
    H1Button.configure(fg = "orange" if STATE.first_habit else "blue")

def flipSecondHabit():
    STATE.second_habit = not STATE.second_habit
    client.publish("pi/habits/second","flip")
    h2_label.set("Complete" if STATE.second_habit else "Incomplete")
    h2_button_text.set("Mark Incomplete" if STATE.second_habit else "Mark Complete")
    H2.configure(bg = "blue" if STATE.second_habit else "orange")
    H2Button.configure(fg = "orange" if STATE.second_habit else "blue")

def stateDisplay(window):
    global L
    global H1
    global H2
    global LButton
    global H1Button
    global H2Button
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
    
    lights_label.set("On" if STATE.lights else "Off")
    lights_button_text.set("Turn Off" if STATE.lights else "Turn On")
    L.configure(bg = "green" if STATE.lights else "red")
    LButton.configure(fg = "red" if STATE.lights else "green")

    h1_label.set("Complete" if STATE.first_habit else "Incomplete")
    h1_button_text.set("Make Incomplete" if STATE.first_habit else "Mark Complete")
    H1.configure(bg = "blue" if STATE.first_habit else "orange")
    H1Button.configure(fg = "orange" if STATE.second_habit else "blue")

    h2_label.set("Complete" if STATE.second_habit else "Incomplete")
    h2_button_text.set("Make Incomplete" if STATE.second_habit else "Mark Complete")
    H2.configure(bg = "blue" if STATE.second_habit else "orange")
    H2Button.configure(fg = "orange" if STATE.second_habit else "blue")
    
def publishColor():
    global color_to_publish
    client.publish("pi/color", color_to_publish)

def publishAnimation():
    global animation_to_publish
    client.publish("pi/animation", animation_to_publish)

def selectColor(window):
    global colors
    global color_to_publish
    selection = tk.Frame(window)
    selection.pack(side=tk.BOTTOM, pady=5)
    
    label = tk.Label(
        selection,
        text = "Select Color:",
        fg = "white",
        bg = "gray",
        width = 20,
        height = 2,
    )
    label.pack(side=tk.LEFT)
    
    color = tk.StringVar(window)
    color.set(colors[0]) # default value
    colorSelect = tk.OptionMenu(
            selection,
            color,
            *colors
    )
    colorSelect.pack(side=tk.LEFT, padx=5)
    color_to_publish = color.get()
    
    go = tk.Button(
            selection,
            text = "Go",
            fg= "black",
            command = publishColor,
    )
    go.pack(side=tk.LEFT)
    
def selectAnimation(window):
    global animations
    global animation_to_publish
    selection = tk.Frame(window)
    selection.pack(side=tk.BOTTOM, pady=5)
    
    label = tk.Label(
        selection,
        text = "Select Animation:",
        fg = "white",
        bg = "gray",
        width = 20,
        height = 2,
    )
    label.pack(side=tk.LEFT)
    
    animation = tk.StringVar(window)
    animation.set(animations[0]) # default value
    aniSelect = tk.OptionMenu(
            selection,
            animation,
            *animations,
    )
    aniSelect.pack(side=tk.LEFT, padx=5)
    animation_to_publish = animation.get()
    
    go = tk.Button(
            selection,
            text = "Go",
            fg= "black",
            command = publishAnimation,
    )
    go.pack(side=tk.LEFT)
    
    
# MQTT setup
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

# Labels and Buttons setup
lights_label = tk.StringVar()
lights_button_text = tk.StringVar()
h1_label = tk.StringVar()
h1_bg = tk.StringVar()
h1_button_text = tk.StringVar()
h2_label = tk.StringVar()
h2_bg = tk.StringVar()
h2_button_text = tk.StringVar()
L = None
H1 = None
H2 = None
LButton = None
H1Button = None
H2Button = None

color_to_publish = ""
animation_to_publish = ""

try:
    # Get current state
    client.publish("pi/habits","info")
    
    # Display Partitions
    stateDisp = tk.Frame(window)
    stateDisp.pack(side = tk.TOP)
    colorSel = tk.Frame(window)
    colorSel.pack(side = tk.TOP)
    aniSel = tk.Frame(window)
    aniSel.pack(side = tk.TOP)
        
    # State
    stateDisplay(stateDisp)

    # Publishers
    selectColor(colorSel)
    selectAnimation(aniSel)
    
    # Display App
    window.mainloop()
    
except KeyboardInterrupt:
    stop()
