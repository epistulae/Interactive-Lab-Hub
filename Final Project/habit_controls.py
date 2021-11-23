#!/usr/bin/env python3

import led_controls as Leds
import stars as Stars
import time

# Track state of habits
class State:
    def __init__(self):
        self.day = time.localtime()[2]
        self.tracking_day = 0
        self.first = Stars.FIRST
        self.second = Stars.SECOND
        self.first_complete = False
        self.second_complete = False

def readInput(habits, day, first, second):
    habits.tracking_day = day
    unset = True
    for i, constellation in enumerate(habits.first.constellations):
        if day > len(constellation):
            day = day - len(constellation)
        else:
            if unset:
                habits.first.cur_constellation = i
                habits.first.cur_star = day-1
        for star in constellation:
            star.complete = bool(first.pop(0))
            
    day = habits.tracking_day
    unset = True
    for i, constellation in enumerate(habits.second.constellations):
        if day > len(constellation):
            day = day - len(constellation)
        else:
            if unset:
                habits.second.cur_constellation = i
                habits.second.cur_star = day-1
        for star in constellation:
            star.complete = bool(second.pop(0))
    
# Flip completeness for today's tracking of the first habit.
def flipFirstHabit(strip, habits, leds, debug=False):
    if not leds.lights:
        leds.lights = True
    if leds.mode is not 0:
        leds.mode = 0
    habits.first_complete = not habits.first_complete
    constellation = habits.first.cur_constellation
    star = habits.first.cur_star
    habits.first.constellations[constellation][star].complete = not habits.first.constellations[constellation][star].complete
    Leds.displayHabits(strip, habits)
    if debug:
        debugHabits(habits)

# Flip completeness for today's tracking of the second habit.
def flipSecondHabit(strip, habits, leds, debug=False):
    if not leds.lights:
        leds.lights = True
    if leds.mode is not 0:
        leds.mode = 0
    habits.second_complete = not habits.second_complete
    constellation = habits.second.cur_constellation
    star = habits.second.cur_star
    habits.second.constellations[constellation][star].complete = not habits.second.constellations[constellation][star].complete
    Leds.displayHabits(strip, habits)
    if debug:
        debugHabits(habits)
        
def resetFirstHabit(strip, habits, leds, debug=False):
    for constellation in habits.second.constellations:
        for star in constellation:
            star.complete = False
    Leds.displayHabits(strip, habits)
    if debug:
        debugHabits(habits)
    
def resetSecondHabit(strip, habits, leds, debug=False):
    for constellation in habits.second.constellations:
        for star in constellation:
            star.complete = False
    Leds.displayHabits(strip, habits)
    if debug:
        debugHabits(habits)

# Check whether or not it's a new day and update the state if it is.
def nextDay(habits):
    day = time.localtime()[2]

    if day is not habits.day:
        habits.day = day
        habits.tracking_day += 1
        # Habit A
        if habits.first.cur_star + 1 is len(habits.first.constellations[habits.first.cur_constellation]):
            # Next constellation (assumes not final star overall, if it was, I'd wipe the state)
            habits.first.cur_constellation += 1
            habits.first.cur_star = 0
        else:
            # Next star
            habits.first.cur_star += 1

        # Habit B
        if habits.second.cur_star + 1 is len(habits.second.constellations[habits.second.cur_constellation]):
            # Next constellation (assumes not final star overall, if it was, I'd wipe the state)
            habits.second.cur_constellation += 1
            habits.second.cur_star = 0
        else:
            # Next star
            habits.second.cur_star += 1
        
        # Save to file once per day
        tracking_file = open("tracking.txt","w")
        tracking_file.write(str(habits.tracking_day)+"\n")
        first = []
        for constellation in habits.first.constellations:
            first += [int(star.complete) for star in constellation]
        tracking_file.write(' '.join([str(star) for star in first])+"\n")
        second = []
        for constellation in habits.second.constellations:
            second += [int(star.complete) for star in constellation]
        tracking_file.write(' '.join([str(star) for star in second])+"\n")

def debugToNextDay(habits):
    habits.day = habits.day + 1
    print(str(habits.day))
    # Habit A
    if habits.first.cur_star + 1 is len(habits.first.constellations[habits.first.cur_constellation]):
        # Next constellation (assumes not final star overall, if it was, I'd wipe the state)
        habits.first.cur_constellation += 1
        habits.first.cur_star = 0
    else:
        # Next star
        habits.first.cur_star += 1

    # Habit B
    if habits.second.cur_star + 1 is len(habits.second.constellations[habits.second.cur_constellation]):
        # Next constellation (assumes not final star overall, if it was, I'd wipe the state)
        habits.second.cur_constellation += 1
        habits.second.cur_star = 0
    else:
        # Next star
        habits.second.cur_star += 1
    
def debugHabits(habits):
    print("========================================")
    print("Habits Debugging")
    print("========================================")
    
    print("First Habit:")
    habit_star = 0
    count_c = 0
    for constellation in habits.first.constellations:
        print("Constellation " + str(count_c))
        count_s = 0
        for star in constellation:
            print("Habit star: " + str(habit_star) + " | Constellation star: " + str(count_s) + " | Complete: " + str(star.complete))
            count_s += 1
            habit_star += 1
        count_c += 1
    
    print("\n")
    print("----------------------------------------")
    print("Second Habit:")
    habit_star = 0
    count_c = 0
    for constellation in habits.second.constellations:
        print("Constellation " + str(count_c))
        count_s = 0
        for star in constellation:
            print("Habit star: " + str(habit_star) + " | Constellation star: " + str(count_s) + " | Complete: " + str(star.complete))
            count_s += 1
            habit_star += 1
        count_c += 1
    print("\n")
