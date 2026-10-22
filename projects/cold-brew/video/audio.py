"""Synthesized soundtrack for Cold Brew (no third-party audio). Timings come from timing.js so picture and sound stay locked."""
import json, math, random, re, struct, wave
from pathlib import Path

def load_timing():
    s = (Path(__file__).parent / "timing.js").read_text()
    return json.loads(s[s.index("{"):s.rindex("}") + 1])

def synth(path, SR=44100):
    T = load_timing(); DUR = T["dur"]; n = int(SR * DUR); random.seed(11)
    L = [0.0] * n; R = [0.0] * n
    def add(t0, dur, fn, g, pan=0.0):
        i0 = int(t0 * SR); gl = g * (1 - pan) ** .5 if pan > 0 else g; gr = g * (1 + pan) ** .5 if pan < 0 else g
        for k in range(int(dur * SR)):
            i = i0 + k
            if 0 <= i < n:
                v = fn(k / SR); L[i] += gl * v; R[i] += gr * v
    def noise(t0, dur, g, a, b, shape):
        """band noise: one-pole lowpass a, subtract slower lowpass b; shape(tau/dur)->envelope"""
        lp = lp2 = 0.0; i0 = int(t0 * SR)
        for k in range(int(dur * SR)):
            i = i0 + k
            if i >= n: break
            x = random.uniform(-1, 1); lp += a * (x - lp); lp2 += b * (lp - lp2)
            v = g * shape(k / SR / dur) * (lp - lp2); L[i] += v; R[i] += v
    # sub drone + warm pad (Fm9-ish), slow swell, fades last 1.2 s
    for f, g in ((55.0, .09), (87.31, .04), (130.81, .03), (155.56, .03), (207.65, .025)):
        add(0, DUR, lambda tau, f=f: min(1, tau / 2.0) * min(1, (DUR - tau) / 1.2) * (math.sin(2*math.pi*f*tau) + .4*math.sin(2*math.pi*f*1.003*tau)), g)
    # slow pulse (kick-like thump every 1.0 s from 1.0 s) very soft
    t = 1.0
    while t < DUR - 1.0:
        add(t, .35, lambda tau: math.exp(-12*tau) * math.sin(2*math.pi*(48 + 70*math.exp(-30*tau))*tau), .16); t += 1.0
    # sparse pluck melody
    for t, f in ((1.5, 622.25), (2.5, 783.99), (3.5, 932.33), (4.5, 783.99), (5.5, 622.25), (6.5, 830.61), (7.5, 932.33)):
        add(t, 1.2, lambda tau, f=f: (1 - math.exp(-300*tau)) * math.exp(-4*tau) * (math.sin(2*math.pi*f*tau) + .3*math.sin(4*math.pi*f*tau)), .04, pan=.3)
    # word whooshes + low hit
    for t in T["words"]:
        noise(t - .12, .5, 2.2, .4, .04, lambda x: math.sin(math.pi * min(1, x)) ** 2)
        add(t, .4, lambda tau: math.exp(-9*tau) * math.sin(2*math.pi*(60 + 80*math.exp(-25*tau))*tau), .22)
    # liquid streams: three pours, each a rising band-noise bed that continues quietly
    for t in T["streams"]:
        noise(t, 1.4, 1.1, .3, .03, lambda x: min(1, x * 3) * (1 - .55 * x))
        noise(t + 1.4, T["dur"] - t - 3.0, .28, .28, .03, lambda x: 1)
    # drips: pitch-dropping plink (water drop)
    for i, t in T["drips"]:
        f0 = (1500, 1250, 1750)[i]; land = t + .85
        add(land, .35, lambda tau, f0=f0: math.exp(-16*tau) * math.sin(2*math.pi*(f0*(1 + 1.2*math.exp(-40*tau)))*tau), .12, pan=(-.4, 0, .4)[i])
    # script write-on: soft scratchy noise
    noise(T["script"], .9, 1.4, .5, .12, lambda x: math.sin(math.pi * x) ** .5)
    # SLOW fill: rising tone + airy noise
    a, b = T["fill"]
    add(a, b - a, lambda tau: min(1, tau / .6) * min(1, (b - a - tau) / .5) * math.sin(2*math.pi*(180 + 90*tau/(b - a))*tau), .05)
    noise(a, b - a, .7, .35, .05, lambda x: math.sin(math.pi * x))
    # counter ticks
    for k in range(12):
        t = T["counter"][0] + (T["counter"][1] - T["counter"][0]) * (1 - (1 - k/12) ** 2 * 1.0) if False else T["counter"][0] + k * (T["counter"][1] - T["counter"][0]) / 12
        add(t, .05, lambda tau: math.exp(-90*tau) * math.sin(2*math.pi*2600*tau), .05)
    # footer line slaps
    for t in T["footer"]:
        noise(t - .05, .25, 1.0, .5, .1, lambda x: math.exp(-6*x))
    # final ding chord
    for f, g in ((1244.51, .1), (1864.66, .05), (2489.0, .03)):
        add(T["ding"], 1.4, lambda tau, f=f: math.exp(-3.5*tau) * math.sin(2*math.pi*f*tau), g)
    peak = max(max(abs(v) for v in L), max(abs(v) for v in R)) or 1
    sc = .8 / peak
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<hh", int(max(-1, min(1, L[i]*sc)) * 32767), int(max(-1, min(1, R[i]*sc)) * 32767)) for i in range(n)))
