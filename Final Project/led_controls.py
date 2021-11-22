#!/usr/bin/env python3

from enum import Enum
import random
from rpi_ws281x import *
import stars as Stars
import time
import threading

# All color values
class Colors(Enum):
    rose = Color(255, 20, 20)
    fire = Color(255, 245, 222)
    meadow = Color(168, 235, 52)
    spring = Color(81, 224, 105)
    forest = Color(27, 153, 23)
    beach = Color(105, 130, 255)
    aqua = Color(21, 187, 183)
    royal = Color(98, 0, 255)
    amethyst = Color(168, 57, 237)
    sakura = Color(255, 87, 179)
    
    # Habit colors
    incomplete = Color(237, 108, 2)
    complete = Color(0, 138, 176)
    pinprick = Color(255, 241, 148)
    
    # Lights off
    blank = Color(0, 0, 0)
    
# All color palettes (5 colors)
# Each color is stored as a (R, G, B) tuple.
class ColorPalettes(Enum):
    #[(), (), (), (), ()]
    teal_petal = [(191, 62, 39), (239, 124, 79), (203, 149, 115), (150, 214, 227), (57, 147, 153)]
    citrus = [(196, 60, 22), (253, 154, 126), (255, 203, 143), (252, 181, 0), (220, 107, 2)]
    tropical = [(255, 106, 0), (255, 202, 42), (102, 176, 22), (155, 216, 218), (188, 206, 209)]
    ocean = [(218, 228, 229), (156, 236, 240), (105, 195, 255), (105, 130, 255), (43, 74, 74)]

class Animation:
    def __init__(self, name, style, palette):
        self.name = name
        self.style = style # solid v varied
        self.palette = palette # Specific color palette

# Tracks state of LED lights
class State:
    def __init__(self):
        self.lights = True # True = on, False = off
        # Habit = 0
        # Mood lighting: Solid = 1
        # Mood lighting: Animated = 2
        self.mode = 0 
        self.mode_count = 3
        self.color = "rose" # Colors enum entry name
        self.animation = Animation("twinkle", "solid", "rainbow")
        self.intercept = False
        
# 
# HABIT MODE FUNCTIONS
#
# Light up LEDs for both habits.
def displayHabits(strip, habits, debug=False):

    # First
    for constellation in habits.first.constellations:
        for star in constellation:
            led_color = Colors.complete.value if star.complete else Colors.incomplete.value
            # Star
            strip.setPixelColor(star.index, led_color)
            update = star.complete 
            # Connectors
            for prior in star.prior_stars:
                if update:
                    led_color = Colors.complete.value if prior[0].complete else Colors.incomplete.value
                leds = prior[1]
                for led in leds:
                    strip.setPixelColor(led, led_color)

    # Second habit
    for constellation in habits.second.constellations:
        for star in constellation:
            led_color = Colors.complete.value if star.complete else Colors.incomplete.value
            # Star
            strip.setPixelColor(star.index, led_color)
            update = star.complete 
            # Connectors
            for prior in star.prior_stars:
                if update:
                    led_color = Colors.complete.value if prior[0].complete else Colors.incomplete.value
                leds = prior[1]
                for led in leds:
                    strip.setPixelColor(led, led_color)
    strip.show()
    
    if debug:
        debugLeds()
        
#
# GENERAL FUNCTIONS
#
# Display just the pinpricks.
def displayPinpricks(strip):
    for led in Stars.PINPRICKS:
        strip.setPixelColor(led, Colors.pinprick.value)
    strip.show()

# Close LEDs in a slow snake. For aestetics.
def slowClearDisplay(strip, leds):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Colors.blank.value)
        strip.show()
        time.sleep(10/1000.0)
    leds.lights = False

# Close LEDs all at once. For debugging.6
def fastClearDisplay(strip, leds):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Colors.blank.value)
    strip.show()
    leds.lights = False
    
