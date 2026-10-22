#!/usr/bin/env python3
"""Render projects/<name>/video/index.html to a 9:16 MP4 with synthesized audio.

Usage: python scripts/render_video.py coffee-launch
Needs: Python 3.9+, `pip install playwright` (+ chromium), and ffmpeg on PATH.
Optional: projects/<name>/audio/narration.m4a (or .mp3/.wav) is mixed in at 0.3 s.
No third-party audio files are used: music and sound effects are synthesized below.
"""
import math, os, random, re, struct, subprocess, sys, wave, shutil, json
from pathlib import Path

SR = 44100
DUR = 8.0
FPS = 30
W, H = 1080, 1920

# Timings must match video/index.html
ICE_LAND = [2.65, 2.85, 3.05, 3.25]
POUR_A, POUR_B = 3.4, 4.8
DING_T = 6.2


def synth_audio(path):
    random.seed(7)
    n = int(SR * DUR)
    buf = [0.0] * n

    def add(t0, dur, fn, gain):
        i0 = int(t0 * SR)
        for k in range(int(dur * SR)):
            i = i0 + k
            if i >= n:
                break
            buf[i] += gain * fn(k / SR)

    # warm pad (Cmaj7), slow attack, release over the last second
    for f in (130.81, 164.81, 196.00, 246.94, 261.63):
        def pad(tau, f=f):
            env = min(1.0, tau / 1.2) * min(1.0, max(0.0, (DUR - tau) / 1.0))
            return env * (math.sin(2*math.pi*f*tau) + 0.5*math.sin(2*math.pi*f*1.004*tau)) * (0.85 + 0.15*math.sin(2*math.pi*0.25*tau))
        add(0.0, DUR, pad, 0.035)

    # gentle plucked arpeggio
    notes = [523.25, 659.25, 783.99, 987.77]
    step = 0.5
    k = 0
    t = 0.5
    while t < DUR - 0.6:
        f = notes[k % 4]
        def pluck(tau, f=f):
            return (1 - math.exp(-250*tau)) * math.exp(-5*tau) * math.sin(2*math.pi*f*tau)
        add(t, 0.9, pluck, 0.05)
        k += 1
        t += step

    # ice clinks
    for i, tl in enumerate(ICE_LAND):
        f = [3136.0, 3520.0, 3322.0, 3729.0][i]
        def clink(tau, f=f):
            return math.exp(-20*tau) * (math.sin(2*math.pi*f*tau) + 0.6*math.sin(2*math.pi*f*1.51*tau))
        add(tl, 0.4, clink, 0.16)

    # pour: band-limited noise with bubbling modulation
    lp = 0.0
    lp2 = 0.0
    i0 = int(POUR_A * SR)
    for k in range(int((POUR_B - POUR_A) * SR)):
        i = i0 + k
        tau = k / SR
        x = random.uniform(-1, 1)
        lp += 0.33 * (x - lp)
        lp2 += 0.035 * (lp - lp2)
        band = lp - lp2
        env = min(1.0, tau / 0.12) * min(1.0, ((POUR_B - POUR_A) - tau) / 0.25)
        mod = 0.8 + 0.2 * math.sin(2*math.pi*9*tau)
        buf[i] += 0.55 * env * mod * band

    # price ding
    def ding(tau):
        return math.exp(-5*tau) * (math.sin(2*math.pi*1174.66*tau) + 0.35*math.sin(2*math.pi*2349.3*tau))
    add(DING_T, 1.6, ding, 0.12)

    peak = max(abs(v) for v in buf) or 1.0
    scale = 0.8 / peak
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, v*scale)) * 32767)) for v in buf))


def find_gsap(root):
    """Local GSAP build so rendering is deterministic and works offline: $GSAP_DIR, else node_modules/gsap/dist."""
    for c in (os.environ.get('GSAP_DIR'), str(root / 'node_modules' / 'gsap' / 'dist')):
        if c and (Path(c) / 'gsap.min.js').exists():
            return Path(c)
    return None


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r'[a-z0-9-]+', sys.argv[1]):
        sys.exit('usage: render_video.py <project-name>   (lowercase letters, digits, hyphens)')
    name = sys.argv[1]
    root = Path(__file__).resolve().parent.parent
    vdir = root / 'projects' / name / 'video'
    html = vdir / 'index.html'
    if not html.exists():
        sys.exit(f'missing {html}')
    out_dir = vdir / 'out'
    out_dir.mkdir(exist_ok=True)
    wav = out_dir / 'audio-synth.wav'
    mp4 = out_dir / f'{name}-9x16.mp4'
    frames_dir = out_dir  # nothing is written per frame; frames are piped

    global DUR, FPS
    tj = vdir / 'timing.js'
    if tj.exists():  # project-defined timing + soundtrack
        t = json.loads(tj.read_text()[tj.read_text().index('{'):tj.read_text().rindex('}') + 1])
        DUR, FPS = float(t['dur']), int(t['fps'])
    print('1/3 synthesizing audio...', flush=True)
    if (vdir / 'audio.py').exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location('project_audio', vdir / 'audio.py')
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        mod.synth(wav, SR)
    else:
        synth_audio(wav)

    narr = None
    for ext in ('m4a', 'mp3', 'wav'):
        c = root / 'projects' / name / 'audio' / f'narration.{ext}'
        if c.exists():
            narr = c
            break
    print('   narration:', narr if narr else 'none (music + sound effects only)')

    print('2/3 rendering frames...', flush=True)
    from playwright.sync_api import sync_playwright
    total = int(DUR * FPS)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
           '-i', str(wav)]
    if narr:
        cmd += ['-i', str(narr)]
        cmd += ['-filter_complex',
                '[1:a]volume=0.45[m];[2:a]adelay=300|300,volume=1.6[n];'
                '[m][n]amix=inputs=2:duration=first:dropout_transition=0,volume=2,alimiter=limit=0.95[a]',
                '-map', '0:v', '-map', '[a]']
    else:
        cmd += ['-filter_complex', '[1:a]alimiter=limit=0.95[a]', '-map', '0:v', '-map', '[a]']
    cmd += ['-t', str(DUR), '-c:v', 'libx264', '-preset', 'slow', '-crf', '26', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-movflags', '+faststart', str(mp4)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': W, 'height': H})
        gdir = find_gsap(root)
        if gdir:
            page.route(re.compile(r'.*/(gsap|ScrollTrigger)\.min\.js'),
                       lambda r: r.fulfill(path=str(gdir / r.request.url.rsplit('/', 1)[1]), content_type='application/javascript'))
            print('   GSAP from', gdir)
        page.goto(html.as_uri() + '?render=1')
        page.wait_for_function('typeof window.renderFrame === "function"', timeout=30000)
        page.evaluate('document.fonts.ready')
        for i in range(total):
            page.evaluate(f'window.renderFrame({i / FPS})')
            ff.stdin.write(page.screenshot(type='jpeg', quality=95))
        browser.close()
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit('ffmpeg failed')

    print('3/3 checking output...', flush=True)
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type,codec_name,width,height,duration', '-of', 'json', str(mp4)]))
    for s in info['streams']:
        print('  ', s)
    size_mb = mp4.stat().st_size / 1e6
    print(f'   file: {mp4.relative_to(root)}  {size_mb:.2f} MB')
    wav.unlink(missing_ok=True)
    print('DONE')


if __name__ == '__main__':
    main()
