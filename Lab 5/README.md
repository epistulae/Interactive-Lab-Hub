Note: My lab 5 is on my final project and testing/prototyping some interactions for it.

# Overview
## Final Project: Zenith
Zenith will be a wall art piece that provides (30-day, two-habit) habit tracking, mood lighting, and audio-reactive lights. 

General Goals of the product:
- Visual indicator of goal progress.
- Highly visible reminder to stay on track of habit.
- Satisfaction of physically 'checking' something off.
- Aestetically pleasing addition to living space.
- Multifunctional (in some way, unspecified).

As of 10/31/2021: The current design is going to be 60 stars arranged in constellations, with groups of constellations consisting of 30 total stars. Constellations are both real and fictional, drawing from my favorite things. Further design to be decided based on outcome of this lab. 

*General aestetic: modern.*

In this lab, I am prototyping interactions with key components of the product. Mainly:
- Habit input 
- Manual light adjustment

## Interaction Planning
Initial thoughts were to use a total of 60 capacitive sensors (use an 8-way muxer with five 12-touch capacitive sensors), one tied to each day/habit.

Some initial feedback from just talking through rough sketches of the product design. 
- Consider not interacting directly with each day/habit tracker directly. How can I retain that satisfaction of touching the sensor and getting instantaneous feedback?
- Consider moving away from an explicitly physical display. What about projection, maybe on the ceiling?
    - I think this takes away from the satisfaction when completing the habit task a bit. I would like to be able to physically interact with something. Also, given I want it to be constantly visible, having it on the ceiling may not be the best idea, especially during the day when there's sunlight or even bright indirect light.
    - Side note: could be an interesting to explore for a different star gazing project though.
- What happens if you're not physically there? How do you track retroactive progress? How do you track this remotely if you're traveling?
    - I think having a companion appliction would be a good idea, not only for this, but for other lighting mode adjustments. But this will be further explored once I actually prototype and see what feels good. 


Key takeaways from sketch brainstorming:
- Rather than just modes of lighting (i.e. tracking vs mood vs audio-reactive), I should also have brightness adjustments and add a sleep/off functionality for night time. The latter will be good for both the user and the Raspberry Pi and the LEDs' longevity. Light is a major disruptor for sleep and I for one cannot sleep with an eye mask on.
- There is very little real estate on the side of the frames and it should be used carefully, without overcrowding. It's also important to not make the frame width too large, as that will look awkward.
- Consider height! Tactile buttons general have low profile, same with displays, around 1/8 inch or lower. Some physical component may not make sense if they protrude too much from the frame. Test these in prototypes to be sure before moving too far with the design.

## Prototyping
### Sensors to try protoyping with
<img width="1181" alt="Screen Shot 2021-11-01 at 1 39 42 AM" src="https://user-images.githubusercontent.com/14368010/139626545-8c7d798f-82f3-48b6-a6e6-7295b67c3d3d.png">

Note: possibly using display in conjunction with tactile buttons or with touch sensors.

General ideas on how to use these:

<img width="474" alt="Screen Shot 2021-11-01 at 1 43 12 AM" src="https://user-images.githubusercontent.com/14368010/139626864-0169a396-65b8-44e8-825b-99224ea32dbd.png"> <img width="479" alt="Screen Shot 2021-11-01 at 1 43 32 AM" src="https://user-images.githubusercontent.com/14368010/139626877-6a79bbff-0185-4ae0-85b4-a669bd4e2395.png">

<img align="left" width="400" alt="Screen Shot 2021-11-01 at 2 02 13 AM" src="https://user-images.githubusercontent.com/14368010/139628382-d4b9dea5-056b-4d76-adb9-737c242f3a53.png"> 

\
&nbsp;
\
&nbsp;
\
&nbsp;
\
&nbsp;
\
&nbsp;

The prototypes will be a section of the left/right side of the frame. The structure is so we can somewhat imagine what it'd be like to interact with these input options against a wall.

\
&nbsp;
\
&nbsp;
\
&nbsp;
\
&nbsp;
\
&nbsp;
\
&nbsp;