#    
# COLORING FUNCTIONS
#
# Define functions which light LEDs in various ways.
def solidColor(strip, leds):
    color = Colors[leds.color].value
    for i in range(strip.numPixels()):
        #if i not in Stars.PINPRICKS:
        strip.setPixelColor(i, color)
    strip.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    # Moving colors 3 steps at a time, one value constant, others moving in opposite directions from 0-255 and 255-0
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, leds, wait_ms=20):
    # Currently changing across all pixels, change this to per constellation
    while (leds.mode is 2) and (not leds.intercept):
        for j in range(256):
            if (leds.mode is 2) and (not leds.intercept):
                for i in range(strip.numPixels()):
                    if leds.mode is 2:
                        strip.setPixelColor(i, wheel((i+j) & 255))
                    else:
                        break
                strip.show()
                time.sleep(wait_ms/1000.0)
            else:
                break
    leds.intercept = False

# Solid color twinkle. 
# Even when we randomize color, at any one time, all stars are the same color.
def solidRainbowTwinkle(strip, leds):
    displayPinpricks(strip)
    
    while (leds.mode is 2) and (not leds.intercept):
        randStars = random.sample(Stars.STARS, 20)
        
        red = random.randrange(256)
        green = random.randrange(256)
        blue = random.randrange(256)
        for k in range(0, 256, 5):
            if (leds.mode is 2) and (not leds.intercept):
                r = int((k/256)*red)
                g = int((k/256)*green)
                b = int((k/256)*blue)
                for star in randStars:
                    strip.setPixelColor(star, Color(r, g, b))
                strip.show()
                time.sleep(20/1000.0)
            else:
                break

        time.sleep(2)
        if (leds.mode is 2) and (not leds.intercept):
            for k in reversed(range(0, 256, 5)):
                if (leds.mode is 2) and (not leds.intercept):
                    r = int((k/256)*red)
                    g = int((k/256)*green)
                    b = int((k/256)*blue)
                    for star in randStars:
                        strip.setPixelColor(star, Color(r, g, b))
                    strip.show()
                    time.sleep(20/1000.0)
                else:
                    break
        else:
            break
    leds.intercept = False

# Varied color twinkle. 
# Stars can have different colors even when showing up at the same time.
def variedRainbowTwinkle(strip, leds):
    displayPinpricks(strip)
    
    while (leds.mode is 2) and (not leds.intercept):
        randStars = random.sample(Stars.STARS, 20)
        
        # Generate set of random numbers
        reds = [random.randrange(256) for _ in range(20)]
        greens = [random.randrange(256) for _ in range(20)]
        blues = [random.randrange(256) for _ in range(20)]
        
        for k in range(0, 256, 5):
            if (leds.mode is 2) and (not leds.intercept):
                for i, star in enumerate(randStars):
                    strip.setPixelColor(star, Color(int((k/256)*reds[i]), int((k/256)*greens[i]), int((k/256)*blues[i])))
                strip.show()
                time.sleep(20/1000.0)
            else:
                break

        time.sleep(2)
        if (leds.mode is 2) and (not leds.intercept):
            for k in reversed(range(0, 256, 5)):
                if (leds.mode is 2) and (not leds.intercept):
                    for i, star in enumerate(randStars):
                        strip.setPixelColor(star, Color(int((k/256)*reds[i]), int((k/256)*greens[i]), int((k/256)*blues[i])))
                    strip.show()
                    time.sleep(20/1000.0)
                else:
                    break
        else:
            break
    leds.intercept = False
    
# Solid color twinkle. 
# Even when we randomize color, at any one time, all stars are the same color.
def solidTwinkle(strip, leds):
    displayPinpricks(strip)

    palette = ColorPalettes[leds.animation.palette].value # len 5
    
    while (leds.mode is 2) and (not leds.intercept):
        randStars = random.sample(Stars.STARS, random.randrange(15,31))
        
        color = palette[random.randrange(5)]
        for k in range(0, 256, 5):
            if (leds.mode is 2) and (not leds.intercept):
                r = int((k/256)*color[0])
                g = int((k/256)*color[1])
                b = int((k/256)*color[2])
                for star in randStars:
                    strip.setPixelColor(star, Color(r, g, b))
                strip.show()
                time.sleep(20/1000.0)
            else:
                break

        time.sleep(2)
        if (leds.mode is 2) and (not leds.intercept):
            for k in reversed(range(0, 256, 5)):
                if (leds.mode is 2) and (not leds.intercept):
                    r = int((k/256)*color[0])
                    g = int((k/256)*color[1])
                    b = int((k/256)*color[2])
                    for star in randStars:
                        strip.setPixelColor(star, Color(r, g, b))
                    strip.show()
                    time.sleep(20/1000.0)
                else:
                    break
        else:
            break
    leds.intercept = False

