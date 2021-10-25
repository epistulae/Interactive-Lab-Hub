import time
import board
import busio
import subprocess
import multiprocessing, signal

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Global process variable control.
manager = multiprocessing.Manager()
Global = manager.Namespace()
Global.music_process_id = 0

def play_music(song_name):
    print(f"music thread " + song_name)
    Global.music_process_id = os.getpid()
    print(Global.music_process_id)
    Global.music_process_id = subproccess.run("aplay music_files/" + song_name, capture_output=True, shell=True)
    print(Global.music_process_id)

while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    if mpr121[7].value:
        music = multiprocessing.Process(target=play_music, args=("rex-incognito.wav",))
        music.start()
        print(f"Thread started rex")
    if mpr121[9].value:
        music = multiprocessing.Process(target=play_music, args=("let-the-living-beware.wav",))
        music.start()
        print(f"Thread started living")
    if mpr121[11].value:
        print(Global.music_process_id)
        if (Global.music_process_id is not 0):
            print(f"hello")
        else:
            print(f"there")
    time.sleep(0.5)  # Small delay to keep from spamming output messages.
