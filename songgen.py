import wave
import random
import struct

from math import *

fr = 44100.0/8.0

def clip(x, lb=-1, ub=1):
    if x > ub:
        return ub
    if x < lb:
        return lb
    return x


class Note:
    def __init__(self, n, volume, start, length):
        self.frequency = 440.0 * pow(2, n/12.0)
        self.start = start
        self.length = length
        self.volume = volume
        
        self.fconst = self.frequency * pi * 2.0
        self.dampconst = dampconst = -5.0/self.length
        
    def calc(self, t):
        if t < self.start:
            return 0
        if t > (self.get_end()):
            return 0
        t -= self.start
        return self.volume*sin(t*self.fconst)*exp(t*self.dampconst)

    def get_end(self):
        return self.start + self.length

class Song:
    def __init__(self):
        self.parts = []
        
    def add_note(self, n, volume, start, length):
        self.parts.append(Note(n, volume, start, length))
        
    def write_wav(self, filename, sampwidth=2):
        mono = []
        
        max_end = 0
        
        for part in self.parts:
            if part.get_end() > max_end:
                max_end = part.get_end()
                
        frames = int(max_end * fr)
        
        print "Calculating %s frames with %s parts" % (frames, len(self.parts))
        
        max_a = 0
        active_parts = self.parts
        for frame in xrange(frames):
            t = frame / fr
            a = 0.0
            dead_parts=[]
            for part in active_parts:
                if part.get_end() < t:
                    dead_parts.append(part)
                else:
                    a += part.calc(t)
            for part in dead_parts:
                active_parts.remove(part)
                
            if abs(a) > max_a:
                max_a = abs(a)
                
            mono.append(a)
            
        for i in xrange(len(mono)):
            mono[i] /= float(max_a)
    
        channels = [mono,]
        nchannels = len(channels)
        nframes = len(channels[0])
        
        print "nchannels: %s sampwidth: %s framerate: %s nframes: %s" % (nchannels, sampwidth, fr, nframes)

        w = wave.open(filename, 'w')
        w.setparams((nchannels, sampwidth, fr, 0, 'NONE', 'not compressed'))

        max_amplitude = float(int((2 ** (sampwidth * 8)) / 2) - 1)
        
        frameparts = []
        for i in xrange(nframes):
            for j in xrange(nchannels):
                val = int(max_amplitude*channels[j][i])
                frameparts.append(struct.pack('h', val))

        rawframes = ''.join(frameparts)

        w.writeframes(rawframes)

# This is a pentatonic scale so pretty much any melody will sound good.
notes = [3, 5, 7, 10, 12]
prg_len = random.randint(3, 7)

prg = [random.choice(notes) for i in xrange(prg_len)]

l = 1
dif = 0.3

main_volume = 0.5
low_volume = 0.5

song = Song()
start = 0
for x in range(100):
    song.add_note(random.choice(notes), main_volume, start, l)
    if (x%4) == 0:
        song.add_note(random.choice(notes)-24, low_volume, start, l*4)

    low_volume += random.gauss(0, 0.1)
    main_volume += random.gauss(0, 0.1)
    low_volume = clip(low_volume, 0.3, 0.7)
    main_volume = clip(low_volume, 0.3, 0.7)

    start+=dif
    
song.write_wav('song.wav')