# Varied color twinkle. 
# Stars can have different colors even when showing up at the same time.
def variedTwinkle(strip, leds):
    displayPinpricks(strip)
    
    palette = ColorPalettes[leds.animation.palette].value # len 5
    
    while (leds.mode is 2) and (not leds.intercept):
        randStars = random.sample(Stars.STARS, 20)
        
        # Star colors, picked from the palette
        colors = [random.choice(palette) for _ in range(20)]
        
        for k in range(0, 256, 5):
            if (leds.mode is 2) and (not leds.intercept):
                for i, star in enumerate(randStars):
                    strip.setPixelColor(star, Color(int((k/256)*colors[i][0]), int((k/256)*colors[i][1]), int((k/256)*colors[i][2])))
                strip.show()
                time.sleep(20/1000.0)
            else:
                break

        time.sleep(2)
        if (leds.mode is 2) and (not leds.intercept):
            for k in reversed(range(0, 256, 5)):
                if (leds.mode is 2) and (not leds.intercept):
                    for i, star in enumerate(randStars):
                        strip.setPixelColor(star, Color(int((k/256)*colors[i][0]), int((k/256)*colors[i][1]), int((k/256)*colors[i][2])))
                    strip.show()
                    time.sleep(20/1000.0)
                else:
                    break
        else:
            break
    leds.intercept = False
    
# Varied color twinkle. 
# Stars can have different colors, showing up a varying times.
def syncopatedTwinkle(strip, leds):
    displayPinpricks(strip)
    
    palette = ColorPalettes[leds.animation.palette].value # len 5
    
    # Initial state
    colors = [random.choice(palette) for _ in range(20)]
    bright = [random.randrange(0, 256, 3) for _ in range(20)]
    randStars = random.sample(Stars.STARS, 20)
    direction = [0 for _ in range(20)]
    
    while (leds.mode is 2) and (not leds.intercept):
        for i, star in enumerate(randStars):
            if (leds.mode is 2) and (not leds.intercept):
                brightness = bright[i]/256
                strip.setPixelColor(star, Color(int(brightness*colors[i][0]), int(brightness*colors[i][1]), int(brightness*colors[i][2])))
                if direction[i] is 0:
                    # Increment
                    if bright[i] is 200:
                        direction[i] = 1
                        bright[i] -= 3
                    else:
                        bright[i] += 3
                        if bright[i] > 200:
                            bright[i] = 200
                else:
                    if bright[i] is 0:
                        direction[i] = 0
                        bright[i] += 3
                    else:
                        bright[i] -= 3
                        if bright[i] <= 0:
                            # New star
                            bright[i] = 0
                            randStars[i] = random.choice(list(set(Stars.STARS) - set(randStars)))
                            colors[i] = random.choice(palette)
            else:
                break
        strip.show()
        time.sleep(40/1000.0)
    leds.intercept = False

# def solidFade(strip, leds, habits):
#     displayPinpricks(strip)
    
#     palette = ColorPalettes[leds.animation.palette].value
#     all_constellations = habits.first.constellations + habits.second.constellations
    
#     while (leds.mode is 2) and (not leds.intercept):
#         colors = random.choice(palette)
#         for k in range(0, 256, 5):
#             if (leds.mode is 2) and (not leds.intercept):
#                 for constellation in all_constellations:
#                     led_color = Color(int((k/256)*colors[0]), int((k/256)*colors[1]), int((k/256)*colors[2]))
#                     for star in constellation:
#                         strip.setPixelColor(star.index, led_color)
#                         # Connectors
#                         for prior in star.prior_stars:
#                             connectors = prior[1]
#                             for pixel in connectors:
#                                 strip.setPixelColor(pixel, led_color)
#                 strip.show()
#                 time.sleep(20/1000.0)
#             else:
#                 break
        
