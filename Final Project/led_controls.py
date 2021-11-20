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
    sunset = Color(237, 108, 2)
    spring = Color(168, 235, 52)
    forest = Color(27, 153, 23)
    aqua = Color(21, 187, 183)
    royal = Color(98, 0, 255)
    amethyst = Color(168, 57, 237)
    sakura = Color(255, 87, 179)
    
    # Habit colors
    incomplete = Color(230, 21, 83)
    complete = Color(81, 224, 105)
    pinprick = Color(255, 245, 222)
    
    # Lights off
    blank = Color(0, 0, 0)

# All color ranges
# Array in pairs of RGB ranges [r1, r2, g1, g2, b1, b2]
class ColorRanges(Enum):
    rainbow = [0, 256, 0, 256, 0, 256]
    starlight = [255, 256, 195, 241, 64, 65]
    fire = [255, 256, 18, 256, 18, 19]
    ocean = [31, 32, 50, 220, 255, 256]
    mystery = [98, 180, 50, 51, 255, 256]
    
# All color palettes (5 colors)
class ColorPalettes(Enum):
    #[Color(), Color(), Color(), Color(), Color()]
    pink_holiday = [Color(157, 203, 255), Color(191, 226, 254), Color(254, 205, 203), Color(223, 126, 137), Color(141, 28, 26)]

class Animation:
    def __init__(self, name, style, color_range, palette=False, color_palette=None):
        self.name = name
        self.style = style # solid v varied
        self.color_range = color_range #  ColorRanges enum entry name
        self.palette = palette # Whether or not to use color palette instead
        self.color_palette = color_palette # Specific color palette

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

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
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
# x1 to x2 is the range to randomly generate color values.
# randrange generates from x1 (inclusive) upto x2 (exclusive).
# if x2 = x1+1, this the generated value will always be x1
def solidTwinkleRange(strip, leds):
    fastClearDisplay(strip, leds)
    displayPinpricks(strip)

    color_range = ColorRanges[leds.animation.color_range].value
    r1 = color_range[0]
    r2 = color_range[1]
    g1 = color_range[2]
    g2 = color_range[3]
    b1 = color_range[4]
    b2 = lcolor_range[5]
    
    while (leds.mode is 2) and (not leds.intercept):
        randStars = random.sample(Stars.STARS, 20)
        
        red = random.randrange(r1, r2)
        green = random.randrange(g1, g2)
        blue = random.randrange(b1, b2)
        for k in range(256):
            if (leds.mode is 2) and (not leds.intercept):
                r = int((k/256)*red)
                g = int((k/256)*green)
                b = int((k/256)*blue)
                for star in randStars:
                    strip.setPixelColor(star, Color(r, g, b))
                strip.show()
            else:
                break

        if (leds.mode is 2) and (not leds.intercept):
            for k in reversed(range(256)):
                if (leds.mode is 2) and (not leds.intercept):
                    r = int((k/256)*red)
                    g = int((k/256)*green)
                    b = int((k/256)*blue)
                    for star in randStars:
                        strip.setPixelColor(star, Color(r, g, b))
                    strip.show()
                else:
                    break
        else:
            break
    leds.intercept = False

# Varied color twinkle. 
# Stars can have different colors even when showing up at the same time.
# x1 to x2 is the range to randomly generate color values.
# randrange generates from x1 (inclusive) upto x2 (exclusive).
# if x2 = x1+1, this the generated value will always be x1
def variedTwinkleRange(strip, leds):
    fastClearDisplay(strip, leds)
    displayPinpricks(strip)

    color_range = ColorRanges[leds.animation.color_range].value
    r1 = color_range[0]
    r2 = color_range[1]
    g1 = color_range[2]
    g2 = color_range[3]
    b1 = color_range[4]
    b2 = lcolor_range[5]
    
    while (leds.mode is 2) and (not leds.intercept):
        randStars = random.sample(Stars.STARS, 20)
        
        # Generate set of random numbers
        reds = [random.randrange(r1, r2) for _ in range(20)]
        greens = [random.randrange(g1, g2) for _ in range(20)]
        blues = [random.randrange(b1, b2) for _ in range(20)]
        
        for k in range(256):
            if (leds.mode is 2) and (not leds.intercept):
                for i, star in enumerate(randStars):
                    strip.setPixelColor(star, Color(int((k/256)*reds[i]), int((k/256)*greens[i]), int((k/256)*blues[i])))
                strip.show()
            else:
                break

        if (leds.mode is 2) and (not leds.intercept):
            for k in reversed(range(256)):
                if (leds.mode is 2) and (not leds.intercept):
                    for i, star in enumerate(randStars):
                        strip.setPixelColor(star, Color(int((k/256)*reds[i]), int((k/256)*greens[i]), int((k/256)*blues[i])))
                    strip.show()
                else:
                    break
        else:
            break
    leds.intercept = False

def animate(strip, leds):
    if leds.animation.name == "twinkle":
        if leds.animation.style == "solid":
            if leds.animation.palette:
                # Twinkle with color palette
                print("Palette")
            else:
                # Twinkle with range
                t = threading.Thread(target=solidTwinkleRange, args=(strip, leds,))
                t.start()
        elif leds.animation.style == "varied":
            if leds.animation.palette:
                # Twinkle with color palette
                print("Palette")
            else:
                # Twinkle with range
                t = threading.Thread(target=variedTwinkleRange, args=(strip, leds,))
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
        animate(strip, leds)

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
        # Solid: go through Colors enums
        colors = [c.name for c in Colors]
        i = colors.index(leds.color)
        n = (i+1) % (len(colors)-4)
        leds.color = colors[n]
    elif leds.mode is 2:
        # Animated: go through ColorRanges followed by ColorPalettes enums.
        colors = [r.name for r in ColorRanges] + [p.name for p in ColorPalettes]
        n = 0
        if leds.animation.palette:
            # Currently a palette
            i = colors.index(leds.color_palette)
            n = (i+1) % len(colors)
        else:
            # Currently a range
            i = colors.index(leds.color_range)
            n = (i+1) % len(colors)
        
        if n >= len(ColorRanges):
            # New color is a palette
            leds.animation.palette = True
            leds.animation.color_palette = colors[n]
        else:
            # New color is a range
            leds.animation.palette = False
            leds.animation.color_range = colors[n]
            
    
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
    print("Animation Color: " + str(leds.animation.color_range) + " Palette: " + str(leds.animation.palette) + " " + str(leds.animation.color_palette))
    print("Intercept: " + str(leds.intercept))
    print("\n")
