# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:45:22 2020

@author: Razan
"""
import pyaudio
import aubio
import numpy as np
import sys
import time
# Inital setup
pitches={196: 'G3', 207.65: 'G#3/ Ab3', 220: 'A3', 233.88: 'A#3/ Bb3', 246.94: 'B3', 261.63: 'C4', 277.18: 'C#4/ Db4', 293.66: 'D4', 311.13: 'D#4/ Eb4', 329.63: 'E4', 349.23: 'F4', 369.99: 'F#4/ Gb4', 392: 'G4', 415.3: 'G#4/ Ab4', 440: 'A4', 466.16: 'A#4/ Bb4', 493.88: 'B4', 523.25: 'C5', 554.36: 'C#5/ Db5', 587.32: 'D5', 622.26: 'D#5/ Eb5', 659.26: 'E5', 698.46: 'F5', 739.99: 'F#5/ Gb5', 783.99: 'G5', 830.61: 'G#5/ Ab5', 880: 'A5', 932.33: 'A#5/ Bb5', 987.77: 'B5'}
letters={'G3': 'A', 'G#3/ Ab3': 'B', 'A3': 'C', 'A#3/ Bb3': 'D', 'B3': 'E', 'C4': 'F', 'C#4/ Db4': 'G', 'D4': 'H', 'D#4/ Eb4': 'I', 'E4': 'J', 'F4': 'K', 'F#4/ Gb4': 'L', 'G4': 'M', 'G#4/ Ab4': 'N', 'A4': 'O', 'A#4/ Bb4': 'P', 'B4': 'Q', 'C5': 'R', 'C#5/ Db5': 'S', 'D5': 'T', 'D#5/ Eb5': 'U', 'E5': 'V', 'F5': 'W', 'F#5/ Gb5': 'X', 'G5': 'Y', 'G#5/ Ab5': 'Z', 'A5': ' ', 'A#5/ Bb5': '.', 'B5': '\n'}
np.set_printoptions(threshold=sys.maxsize)
CHUNK = 2048 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
FORMAT = pyaudio.paFloat32
METHOD = "default"
HOP_SIZE = CHUNK//2
PERIOD_SIZE_IN_FRAME = HOP_SIZE

# get the closest note that you are playing, don't have to worry about intonation that much
def get_closest_note(pitch):
    note=""
    min_diff=1000 # highest note mapped is around 1000hz
    for key_pitch in pitches.keys():
        curr_diff=abs(key_pitch-pitch)
        if(curr_diff<min_diff):
            note=pitches[key_pitch]
            min_diff=curr_diff
            
    return note
            
#Set up mic to get audio stream from 
mic=pyaudio.PyAudio()
stream=mic.open(format=FORMAT,channels=1,rate=RATE,input=True,frames_per_buffer=PERIOD_SIZE_IN_FRAME)

# Setup pitch detector using Aubio
pitchDetector= aubio.pitch(METHOD,CHUNK,HOP_SIZE,RATE)
pitchDetector.set_unit("Hz")
pitchDetector.set_silence(-40)
#for _ in range(10000):
while True: 
    data = np.fromstring(stream.read(PERIOD_SIZE_IN_FRAME),dtype=aubio.float_type)
    pitch=pitchDetector(data)[0]
    if(pitch>190 and pitch<1000):
        print(letters[get_closest_note(pitch)],end="")
        time.sleep(0.1)
stream.stop_stream()
stream.close()
mic.terminate()


