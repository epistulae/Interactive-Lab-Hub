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
- I added several possible functionalities as thing went on, inluding playing around with the light sensor to detect daylight and the proximity sensor to do gesture controlled actions, possibly with audio output. However, I took a step back and realized it was straying away from the point of the product I want to make and overloading it. Ultimately, Zenith is wall art that functions as a habit tracker with added creative lighting, and the best way to do that with is more obvious inputs. Also, my chosen LEDs require I turn off the microphone speaker.

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
- This was incredibly ugly looking, essentially a very large switch statement (which does not exist in Python). After playng around a little, I decided to not completely implelent it.

**Use in final?**

Most certainly not. I thought it might make sense to even tie in the on-off button for the Pi, but that wants to be wired to a different GPIO pin than the QWIIC pins. The numpad makes the frame far too big and it's a very large, and frankly, ugly component to live on the frame. Given aestetics is a big component of the project, this is not the best choice. It also needs a codebook to operate. I want everything to be as simple as possible on the product itself.

### Tactile Buttons
<img width="500" align="left" alt="Screen Shot 2021-11-01 at 2 19 57 AM" src="https://user-images.githubusercontent.com/14368010/139629968-02a6650d-9855-440e-b4c9-406feacad56b.png">

\
&nbsp;
\
&nbsp;
\
&nbsp;

These are two connected LED tactile buttons on a Sparkfun QWIIC button breakout. The breakout boards have the addresses set up on the back side to use different addresses (Note: breakout board has 4 addressable bits, so I can chain 16 max), so I can chain them together. This version of input only allows for daily tracking.

If I also use tactile buttons for brightness, and perhaps just one button to cycle through the modes would be sufficient.

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
- This implementation was extended in the capacitive version. Overall, having simplicity in the button makes sense, because, again, while more functionality, even in inputting habit on different dates may seem desirable, the goal is to do everything *the day of*. 

#### Demo
Please see capacitive with OLED demo. This demo was very uninteresting since it just printed on terminal, and the capacitive demo includes the same functionality.

**Use in final?**

No. If I could get blue buttons it would be different but the colors don't fit the aestetic. I may use one of the button as an on off switch, without turning on the LED in the button since when Zenith is on, all the other LED lights would be on for the constellations.

### Rotary Encoder with OLED display
This is a rotary encoder with a display that shows the value for the encoder. At different turns, it shows what thing is being acted on if the encoder is pressed. It's broken up into Habit A, Habit B, and 3 brightness levels split up between 360 degrees.

Notes from prototyping:
- The general shape is difficult to ork with, and there is no good, clean way to prevent a user from overturning, though the coding can just mod everything.
- Tracking two habit with the encoder is non-intuitive.
- The encoder extends very far from the frame.
- Ideally this is best for the brightness adjustment only, but I see very little need for this to be on the frame if it is this unaestetic and is not multifuncitonal.

**Use in final?**

No. It is not only ugly but it is also unintuitive. At this point I've ruled out the OLED screen in general, and the rotary encoder cannot work without a screen to show what you're reacting on.

### Capacitive Buttons (Constellation)
General capacitive buttons but directly using the stars on the contellation display.

Notes from prototyping:
- Copper tape blocks light so to compensate for the same size of light, the stars and lines needed to be larger and overall, it was not the design I'm looking for.
- Trying to precisely wrap the copper tape was a nightmare. The adhesive is not too strong, and the tape itself tears easily, which is very unfortunate when working on a sharp opject (stars).

**Use in final?**

No. I could barely get the prototype to even connect to the capacitive sensor board, and it look very unappealing. Inputs were also only logged about 20% of the time.


### Capacitive Buttons with OLED Display
Capacitive buttons against the frame. In this iteration, 4 buttons, 2 for habit input and 2 for shifting the dates up and down. This iteration has the OLED screen displaying what the inputs are. There is another iteration of this prototype without the OLED screen, but since it's just the same functionality as the tactile buttons and the 2 habit input buttons here, I'm not going to explicitly document it separately.

Notes from prototyping:
- Tape is still hard to use around an irregular shape (star), but worked much better on the arrow. Perhaps consider other simple shapes for input buttons. 
- The copper is bright but not too eye catching unless under direct light.
- Without the OLED, the buttons themselves take up very, very little space.

#### Programing
The initial version of this includes saving to an on-disk (SD Card) file. This will be directly pushed to Github. I'm experimenting with directly connecting my gmail account, but that seems like a problematic security issue, so perhaps a text file to Github is sufficient. The Pi can be programmed to export to github on turndown.

All inputs are saved so this is a stateful system. This is because the tracker wouldn't really function well if it refreshed every time. However, this reminded me that perhaps I want to include a refresh function in a future mobile application for non-necessary functions.

#### Demo


https://user-images.githubusercontent.com/14368010/141211988-3e875576-6550-4115-8887-8e8597c4b0d9.mp4


**Use in final?**

Yes. But, just the capacitive buttons without OLED. It's not great to test without the screen in a demo if I don't have the LEDs responding to inputs, but the screen becomes redundant in the final product. Also, while it's nice to be able to backfill, and perhaps this is a functionality for the phone app, the device itself is meant for direct, daily, in person use. Thus, just 3 capacitive buttons (Habit A, Habit B, Mode change cycle) plus a tactile button (on-off) is sufficient.

