#!/usr/bin/env python3

class Star:
    def __init__(self, index, complete=False):
        self.index = index
        self.complete = complete
        # Previous stars: (star, connector)
        self.prior_stars = []
        
class Habit:
    def __init__(self, constellations):
        self.constellations = constellations
        self.cur_constellation = 0
        self.cur_star = 0
        
PINPRICKS = [0, 58, 59, 60, 76, 77, 98, 99, 100, 101, 122, 123, 124, 125, 130, 142, 143] 

# Constellation Graphs
hourglass_1 = Star(1)

hourglass_2 = Star(6)
hourglass_2.prior_stars.append((hourglass_1, [2, 3, 4, 5]))

hourglass_3 = Star(10)
hourglass_3.prior_stars.append((hourglass_1, [23, 24]))
hourglass_3.prior_stars.append((hourglass_2, [7, 8, 9]))

hourglass_4 = Star(14)
hourglass_4.prior_stars.append((hourglass_3, [11, 12, 13]))

hourglass_5 = Star(19)
hourglass_5.prior_stars.append((hourglass_3, [20, 21, 22]))
hourglass_5.prior_stars.append((hourglass_4, [15, 16, 17, 18]))

HOURGLASS = [hourglass_1, hourglass_2, hourglass_3, hourglass_4, hourglass_5]

# -------------------------------------------------------

teapot_1 = Star(50)

teapot_2 = Star(46)
teapot_2.prior_stars.append((teapot_1, [47, 48, 49]))

teapot_3 = Star(44)
teapot_3.prior_stars.append((teapot_1, [25,26]))
teapot_3.prior_stars.append((teapot_2, [45]))

teapot_4 = Star(30)
teapot_4.prior_stars.append((teapot_3, [27, 28, 29]))

teapot_5 = Star(33)
teapot_5.prior_stars.append((teapot_3, [41, 42, 43]))
teapot_5.prior_stars.append((teapot_4, [31, 32]))

teapot_6 = Star(35)
teapot_6.prior_stars.append((teapot_5, [34]))

teapot_7 = Star(37)
teapot_7.prior_stars.append((teapot_6, [36]))

teapot_8 = Star(57)
teapot_8.prior_stars.append((teapot_1, [51, 52, 53, 54, 55, 56]))
teapot_8.prior_stars.append((teapot_5, [39, 40]))
teapot_8.prior_stars.append((teapot_7, [38]))

TEAPOT = [teapot_1, teapot_2, teapot_3, teapot_4, teapot_5, teapot_6, teapot_7, teapot_8]

# -------------------------------------------------------

triangle_1 = Star(65)

triangle_2 = Star(61)
triangle_2.prior_stars.append((triangle_1, [62, 63]))

triangle_3 = Star(68)
triangle_3.prior_stars.append((triangle_1, [66, 67]))
triangle_3.prior_stars.append((triangle_2, [69, 70, 71]))

TRIANGLE = [triangle_1, triangle_2, triangle_3]

# -------------------------------------------------------

butterfly_1 = Star(72)

butterfly_2 = Star(97)
butterfly_2.prior_stars.append((butterfly_1, [73]))

butterfly_3 = Star(75)
butterfly_3.prior_stars.append((butterfly_2, [74]))

butterfly_4 = Star(93)
butterfly_4.prior_stars.append((butterfly_2, [94, 95, 96]))
butterfly_4.prior_stars.append((butterfly_3, [78, 79, 80]))

butterfly_5 = Star(87)
butterfly_5.prior_stars.append((butterfly_4, [81, 82, 83, 84, 85, 86]))

butterfly_6 = Star(88)
butterfly_6.prior_stars.append((butterfly_4, [89, 90, 91, 92]))

BUTTERFLY = [butterfly_1, butterfly_2, butterfly_3, butterfly_4, butterfly_5, butterfly_6]

# -------------------------------------------------------

orion_1 = Star(102)

orion_2 = Star(105)
orion_2.prior_stars.append((orion_1, [103, 104]))

orion_3 = Star(108)
orion_3.prior_stars.append((orion_2, [106, 107]))

orion_4 = Star(109)

orion_5 = Star(112)
orion_5.prior_stars.append((orion_1, [110, 111]))

orion_6 = Star(114)
orion_6.prior_stars.append((orion_5, [113]))

orion_7 = Star(116)
orion_7.prior_stars.append((orion_6, [115]))

orion_8 = Star(118)
orion_8.prior_stars.append((orion_7, [117]))
orion_8.prior_stars.append((orion_3, [119, 120, 121]))

ORION = [orion_1, orion_2, orion_3, orion_4, orion_5, orion_6, orion_7, orion_8]

# -------------------------------------------------------

serpens_1 = Star(40)

serpens_2 = Star(37)
serpens_2.prior_stars.append((serpens_1, [138, 139]))

serpens_3 = Star(35)
serpens_3.prior_stars.append((serpens_1, [141]))
serpens_3.prior_stars.append((serpens_2, [136]))

serpens_4 = Star(33)
serpens_4.prior_stars.append((serpens_3, [127, 128]))

serpens_5 = Star(29)
serpens_5.prior_stars.append((serpens_4, [131, 132]))

serpens_6 = Star(26)
serpens_6.prior_stars.append((serpens_5, [127, 128]))

SERPENS = [serpens_1, serpens_2, serpens_3, serpens_4, serpens_5, serpens_6]

# -------------------------------------------------------

narwhale_1 = Star(0)

narwhale_2 = Star(0)

narwhale_3 = Star(0)

narwhale_4 = Star(0)

narwhale_5 = Star(0)

narwhale_6 = Star(0)

NARWHALE = [narwhale_1, narwhale_2, narwhale_3, narwhale_4, narwhale_5, narwhale_6]

# -------------------------------------------------------

draco_1 = Star(0)

draco_2 = Star(0)

draco_3 = Star(0)

draco_4 = Star(0)

draco_5 = Star(0)

draco_6 = Star(0)

draco_7 = Star(0)

draco_8 = Star(0)

draco_9 = Star(0)

draco_10 = Star(0)

draco_11 = Star(0)

draco_12 = Star(0)

draco_13 = Star(144)
draco_13.prior_stars.append((draco_12, [145]))

DRACO = [draco_1, draco_2, draco_3, draco_4, draco_5, draco_6, draco_7, draco_8, draco_9, draco_10, draco_11, draco_12, draco_13]

# -------------------------------------------------------

shield_1 = Star(0)

shield_2 = Star(0)

shield_3 = Star(0)

shield_4 = Star(0)

shield_5 = Star(0)

SHIELD = [shield_1, shield_2, shield_3, shield_4, shield_5]

# Habit Constants
HABIT_A = Habit([SERPENS]) # narwhale, serpens, draco, shield
HABIT_B = Habit([HOURGLASS, TEAPOT, TRIANGLE, ORION, BUTTERFLY])
