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

In this lab, I am prototyping possible interactions with key components of the product. Mainly:
- Habit input 
- Manual light adjustment

## Interactions
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

### Sensors to try protoyping with
<img width="1181" alt="Screen Shot 2021-11-01 at 1 39 42 AM" src="https://user-images.githubusercontent.com/14368010/139626545-8c7d798f-82f3-48b6-a6e6-7295b67c3d3d.png">

Note: possibly using display in conjunction with tactile buttons or with touch sensors.

General ideas on how to use these:

<img width="474" alt="Screen Shot 2021-11-01 at 1 43 12 AM" src="https://user-images.githubusercontent.com/14368010/139626864-0169a396-65b8-44e8-825b-99224ea32dbd.png"> <img width="479" alt="Screen Shot 2021-11-01 at 1 43 32 AM" src="https://user-images.githubusercontent.com/14368010/139626877-6a79bbff-0185-4ae0-85b4-a669bd4e2395.png">

