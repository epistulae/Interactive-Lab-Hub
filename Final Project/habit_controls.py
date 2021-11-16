#!/usr/bin/env python3

import led_controls as Leds
import stars as Stars
import time

class State:
    def __init__(self):
        self.day = time.localtime()[2]
        self.first = Stars.HABIT_A
        self.second = Stars.HABIT_B

habits = State()

def flipFirstHabit(strip, debug=False):
    constellation = habits.first.cur_constellation
    star = habits.first.cur_star
    habits.first.constellations[constellation][star].complete = not habits.first.constellations[constellation][star].complete
    Leds.updateStar(strip, habits.first.constellations[constellation][star])
    if debug:
        debugHabits()
    
def flipSecondHabit(strip, debug=False):
    constellation = habits.second.cur_constellation
    star = habits.second.cur_star
    habits.second.constellations[constellation][star].complete = not habits.second.constellations[constellation][star].complete
    Leds.updateStar(strip, habits.second.constellations[constellation][star])
    if debug:
        debugHabits()

def nextDay():
    day = time.localtime()[2]

    if day is not habits.day:
        habits.day = day
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

def debugHabits():
    print("========================================")
    print("Habits Debugging")
    print("========================================\n")
    
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
        
    print("----------------------------------------\n")
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
