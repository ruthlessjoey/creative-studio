"""Synthesized soundtrack for Matcha (no third-party audio): calm pentatonic plucks, ice clinks, pour, whisk-like texture."""
import json, math, random, struct, wave
from pathlib import Path

def load_timing():
    s = (Path(__file__).parent / "timing.js").read_text()
    return json.loads(s[s.index("{"):s.rindex("}") + 1])

def synth(path, SR=44100):
    T = load_timing(); DUR = T["dur"]; n = int(SR * DUR); random.seed(5)
    L = [0.0] * n; R = [0.0] * n
    def add(t0, dur, fn, g, pan=0.0):
        i0 = int(t0 * SR); gl = g * (1 - pan) ** .5 if pan > 0 else g; gr = g * (1 + pan) ** .5 if pan < 0 else g
        for k in range(int(dur * SR)):
            i = i0 + k
            if 0 <= i < n:
                v = fn(k / SR); L[i] += gl * v; R[i] += gr * v
    def noise(t0, dur, g, a, b, shape):
        lp = lp2 = 0.0; i0 = int(t0 * SR)
        for k in range(int(dur * SR)):
            i = i0 + k
            if i >= n: break
            x = random.uniform(-1, 1); lp += a * (x - lp); lp2 += b * (lp - lp2)
            v = g * shape(k / SR / dur) * (lp - lp2); L[i] += v; R[i] += v
    # soft pad: D major add9 (D2 A2 D3 E3 F#3), slow swell, fade at end
    for f, g in ((73.42, .08), (110.0, .04), (146.83, .035), (164.81, .03), (185.0, .025)):
        add(0, DUR, lambda tau, f=f: min(1, tau / 2.5) * min(1, (DUR - tau) / 1.2) * (math.sin(2*math.pi*f*tau) + .4*math.sin(2*math.pi*f*1.002*tau)), g)
    # gentle pentatonic pluck phrase (D major pentatonic), koto-like decay
    notes = [(0.9,587.33),(1.6,659.25),(2.3,880.0),(3.0,739.99),(3.9,659.25),(4.6,587.33),(5.5,739.99),(6.2,880.0),(7.1,987.77),(7.9,739.99),(8.6,1174.66)]
    for t, f in notes:
        add(t, 1.6, lambda tau, f=f: (1 - math.exp(-400*tau)) * math.exp(-3.2*tau) * (math.sin(2*math.pi*f*tau) + .35*math.sin(4*math.pi*f*tau) + .12*math.sin(6*math.pi*f*tau)), .055, pan=.25)
    # soft low pulse each 1.25 s
    t = 1.25
    while t < DUR - 1.0:
        add(t, .5, lambda tau: math.exp(-9*tau) * math.sin(2*math.pi*(50 + 60*math.exp(-28*tau))*tau), .12); t += 1.25
    # whisk-like shimmer at the start (fast filtered noise bursts)
    for k in range(10):
        noise(.05 + k * .07, .06, 1.2, .6, .25, lambda x: math.sin(math.pi * x))
    # row whooshes
    for t in (.1, .22, .34, .46, .58):
        noise(t, .5, 1.2, .35, .04, lambda x: math.sin(math.pi * min(1, x)) ** 2)
    # ice: whoosh while falling then bright clinks on landing
    for i, t in enumerate(T["ice"]):
        f = (3136.0, 3520.0, 2960.0, 3322.0, 3729.0)[i]
        add(t, .45, lambda tau, f=f: math.exp(-18*tau) * (math.sin(2*math.pi*f*tau) + .6*math.sin(2*math.pi*f*1.51*tau) + .3*math.sin(2*math.pi*f*2.3*tau)), .16, pan=(-.3, .3, 0, -.2, .2)[i])
    # pour
    a, b = T["pour"]
    noise(a, .5, 1.0, .3, .03, lambda x: min(1, x * 4))
    noise(a + .5, b - a - .5, .55, .28, .03, lambda x: 1 - .2 * x)
    noise(b, .4, .5, .28, .03, lambda x: 1 - x)
    # bubbling gurgle during pour
    for k in range(40):
        t = a + .3 + k * (b - a - .4) / 40; f0 = 400 + random.random() * 500
        add(t, .08, lambda tau, f0=f0: math.exp(-40*tau) * math.sin(2*math.pi*f0*(1 + 2*tau*10)*tau), .04)
    # script write-on and footer taps
    noise(T["script"], .9, 1.2, .5, .12, lambda x: math.sin(math.pi * x) ** .5)
    for t in T["footer"]:
        noise(t - .05, .25, 1.0, .5, .1, lambda x: math.exp(-6*x))
    # camera macro swell
    m0, m1 = T["macro"]
    noise(m0, m1 - m0, .6, .3, .05, lambda x: math.sin(math.pi * x))
    # final chime
    for f, g in ((1174.66, .1), (1760.0, .05), (2349.3, .03)):
        add(T["ding"], 1.4, lambda tau, f=f: math.exp(-3.2*tau) * math.sin(2*math.pi*f*tau), g)
    peak = max(max(abs(v) for v in L), max(abs(v) for v in R)) or 1
    sc = .8 / peak
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<hh", int(max(-1, min(1, L[i]*sc)) * 32767), int(max(-1, min(1, R[i]*sc)) * 32767)) for i in range(n)))