<img align="right" width="500" alt="Screen Shot 2021-11-01 at 2 20 31 AM" src="https://user-images.githubusercontent.com/14368010/139630027-18d81964-3df2-4397-b0ec-4c96a0503c2f.png">

### OLED Display + Number Pad

The display will show the inputs in real time as the user inputs them. The number pad gives a lot of versatility. We can have a codebook and have the number pad control all interactions in general (outside of the on/off sleep).

Sample codebook:
- Habit tracking (retroactive possible, programatically block proactive)
    - 1 through 30 followed by star * is tracking for habit A. 
    - 1 through 30 followed by pound # is tracking for habit B.
    - Just * or # for today's tracking of both habits.
- Display mode
    - Maybe some longer numbers. I.e. 6663 (MOOD), 87225 (TRACK) or even just sequences the user likes.
- Brightness
    - 100, 200, ... through 500 for 5 brightness levels.

<img width="833" alt="Screen Shot 2021-11-01 at 2 41 34 AM" src="https://user-images.githubusercontent.com/14368010/139631934-e1dcc67a-d4b2-49bd-94f9-046400efcf15.png">

Notes from prototyping:
- Display has QWIIC connectors that are 1/8 inch, and display is 1/16 inch under the connectors, and with the board being at least 1/8 inch, the screen is sunken into the frame by at least 3/16 inch. I could have a sloped viewing area to counteract but...
- The number pad is quite large and makes the frame need at least 2 1/8 inches without the 1/8 or 1/4 inch thickness from the acrylic slab where the main design would be.
- The pad is also quite conspicuous, and I prefer the design to be more incognito.
- Usage against the wall is actually not too bad. Not the most ergonomic, but not bad.
- It does limit where the product can be displayed, the side with the pad must be visble/have sufficient lighting and reachable.
    - Alternatively, I can have a pad on both sides, but that would be even less aestetically pleasing. 

#### Programing
Notes from initial implementation:
- TODO

#### Demo
TODO

**Use in final? TODO **


### Tactile Buttons
<img width="500" align="left" alt="Screen Shot 2021-11-01 at 2 19 57 AM" src="https://user-images.githubusercontent.com/14368010/139629968-02a6650d-9855-440e-b4c9-406feacad56b.png">

\
&nbsp;
\
&nbsp;
\
&nbsp;

These are two connected LED tactile buttons on a Sparkfun QWIIC button breakout. The breakout boards have the addresses set up on the back side to use different addresses (Note: breakout board has 4 addressable bits, so I can chain 16 max), so I can chain them together. This version of input only allows for daily tracking.

If I also use tactile buttons for brightness, perhaps just one button to cycle through the modes would be sufficient.

\
&nbsp;
\
&nbsp;
\
&nbsp;
\
&nbsp;

<img width="828" alt="Screen Shot 2021-11-01 at 2 43 45 AM" src="https://user-images.githubusercontent.com/14368010/139632140-cec2dc71-fbc3-45a4-903a-42fb43bf9486.png">

Notes from prototyping:
- The board used is slightly more than 1/8 inch so when used on a 1/8 inch frame, it would feel better. The buttons would be flush against the surface of the frame but the low actuation needed to push the buttons means that's perfectly fine.
- The LED part of the buttons are kind of useless, because a design aspect is having the sides be clean and simple.
- Would need different button colors (or paint).
- No retroactive tracking, (in 2 button version) so need to rely on some companion phone/web application.
- Low space requirements. Allows for thinner frame profile.
- Generally incognito (minus color). Alternatively, can use blue/orange to match expectd base tracker mode LED colors.
- Button themselves (if in the right colors) can give far away visual indication of habit completeness for the day (if frame is easily visible).
- Can be implemented on both sides (2 button version only), so the product can be placed/moved anywhere so long as one side is available.

#### Programing
Notes from initial implementation:
- TODO

#### Demo
TODO

**Use in final? TODO **

### Capacitive Buttons (Frame)
** TODO **

### Capacitive Buttons (Constellation)
** TODO **

### Capacitive Buttons with OLED Display
** TODO **

### Rotary Encoder with OLED display
** TODO **
