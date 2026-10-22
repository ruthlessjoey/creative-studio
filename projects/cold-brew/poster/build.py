"""Builds poster.svg (fonts embedded, no network) and poster.png. Run: python projects/cold-brew/poster/build.py"""
import base64, pathlib
from fontTools.ttLib import TTFont
ROOT=pathlib.Path(__file__).resolve().parents[3]; F=ROOT/"assets/fonts"
def b64(n): return base64.b64encode((F/n).read_bytes()).decode()
def width(fontfile,text,size):
    f=TTFont(F/fontfile); cm=f.getBestCmap(); hm=f["hmtx"]; upm=f["head"].unitsPerEm
    return sum(hm[cm[ord(c)]][0] for c in text)*size/upm
W,H=1080,1350; MARGIN=70; TARGET=W-2*MARGIN
rows=[("COLD","#2A160A"),("BREW","#5B3220"),("SLOW","#9A7A58")]
fs={t:TARGET/width("archivo-black-wide.woff",t,1) for t,_ in rows}
size=min(fs.values())  # same size for all rows; narrower rows get tracking
RH=size*0.80
y0=300
txt=[]
for i,(t,c) in enumerate(rows):
    w=width("archivo-black-wide.woff",t,size); ls=(TARGET-w)/(len(t)-1) if len(t)>1 else 0
    txt.append(f'<text x="{MARGIN}" y="{y0+i*RH+size*0.72:.0f}" font-family="AB" font-size="{size:.0f}" letter-spacing="{ls:.1f}" fill="{c}">{t}</text>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Cold Brew poster</title>
<desc id="d">Giant stacked words COLD, BREW, SLOW in coffee browns with three streams of cold brew pouring through the letters, a red script note "12 hours", and a spec-sheet footer.</desc>
<defs>
<style>
@font-face{{font-family:AB;src:url(data:font/woff;base64,{b64("archivo-black-wide.woff")})}}
@font-face{{font-family:AM;src:url(data:font/woff;base64,{b64("archivo-medium.woff")})}}
@font-face{{font-family:KS;src:url(data:font/woff;base64,{b64("kaushan.woff")})}}
@font-face{{font-family:DM;src:url(data:font/woff;base64,{b64("dmmono.woff")})}}
</style>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .9 -.28"/></filter>
<linearGradient id="liq" x1="0" x2="1"><stop offset="0" stop-color="#7A3E0C"/><stop offset=".35" stop-color="#C9731F"/><stop offset=".6" stop-color="#E39A3C"/><stop offset="1" stop-color="#8F4A10"/></linearGradient>
<filter id="sh" x="-20%" y="-5%" width="140%" height="110%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="#EDE8DE"/>
<!-- top spec row -->
<g font-family="DM" font-size="20" fill="#2A160A" letter-spacing="1.5">
<text x="{MARGIN}" y="70">COLD BREW ©</text><text x="{W/2}" y="70" text-anchor="middle">Nº 01 / BATCH</text><text x="{W-MARGIN}" y="70" text-anchor="end">STEEPED SLOW</text></g>
<!-- stacked words -->
{chr(10).join(txt)}
<!-- liquid streams: soft shadow, body, highlight, bulb drops -->
<clipPath id="below"><rect x="0" y="95" width="1080" height="1255"/></clipPath>
<g id="streams" clip-path="url(#below)">
<g filter="url(#sh)" opacity=".35" fill="#2A160A" transform="translate(14 8)">
<path d="M300 40 C312 120 306 190 300 330 L298 880 C298 900 262 900 262 880 L262 330 C256 190 262 120 270 40Z"/>
</g>
<path d="M258 0 L346 0 C334 90 326 200 318 330 L312 930 C312 962 292 972 280 972 C268 972 252 962 252 930 L246 330 C240 200 250 90 258 0Z" fill="url(#liq)"/>
<path d="M285 0 L296 0 C292 120 292 240 290 900" stroke="#FFF1D6" stroke-opacity=".55" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M610 0 L680 0 C672 110 662 240 656 330 L652 760 C652 790 636 800 630 800 C622 800 610 790 610 760 L604 330 C598 240 604 110 610 0Z" fill="url(#liq)"/>
<path d="M630 0 L640 0 C637 130 637 260 636 720" stroke="#FFF1D6" stroke-opacity=".5" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M830 0 L880 0 C872 100 866 220 862 330 L860 620 C860 645 850 652 845 652 C838 652 830 645 830 620 L826 330 C824 220 826 100 830 0Z" fill="url(#liq)"/>
<g fill="url(#liq)"><circle cx="280" cy="1008" r="19"/><ellipse cx="280" cy="1062" rx="9" ry="12"/><circle cx="632" cy="838" r="16"/><circle cx="846" cy="688" r="13"/><circle cx="846" cy="740" r="7"/>
<circle cx="560" cy="905" r="10"/><circle cx="598" cy="935" r="7"/><circle cx="900" cy="860" r="9"/></g>
<g fill="#FFF1D6" fill-opacity=".7"><circle cx="274" cy="1002" r="5"/><circle cx="627" cy="833" r="4"/><circle cx="842" cy="683" r="3"/></g>
</g>
<rect x="{MARGIN}" y="92" width="{TARGET}" height="3" fill="#2A160A"/>
<!-- red script accent -->
<text x="560" y="{y0+RH*1.5+size*0.72+20:.0f}" font-family="KS" font-size="150" fill="#B0121C" transform="rotate(-8 600 700)">12 hrs</text>
<!-- spec-sheet footer -->
<g stroke="#2A160A" stroke-width="3"><line x1="{MARGIN}" y1="1100" x2="{W-MARGIN}" y2="1100"/><line x1="{MARGIN}" y1="1190" x2="{W-MARGIN}" y2="1190"/><line x1="{MARGIN}" y1="1270" x2="{W-MARGIN}" y2="1270"/></g>
<g font-family="AM" font-size="30" fill="#2A160A"><text x="{MARGIN}" y="1150">STEEPED COLD, 12 HOURS*</text><text x="{W-MARGIN}" y="1150" text-anchor="end">NO HEAT. NO RUSH.</text></g>
<g font-family="DM" font-size="22" fill="#2A160A" letter-spacing="1"><text x="{MARGIN}" y="1236">NET 350 ML*</text><text x="{W/2}" y="1236" text-anchor="middle">SERVE OVER ICE</text><text x="{W-MARGIN}" y="1236" text-anchor="end">RP XX.XXX*</text>
<text x="{MARGIN}" y="1312" font-size="17" opacity=".75">* PLACEHOLDER: CONFIRM WITH BRAND</text></g>
<!-- grain on top -->
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".5" style="mix-blend-mode:multiply"/>
</svg>'''
out=pathlib.Path(__file__).parent/"poster.svg"; out.write_text(svg); print("svg",len(svg)//1024,"KB size",size)
