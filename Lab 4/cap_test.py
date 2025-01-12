import time
import board
import busio
import multiprocessing, signal

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)


def play_music(name):
    print(f"music thread" + name)
    time.sleep(10)
    print(f"thread complete")

processes = list()

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
        if (len(processes) is not 0):
            print(f"hello")
            processes[0].terminate()
        else:
            print(f"there")
    time.sleep(0.5)  # Small delay to keep from spamming output messages.
