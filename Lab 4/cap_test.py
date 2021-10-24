import time
import board
import busio
import multiprocessing, signal

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)


def play_music(name):
    while !interrupt_thread:
        print(f"music thread" + name)
        time.sleep(10)
        print(f"thread complete")

processes = list()

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    if mpr121[1].value:
        music = threading.Thread(target=play_music, args=("song",))
        threads.append(music)
        music.start()
        print(f"Thread started")
    if mpr121[9].value:
        interrupt_thread = true
    time.sleep(0.5)  # Small delay to keep from spamming output messages.
