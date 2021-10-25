import time
import board
import busio
import os
import multiprocessing, signal

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)


def play_music(name):
    print(f"music thread" + name)
    process_id = os.getpid()
    os.system ('aplay music_files/rex-incognito.wav')
    print(f"thread complete")

global process_id = ""

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    if mpr121[9].value:
        music = multiprocessing.Process(target=play_music, args=("cynthia",))
        processes.append(music)
        music.start()
        print(f"Thread started")
    if mpr121[11].value:
        if (process_id is not ""):
            print(f"hello")
            os.kill(process_id, signal.SIGINT)
            processes[0].terminate()
        else:
            print(f"there")
    time.sleep(0.5)  # Small delay to keep from spamming output messages.