#         time.sleep(2)
#         if (leds.mode is 2) and (not leds.intercept):
#             for k in reversed(range(0, 256, 5)):
#                 if (leds.mode is 2) and (not leds.intercept):
#                     for i, constellation in enumerate(all_constellations):
#                         led_color = Color(int((k/256)*colors[0]), int((k/256)*colors[1]), int((k/256)*colors[2]))
#                         for star in constellation:
#                             strip.setPixelColor(star.index, led_color)
#                             # Connectors
#                             for prior in star.prior_stars:
#                                 connectors = prior[1]
#                                 for pixel in connectors:
#                                     strip.setPixelColor(pixel, led_color)
#                     strip.show()
#                     time.sleep(20/1000.0)
#                 else:
#                     break
#         else:
#             break
#     leds.intercept = False

def animate(strip, leds, habits):
    if leds.animation.name == "twinkle":
        if leds.animation.style == "solid":
            if leds.animation.palette == "rainbow":
                # Rainbow twinkle
                t = threading.Thread(target=solidRainbowTwinkle, args=(strip, leds,))
                t.start()
            else:
                # Palette Twinkle
                t = threading.Thread(target=solidTwinkle, args=(strip, leds,))
                t.start()
        elif leds.animation.style == "varied":
            if leds.animation.palette == "rainbow":
                # Rainbow twinkle
                t = threading.Thread(target=variedRainbowTwinkle, args=(strip, leds,))
                t.start()
            else:
                # Palette Twinkle
                t = threading.Thread(target=variedTwinkle, args=(strip, leds,))
                t.start()
        elif leds.animation.style == "syncopated":
            t = threading.Thread(target=syncopatedTwinkle, args=(strip, leds,))
            t.start()
    elif leds.animation.name == "rainbow":
        t = threading.Thread(target=rainbow, args=(strip, leds,))
        t.start()

#
# EXTERNAL FUNCTIONS
#
# Habit = 0
# Mood lighting: Solid = 1
# Mood lighting: Animated = 2
# More can be added. Update mode_count to match and add appropriate handler here.
def displayMode(strip, leds, habits, debug=False):
    # All modes have white pinpricks.
    leds.lights = True
    displayPinpricks(strip)
    if leds.mode is 0:
        displayHabits(strip, habits)
    elif leds.mode is 1:
        solidColor(strip, leds)
    elif leds.mode is 2:
        animate(strip, leds, habits)

    if debug:
        debugLeds(leds)

# Cycle through available modes. 
def cycleMode(strip, leds, habits, debug=False):
    # All modes have white pinpricks.
    leds.mode = (leds.mode + 1) % leds.mode_count
    displayMode(strip, leds, habits, debug)
    
# Cycle through available colors for current mode. 
def cycleColor(strip, leds, habits, debug=False):
    if leds.mode is 1:
        # Solid: go through Colors enum
        colors = [c.name for c in Colors]
        i = colors.index(leds.color)
        n = (i+1) % (len(colors)-4)
        leds.color = colors[n]
    elif leds.mode is 2:
        # Animated: go through ColorPalettes enum
        colors = [p.name for p in ColorPalettes]
        new_color = ""
        if leds.animation.palette == "rainbow":
            new_color = colors[0]
        else:
            i = colors.index(leds.animation.palette)
            if i < (len(colors)-1):
                new_color = colors[i+1]
            else:
                new_color = "rainbow"
        leds.animation.palette = new_color
    
    displayMode(strip, leds, habits, debug)

# Start display.
def initDisplay(strip, leds, habits, debug=False):
    displayPinpricks(strip)
    displayMode(strip, leds, habits, debug)
    leds.lights = True

# Switch LED display on and off.
def lightFlip(strip, leds, habits, debug=False):
    if leds.lights:
        # Close lights
        fastClearDisplay(strip, leds)
    else:
        # Turn on lights
        initDisplay(strip, leds, habits, debug)
        
    if debug:
        debugLeds(leds)

def debugLeds(leds):
    print("========================================")
    print("LEDs Debugging")
    print("========================================")
    print("Light on: " + str(leds.lights))
    print("Mode: " + str(leds.mode))
    print("Color: " + str(leds.color))
    print("Animation: " + str(leds.animation.name) + " " + str(leds.animation.style))
    print("Animation Palette: " + str(leds.animation.palette))
    print("Intercept: " + str(leds.intercept))
    print("\n")
