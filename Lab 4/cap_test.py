import time
import board
import busio
import os

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
        if mpr121[1].value:
            os.system("mpg123 rex-incognito.wav")
    time.sleep(1)  # Small delay to keep from spamming output messages.
