#!/usr/bin/env python3

import stars as Stars
import time

class State:
    def __init__(self):
        self.lights = True # True = on, False = off
        self.day = time.localtime()[2]
        # Habit = 0
	# Mood lighting = 1
	# More can be added. Update mode_count to match and add appropriate handlers.
        self.mode = 0 
        self.mode_count = 2
        self.color = "Rainbow"
        
STATE = State()

def nextDay():
    day = time.localtime()[2]
    
    if day is not STATE.day:
        STATE.day = day
        # Habit A
        if Stars.HABIT_A.cur_star + 1 is len(Stars.HABIT_A.constellations[Stars.HABIT_A.cur_constellation]):
            # Next constellation (assumes not final star overall, if it was, I'd wipe the state)
            Stars.HABIT_A.cur_constellation += 1
            Stars.HABIT_A.cur_star = 0
        else:
            # Next star
            Stars.HABIT_A.cur_star += 1

        # Habit B
        if Stars.HABIT_B.cur_star + 1 is len(Stars.HABIT_B.constellations[Stars.HABIT_B.cur_constellation]):
            # Next constellation (assumes not final star overall, if it was, I'd wipe the state)
            Stars.HABIT_B.cur_constellation += 1
            Stars.HABIT_B.cur_star = 0
        else:
            # Next star
            Stars.HABIT_B.cur_star += 1

def debugHabits():
    print("========================================")
    print("Habits debugging")
    count_c = 0
    for constellation in Stars.HABIT_A.constellations:
        print("Habit A Constellation " + str(count_c))
        count_s = 0
        for star in constellation:
            print("Star " + str(count_s) + " complete: " + str(star.complete))
            count_s += 1
        count_c += 1
    count_c = 0
    for constellation in Stars.HABIT_B.constellations:
        print("Habit B Constellation " + str(count_c))
        count_s = 0
        for star in constellation:
            print("Star " + str(count_s) + " complete: " + str(star.complete))
            count_s += 1
        count_c += 1
