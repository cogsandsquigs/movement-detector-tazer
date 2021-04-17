"""
This code was written by Ian Pratt (ipratt-code, t0x1c_101, etc.)
All of this was his design. It's purpose? To get the sound level of an audio stream.
"""

import pyaudio
import numpy as np
import pylab
import time

RATE = 44100
CHUNK = int(RATE / 20)  # RATE / number of updates per second


def GenStream():
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    return stream


def StopEverything(stream):
    stream.stop_stream()
    stream.close()
    pyaudio.PyAudio().terminate()


def GetSoundLevel(s):
    return np.average(np.abs(np.fromstring(s.read(CHUNK), dtype=np.int16)) * 2)


"""
stream = GenStream()
for i in range(int(10 * RATE / CHUNK)):  # do this for 10 seconds
    print(GetSoundLevel(stream))
StopEverything(stream)
"""
