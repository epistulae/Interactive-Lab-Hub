# Zenith

Habit building is hard. It takes determination, perseverance, and some daily reminders. Unfortunately, most habit tracking apps are cluttered or easily forgotten. 

Introducing Zenith, a habit tracker where you light your way through the stars. This functional decor tracks up to two habits over 30 days, giving you a visual reminder to complete your goals. When inspiration strikes, don't wait til next Monday, next month, or even next year. Zenith doesn't label by the calendar so it's easy to start tracking your goals whenever. 

Zenith is also great for when it's time to relax. Just switch over to colored or animation mode for interesting mood lighting. 

Basic controls for habit tracking are on the frame, along with mode cycling and an on-off switch for the lights. The full suite of controls are available on the companion mobile app. Remember to log your activity every day! Once it's past midnight, you won't be able to give yourself credit. 

**Other functions:**
- (TODO) Do not disturb times: Set times when Zenith's lights should automatically turn off or on.
- Remote color and animation: Choose between a set of colors and animations.
- (TODO) Persistent mode: Save your habit tracking data and export to the app and see how you're doing over time.
- (TODO) Single vs duo habit mode: Only want to track one habit for longer? Switch to single habit mode to track one habit over 60 days instead of 2 habits over thirty. Note: Only available if you have not started tracking yet. If you've already begun, you'll have to start anew.

Coming soon: Zenith will be able to connect to your Spotify account and visualize the current track.

## Demo

