# Chatterboxes
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Additional Parts

As mentioned during the class, we ordered additional mini microphone for Lab 3. Also, a new part that has finally arrived is encoder! Please remember to pick them up from the TA.

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. As we discussed in the class, there are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2021
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.
### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using a USB microphone, and the speaker on your webcamera. (Originally we intended to use the microphone on the web camera, but it does not seem to work on Linux.) In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*

My shell file is greetings.sh. I used the GoogleTTS because it's the least robotic sounding.



### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

One thing you might need to pay attention to is the audio input setting of Pi. Since you are plugging the USB cable of your webcam to your Pi at the same time to act as speaker, the default input might be set to the webcam microphone, which will not be working for recording.

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

My shell file is age_question.sh. The recording is saved in recorded_mono.wav.


### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*

<img width="565" alt="Screen Shot 2021-10-06 at 6 43 24 AM" src="https://user-images.githubusercontent.com/14368010/136188309-1b5ea29a-cc5e-4246-8218-be18b8978a96.png">
<img width="558" alt="story2" src="https://user-images.githubusercontent.com/14368010/137573654-c9441bdc-4220-4f4c-ac64-6a5487b0123e.png">

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 


\*\***Please describe and document your process.**\*\*
I used a notepad to brainstorm and I used some sticky notes to create a speech flowchart for my speech-enabled vacuum cleaner. 
<img width="1406" alt="flow" src="https://user-images.githubusercontent.com/14368010/137573332-51648f1f-8af4-4b93-bdc1-caaddf73dcd7.png">

I expect dialogue to be like:
- Schedule a cleaning for 9AM. "Done. Cleaning scheduled for 9AM." and other scheduling commands.
- Clean the kitchen. "Going to clean the kitchen." and other similar cleaning commands.
- How dirty was the house today? "Cleaning this floor resulted in 10 grams of debris." and other questions relating to metric. (Maybe even comparisons between dates/time periods.)
- Cancel current cleaning. "Stopping vacuum of the study. Returning to port." and other interruption commands.

### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

It was very different from what I expected. My partner specifically broke down parts of the vacuuming process. Specifically, she said:
- Vacuum the floor.
- Dump the trash.
- Go to your home.
- Charge yourself. 

All of these diaglog options were much simpler than I brainstormed. I was thinking the vacuum would be directed the same way you might as a roommate to do a chore. Also, it was hard to initialize the conversation/interaction as my partner didn't know what I was supposed to be. I said something along the lines of: "Good morning (assuming it just reached 9 AM), it's 9AM. Starting scheduled cleaning." 

Please see a clip of that interaction below. The full recording had trouble being uploaded to Github.

https://user-images.githubusercontent.com/14368010/135969405-e876d42a-fa09-4041-8f87-d0ba649bdc07.mov

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*
I did not wizard with the Pi.


# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...
- I could include an introduction message when my device starts up, i.e. for the first time out of the box, since afterwards the user would be already familiar, it doesn't need to do the spiel every time. 
- I should also add a command where the user can ask the device "what can you do", and what commands it can follow. This will clear up misunderstandings of what level of granularity commands need to be. For perhaps, after some simple commands, the device can offer futher functionality, i.e. "I see you've asked me to clean the kitchen every other day, should I schedule in a cleaning routine?"
- Following one point a fellow student brought up, having a robot voice randomly start announcing something, i.e. "job complete" is very jarring. Having something like music to prelude the voice, or even replace the voice may make it more user friendly. This reminded me of my rice cooker, which plays a cheerful tune when it's complete. I think having this at the start of umprompted statements from the device would be nice.


2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?

**Device to User Interaction Signal**

I would use something like light and different light colors to show different states of readiness for interactions. For example, if the vacuum is low on battery, it might have a battery light that can turn red. 

This would signal to the user immediate action commands can't be carried out right now. E.g. the user wouldn't need to go through this kind of interaction:
- User: "Go clean the kitchen."
- Vacuum: "Sorry, I'm low on battery, want me to schedule cleaning for once I'm at least 20% charged?"
- User: "No. :( "

**User to Device Interaction Signal**

I would have 1-3 pressable buttons that when pressed, will do some common commands, i.e. 'empty the trash', 'go clean everywhere', or 'map out the room floorplan'.


3. Make a new storyboard, diagram and/or script based on these reflections.

<img width="889" alt="Screen Shot 2021-10-16 at 1 43 56 AM" src="https://user-images.githubusercontent.com/14368010/137575400-ad6b1218-c3c1-49f6-9b09-a90a9d7c147d.png">

**Indroduction script:**

Vacuum: *Jingle jingle* Hello! I am Sweep, your new cleaning companion. I can help you keep your home super clean all the time! On my first cleaning through your home, I will map out the floor plan so you can assign room names and tell me to clean specific rooms. I can also schedule cleaning routines to make spotless floors a bleeze. To get started, just say "Sweep, clean my house."

User: "Sweep, clean my house."

Vacuum (Sweep): "Beginning first cleaning of the house. Creating the floorplan."

**Suggestion script:**

Sweep: *Jingle jingle*, job complete. I've finished cleaning your kitchen! I noticed you like having the kitchen cleaned every other day in the evenings between 7 and 9 PM. Should I make this a routine?

User: Yes! Please do.

Sweep: OK! Routine saved.


## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*
I made a mini model wizard of my device in a tabletop setting. The audio sensor takes in the commands and the "vacuum" Sweep responds out loud and goes to complete whatever task the user asked it to do. The Pi controls the webcam which sit on top of the pseudo "dock" for Sweep.

Individual responses as part of this demo are hard coded, with three sets of full back and forth interactions that have varied responses based on audio input. Specifically:
- *sweep_introduction_sequence.sh* Introduction sequence -> maybe start cleaning.
- *simple_clean_interaction.sh* Immediate cleaning command -> confirmation of command acknowledged. 
- *routine_suggestion.sh* Suggestion for routine -> possible saving of routine.

One issue was how it wasn't clear how to start interacting with the device, so I added a "Start" button to the mock design. Upon "startup", this initiates the introduction. The idea is, afterwards, it will be a "clean everything" manual button. 

While vacuum robots exist, i.e. iRobot, I noticed while using it that some things it can do are not clear, and only explained in the manual. But, honestly, who reads the manual? So, I took inspiration from Alexa, and from peer feedback, to include automatic suggestions and a clear introduction for the device. Here's a sample interaction (video):

*Include videos or screencaptures of both the system and the controller.*

Full demo video on Youtube: https://youtu.be/Ff1PvFMi4Fs

*sweep_introduction_sequence.sh* Interaction, both branches:


https://user-images.githubusercontent.com/14368010/137579914-f2e8af94-6548-44f9-8a00-64ac2892e6b2.MOV


https://user-images.githubusercontent.com/14368010/137579921-a385a444-9d71-4fd8-a1d2-f3b0adf391bb.MOV




*simple_clean_interaction.sh* Interaction, both branches:

*routine_suggestion.sh* Interaction, both branches:


## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.) 

Answer the following:

### What worked well about the system and what didn't?
\*\**your answer here*\*\*

### What worked well about the controller and what didn't?

\*\**your answer here*\*\*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

\*\**your answer here*\*\*


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

\*\**your answer here*\*\*

