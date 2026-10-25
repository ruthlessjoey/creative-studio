#!/usr/bin/env python3
"""Placeholder foley for the Iced Matcha film (python stdlib only): room tone, soft cut whooshes, ice clinks, liquid pour.
These are SYNTHESIZED stand-ins, not recordings. Replace hyperframes/assets/audio/foley.wav with real foley when you have it.
Usage: python projects/iced-matcha/audio/make_foley.py"""
import math, random, struct, wave
from pathlib import Path
SR = 44100; DUR = 10.0; N = int(SR * DUR); random.seed(17)
buf = [0.0] * N

def add_noise(t0, dur, gain, lp_a, hp_b, env):
    lp = lp2 = 0.0; i0 = int(t0 * SR)
    for k in range(int(dur * SR)):
        i = i0 + k
        if i >= N: break
        x = random.uniform(-1, 1); lp += lp_a * (x - lp); lp2 += hp_b * (lp - lp2)
        buf[i] += gain * env(k / SR / dur) * (lp - lp2)

def add_tone(t0, dur, fn, gain):
    i0 = int(t0 * SR)
    for k in range(int(dur * SR)):
        i = i0 + k
        if i >= N: break
        buf[i] += gain * fn(k / SR)

# room tone: very quiet low-passed noise with slow movement, fades in/out
add_noise(0, DUR, .22, .05, .004, lambda x: min(1, x * 12) * min(1, (1 - x) * 6) * (.8 + .2 * math.sin(x * 9)))
# soft whooshes on cuts (rotate center so no two are identical)
for k, t in enumerate((1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)):
    a = (.22, .3, .26, .34)[k % 4]
    add_noise(t - .12, .38, .55, a, .03, lambda x: math.sin(math.pi * min(1, x)) ** 2)
# ice clinks (scene 2): short filtered noise tick plus a quiet glassy ring, three takes
for t, f, g in ((1.38, 3380, .10), (1.62, 4120, .08), (1.86, 2960, .09)):
    add_noise(t, .05, 1.2, .8, .3, lambda x: math.exp(-6 * x))
    add_tone(t, .35, lambda tau, f=f: math.exp(-22 * tau) * (math.sin(2*math.pi*f*tau) + .5*math.sin(2*math.pi*f*1.47*tau)), g)
# liquid pour (scene 3): band noise with bubbling modulation
add_noise(2.1, .95, .85, .27, .035, lambda x: min(1, x * 5) * min(1, (1 - x) * 4) * (.8 + .2 * math.sin(x * 70)))
for k in range(26):
    t = 2.2 + k * .03 + random.random() * .02; f0 = 380 + random.random() * 520
    add_tone(t, .07, lambda tau, f0=f0: math.exp(-45 * tau) * math.sin(2*math.pi*f0*(1 + 14*tau)*tau), .035)
peak = max(abs(v) for v in buf) or 1; sc = .7 / peak
out = Path(__file__).resolve().parents[1] / 'hyperframes' / 'assets' / 'audio' / 'foley.wav'
with wave.open(str(out), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, v * sc)) * 32767)) for v in buf))
print('wrote', out)