## Table of Contents
- [Timeline](#timeline)
- [Design Stages](#design-stages)
    - [Initial Design Notes](#initial-design-notes)
    - [Prototyping](#prototyping)
    - [Laser Cutting: Star Map](#laser-cutting-star-map)
    - [Laser Cutting: Frame](#laser-cutting-frame)
- [Constuction](#construction)
- [Software Implementation](#software-implementation)
    - [Physical](#physical)
    - [Remote](#remote)
- [Reflection](#reflection)

## Timeline

| Objective | Time |
| :--------- | :----- |
| Ideation | Mid October |
| Initial sketches | Late October |
| Controls prototyping | Early November
| Materials testing | Early November
| Construction | Mid November
| Basic working prototype | Mid November
| Mobile application development | Mid November
| Completed prototype | Late November
| Full software (backend and application) | Late November
| Audio visualization: *Stretch goal* | Early December


## Design Stages
### Initial Design Notes
These are some rough notes from the initial planning stage. A lot of things were in flux.

Create some better way to track habits.

#### Possible designs:
- Florals, city scape? (Light up windows in buildings)
    - Direcly interact with a window to see it light up
    - Ideally uniquely designed for me. But, without being tacky.
- 1-2 items over 30 days?
    - Just one week?
- Key point: must be aestetically pleasing
- Secondary use: mood lighting? 

#### Main Steps:
- Figure out input
- Figure out display style
- Figure out LED connection (external power source? How to connect to pi?)
- On off button
- Program inputs
- Program LED reactions: lights, brightnes, etc.
- Remote control

#### Second round design
- Constellations/stars
- 30 or 60? How can I distinguish between the two habits?
    - Do I need a muxer? Capacitive sensors only give 12 touch sensors. If I want even 30, I need a mux since the chip only has one address change section so I can only daily chain 2 at once.
    - How shall I add layers? Clouds? Make it map like? (Star map)
- How to incorporate things subtlely:
    - Quotes as constellation connectors
    - Use Zelda colors: Orange for not activated, blue for activated
    - Possibly non-real constellations
    - If 60, need constellations that add up to two sets of 30.

Notes from mini-critique:
- Possibly have a projection? If using star design idea.
    - Decision, no, I want this to be very tactile for that sense of satisfaction physically. (Note: even though I added remote functionality, this is still a main point)

#### Third round design:
Constellation star map design: possibly with a shooting star that is a different color if today's habits are not done yet. Distinguish between the two habits by having them reprented by different constellations. Perhaps etch in the star 1 or 2 based on which habit.

Constellations:
| Constellation | Stars | Real | Habit |
|:-------------:|:-----:|:----:|:-----:|
|Summer Triangle|3|Asterism|1|
|Teapot|8|Asterism|1|
|Narwhale| 6|Fictional|1|
|Draco |13 (flex)|Real|1|
|Orion|8|Real|2|
|Hourglass| 5 (flex)|Fictional|2|
|Butterfly|6|Fictional|2|
|Cygnus|8|Real|2|
|L-shape|3|Fictional|2|

#### Constellation Designs
I tried several design options and all they combined permutations. I consulted several friends and other students to help decide on the final one: thin quote lines with varying star sizes (Varying as in likely two. Any more may feel like too much.)

First iteration:

<img width="697" alt="Screen Shot 2021-11-18 at 4 27 35 PM" src="https://user-images.githubusercontent.com/14368010/142499436-e7e9845f-1c57-497a-9d5e-6f9fcfce7f58.png">

Second iteration:

<img width="855" alt="Screen Shot 2021-11-18 at 4 29 28 PM" src="https://user-images.githubusercontent.com/14368010/142499728-c0d3d9b8-5fe8-4ecf-a9ae-2564b1ca3422.png">
<img width="905" alt="Screen Shot 2021-11-18 at 4 30 13 PM" src="https://user-images.githubusercontent.com/14368010/142499839-64521000-bf23-4cd2-b72e-ea2c4fef8042.png">

Third iteration: I was told that the quotes are cool but too big. So:

<img width="997" alt="Screen Shot 2021-11-18 at 4 32 03 PM" src="https://user-images.githubusercontent.com/14368010/142500057-a8b231a1-6998-4907-8949-a23349927d5c.png">

### Prototyping
For the input prototyping, please find the detailed documentation, pictures, and demo [here](https://github.com/epistulae/Interactive-Lab-Hub/tree/Fall2021/Lab%205).

### Laser Cutting: Star Map

Updated Contellations:
Constellations:
| Constellation | Stars | Real | Habit |
|:-------------:|:-----:|:----:|:-----:|
|Serpens Caput|6|Real|1|
|Shield|5|Real|1|
|Narwhale| 6|Fictional|1|
|Draco |13|Real|1|
|Orion|8|Real|2|
|Teapot|8|Asterism|2|
|Winter Triangle|3|Asterism|2|
|Hourglass| 5|Fictional|2|
|Butterfly|6|Fictional|2|

#### Cutting Tests
Before going on to design the whole map, I tested printing the design on acrylic. 

<img width="851" alt="Screen Shot 2021-11-18 at 4 18 51 PM" src="https://user-images.githubusercontent.com/14368010/142498290-5cccd1b4-bc59-45c1-8a06-11c648c90fbb.png">

Clearly, the initial design of using quotes directly as lines is not a good idea. Even put when behind transluscent acrylic and using the LEDs to cast shadows of the quotes, it looks horrendous, so I ultimately got to the final version of etching on the acrylic directly. The quotes are actually much more subtle in the final version, which is what I was originally going for. They are meant to be like little easter eggs. (For myself :D )

#### Full Constellation Map Design

Here are the Adobe Illustrator Iterations of the constellations design. While the shapes are filled, they had outline strokes (0.001) and it was printed (laser cut) with vector only. Placement and sizing achieve by tracking over reference photos. The final adobe illustrator file, along with pdf print files, are available in the [design]() folder. I added pinprick stars after thinking just the constellations looked a bit bland.

<img width="821" alt="Screen Shot 2021-11-18 at 3 53 27 PM" src="https://user-images.githubusercontent.com/14368010/142494990-bad40880-ffc3-4ec5-82c2-22852db77f5c.png">

<img width="547" alt="Screen Shot 2021-11-18 at 3 54 28 PM" src="https://user-images.githubusercontent.com/14368010/142495169-9fb11cc9-cdb2-4502-b7db-b6a32d57e99c.png">

<img width="576" alt="Screen Shot 2021-11-18 at 3 57 39 PM" src="https://user-images.githubusercontent.com/14368010/142495572-b55e1706-337b-4009-9353-30a8b0018a7f.png">

#### Materials Selection
I decided on matte black acrylic for a background due to how well it looks for a night sky. Glossy acrylic also smudges and attracts dust more than matte acrylic.

I also tested a couple different transluscent acrylics. 1/4" glossy white, 1/8" glossy white, 1/8" matte white, 1/16" glossy white. Testing led diffusion:

<img width="603" alt="Screen Shot 2021-11-18 at 4 09 00 PM" src="https://user-images.githubusercontent.com/14368010/142497081-2cce337f-c126-47b3-8a79-41cecf35e918.png">

I decided on 1/8" glossy for the stars and constellation lines. This allows the etched quotes to show up better and when the lights are off, light bounces off the glossy white in a very lovely faint twinkle.

#### Completed Acrylic

On a whim, I decided to add my signature to the lower right hand corner the same way I would sign artwork. The signature was vectorized and then etched at half power of the cutting. Note: signature vector is filled with grey, not black, which would be deeper. See exact colors in the Adobe Illustrator files.

<img width="954" alt="Screen Shot 2021-11-18 at 4 40 32 PM" src="https://user-images.githubusercontent.com/14368010/142501177-2442308c-310a-4b60-8aad-f8ca5e029afd.png">


### Laser Cutting: Frame
Note: when building Zenith, the frame was the last thing I did. I layed out the leds and tested those with a basic functionality software before moving onto the frame.

The frame is 3/32" (2.5mm) birch plywood (I see 5 visible layers from the side). The wood is painted with a mix of mars black and burnt umber in a 1 to 2 ratio. Mars black is a very blue toned back so it tones down the warming burnt umber for a very deep, neutral brown.

## Construction

I tested having the LEDs directly against the constellations. I expected it will not be enough diffusion, and indeed you can very clearly see the distinct LEDs. 

<img width="691" alt="Screen Shot 2021-11-18 at 4 54 48 PM" src="https://user-images.githubusercontent.com/14368010/142503066-bcd969f7-8b94-4283-99c1-927474022cc3.png">


After just manually testing the distance the LEDs should be, around 7/16" is a pretty good distance. I tested a couple different spacer designs and the final iteration worked well, so I printed out enough for the whole design. The final one has slightly chubbier legs to make it easier to glue, and more of a tab on top to completely cover the width of the strip.

<img width="524" alt="Screen Shot 2021-11-18 at 4 55 10 PM" src="https://user-images.githubusercontent.com/14368010/142503111-4011ff97-50a2-4808-ab1b-115731e956ea.png">

Though it was more effort to raise the LEDs, it make a clear difference. 

<img width="286" alt="Screen Shot 2021-11-19 at 3 12 02 AM" src="https://user-images.githubusercontent.com/14368010/142588268-6ad9cd23-56ac-4db8-ace7-cf83cf35c5f4.png">

#### Progress shots:
<img width="871" alt="Screen Shot 2021-11-19 at 3 02 27 AM" src="https://user-images.githubusercontent.com/14368010/142587103-bb48c48a-262a-456b-8209-c615800f780b.png">

<img width="869" alt="Screen Shot 2021-11-19 at 3 10 16 AM" src="https://user-images.githubusercontent.com/14368010/142588023-9ae1b727-b375-4131-a167-5d6bb16f1a14.png">


## Software Implementation
### Physical
### Remote

## Reflection

Roughly estimating wattage for LED power consumption wasn't the best idea. Zenith currently uses a 5V 15A power supply for a max 75W power. The website suggested 5V 20A but the ones I saw on Amazon were too bulky so I opted for slightly less. On the other hand, this was sort of a happy accident, because I get lovely gradients without manually programming them in.

