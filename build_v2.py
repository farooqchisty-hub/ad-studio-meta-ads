"""Renders v2/index.html: Farooq's 6 picks reworked. usage: python3 build_v2.py"""
import html, os, re
from concepts_v2 import CONCEPTS, LPS

e = html.escape
TAG = {'Radar': 't-radar', 'Clone': 't-clone', 'AI influencers': 't-ai', 'Ads Agent': 't-ai', 'Static ads': 't-static'}

MOTION = [
 ('One stage, two lights', 'A single designed world: a dark, spotlit stage and a warm cream stage that swap on most cuts. Nothing ever cuts to black; every transition is a 2-frame motion-blur streak into a rack focus.', 'All'),
 ('Karaoke captions', 'Every spoken word appears as it is said: the newest word bold, older words fading to grey, one mint pill per sentence on the phrase that matters. Words enter at about 65% scale with a slight skew and settle in 180 ms.', 'All'),
 ('Time Tunnel', 'The camera flies down a runway of real Radar ads with day markers on the floor. Most ads fold flat and turn grey as they pass, their badges freezing on STOPPED. The winners stay upright and lit. Speed ramps, streaks, depth haze.', '1, 5, 8'),
 ('Clone Morph', 'A scan line detects the ad’s zones as wireframes; a headline word flips on its X axis into the new word; the old product bursts into particles that re-form as the new one; everything locks with a magnetic snap and a micro camera shake.', '1, 5, 8'),
 ('Exploded view', 'An ad separates into a glossy SURFACE plate and a glowing STRUCTURE plate, with labelled layers on mono leader lines; the surface is swapped while the structure stays.', '8'),
 ('Timeline transplant', 'A video ad unrolls into a film strip of shot slots; new shots drop into the same slots and both versions play side by side.', '8'),
 ('Portal dive', 'The camera pushes through a laptop or phone bezel into the product UI as a 3D world, and pulls back out, so screen moments never feel like a cutaway.', '3, 5'),
 ('Casting Wall', 'A curved 3D wall of creator tiles; phones light up as their creator speaks; at the reveal every tile flies into one formation.', '3, 10'),
 ('Agent assembly', 'The agent’s chat becomes physical cards: research chips tick in, casting cards fan out and flip, a voice waveform morphs into script lines, the script rolls onto a film strip, the strip feeds a phone that plays the result.', '3, 4, 10'),
 ('Match-cut objects', 'One object carries the story across scenes: the phone showing the creator’s reply turns round to play the finished ad; a tilted bottle becomes the portal to the next creator.', '4, 10'),
 ('Physics stickers and stamps', 'AI stickers, STOPPED stamps and role labels land with squash, overshoot and a slight tilt, one per beat, never as a pile.', 'All'),
 ('Mosaic lockup', 'Every ad tile used in the film streams into the Ad Studio by Brevo lockup, which collapses into the landing page’s own CTA button.', 'All'),
]
RULES = [
 'AI footage keeps a natural, motivated grade. No green glare, tint, glow or LUT on any AI video; brand color lives only in the graphics.',
 'Real Ad Studio UI only, rebuilt as HTML replicas from the 2x recordings, with real cursor paths from the click logs. Third-party brands in Radar shown as they are; every price in USD.',
 'Narration in a calm, complete, explanatory register (about 2 words a second on camera, about 2.2 for the narrator), continuous from first frame to last.',
 'Nothing sits still for more than about 1 second while someone speaks; readable surfaces face the camera within 8 degrees and hold for at least 1.2 seconds.',
 'Sound: one quiet cue per meaningful event, music about 27% under the voice and cut on its bar grid, ending on the real ending under the lockup.',
]

def concept(c):
    lp = LPS[c['lp']]
    words = sum(len(t.split()) for _, _, _, t, _ in c['script'])
    tags = ''.join(f'<span class="tag {TAG.get(f, "t-static")}">{e(f)}</span>' for f in c['feature'])
    script = ''.join(f'<div class="line"><div class="who">{e(w)}<small>{a}-{b} s{" · on camera" if nat else " · voiceover"}</small></div><p>{e(t)}</p></div>' for w, a, b, t, nat in c['script'])
    shots = ''.join(f'<tr><td class="tc">{e(t)} s</td><td>{p}</td><td>{e(s)}</td></tr>' for t, p, s in c['shots'])
    claims = ''.join(f'<li>{e(a)} <small>({e(b)})</small></li>' for a, b in c['claims'])
    return f'''
<article class="concept" id="c{c['n']}">
  <header><div class="cn">{c['n']:02d}</div><div><h3>{e(c['title'])}</h3>
  <div class="meta"><span class="lp lp{c['lp']}">{e(lp['name'])}</span>{tags}<span class="len">{c['length']} s</span><span class="fmt">{words} words</span></div>
  <p class="fmt" style="margin:6px 0 0">{e(c['fmt'])}</p></div></header>
  <p class="idea">{e(c['logline'])}</p>
  <p class="obs">{e(c['why'])}</p>
  <h4>Script</h4><div class="script">{script}</div>
  <h4>Shot by shot</h4>
  <div class="tbl"><table><thead><tr><th>Time</th><th>Picture and motion</th><th>Sound</th></tr></thead><tbody>{shots}</tbody></table></div>
  <dl class="prod"><dt>AI footage</dt><dd>{e(c['ai'])}</dd><dt>Product footage</dt><dd>{e(c['product'])}</dd><dt>Claims used</dt><dd><ul>{claims}</ul></dd><dt>Cost to make</dt><dd>{e(c['credits'])}</dd><dt>Watch out</dt><dd>{e(c['watch'])}</dd><dt>Lands on</dt><dd><a href="{lp['url']}" target="_blank" rel="noopener">{e(lp['url'])}</a>: “{e(lp['hero'])}”</dd></dl>
</article>'''

lp_cards = ''
for k, lp in LPS.items():
    ids = [c for c in CONCEPTS if c['lp'] == k]
    links = ', '.join(f'<a href="#c{c["n"]}">{c["n"]:02d} {e(c["title"])}</a>' for c in ids)
    lp_cards += f'<div class="card"><span class="lp lp{k}">{e(lp["name"])}</span><h4>{e(lp["hero"])}</h4><p>{e(lp["promise"])}</p><p><b>CTA in the ads:</b> {e(lp["cta"])} · 3 free ads, no credit card</p><p><b>Concepts:</b> {links}</p><p><a href="{lp["url"]}" target="_blank" rel="noopener">Open the page</a></p></div>'

motion = ''.join(f'<div class="card mv"><h5>Used in {e(w)}</h5><h4>{e(n)}</h4><p>{e(d)}</p></div>' for n, d, w in MOTION)
rules = ''.join(f'<li>{e(r)}</li>' for r in RULES)
cost_rows = ''.join(f'<tr><td><a href="#c{c["n"]}">{c["n"]:02d} {e(c["title"])}</a></td><td>{e(LPS[c["lp"]]["name"])}</td><td>{c["length"]} s</td><td>{e(c["credits"])}</td></tr>' for c in CONCEPTS)

body = f'''
<nav class="top"><div class="wrap"><a href="#changes">What changed</a><a href="#lps">Landing pages</a><a href="#motion">Motion</a>{''.join(f'<a href="#c{c["n"]}">{c["n"]:02d}</a>' for c in CONCEPTS)}<a href="#cost">Cost</a><a href="../">v1 report</a></div></nav>
<div class="wrap">
<section class="hero">
<div class="kicker">Ad Studio by Brevo · Meta video ads · concepts v2 · 27 Oct 2026</div>
<h1>Your six picks, rebuilt: 50 to 60 seconds, narrated properly, built on the two test pages.</h1>
<p class="lede">Concepts 01, 03, 04, 05, 08 and 10, each now sending traffic to one of the landing pages from the other session, with a full script, a shot-by-shot motion plan and its cost to make. Pick 4 or 5 and I move to storyboards.</p>
<span class="status">Waiting on you: pick 4 or 5</span>
</section>

<section id="changes">
<h2>What changed from v1</h2>
<div class="card"><ul class="tldr">
<li><b>Length:</b> every ad is now 55 to 60 seconds.</li>
<li><b>Narration:</b> rewritten in the university-professor register: complete sentences that explain the cause and then the effect, flowing without a break from the first frame to the last. No clipped lines. On-camera takes stay at or under 2 words a second so the generated speech stays clean.</li>
<li><b>Landing pages:</b> three concepts lead to LP A (Winners), three to LP B (Agent). Each ad uses that page’s own promise, CTA and offer (“3 free ads, no credit card”), and only claims the pages or the product already make.</li>
<li><b>Motion:</b> a 12-move motion system at the level of your getripping reference, with the signature move for each concept called out shot by shot.</li>
<li><b>AI footage:</b> natural grade only. No green glare, tint or glow on any AI video.</li>
<li><b>Your calls on v1:</b> third-party brands in Radar are shown as they are (no blur); every price on screen is in USD, and anything else gets cropped out.</li>
<li><b>On “batch for what?”:</b> I meant the four concepts I had recommended first in v1. The credits are the Ad Studio generations those ads need, because wherever an ad says a creator was made in Ad Studio, that creator has to actually be generated in Ad Studio (about 140 credits per 15 s creator video at 720p). The cost of each v2 concept is listed <a href="#cost">below</a>.</li>
</ul></div>
</section>

<section id="lps">
<h2>The two landing pages these ads feed</h2>
<div class="grid g2">{lp_cards}</div>
</section>

<section id="motion">
<h2>The motion system</h2>
<p class="lede">One designed world per film, the camera always moving, every transition carrying meaning. These are the 12 moves the six films are built from.</p>
<div class="grid g3">{motion}</div>
<h4>Rules for every film</h4>
<div class="card"><ul class="tldr">{rules}</ul></div>
</section>

<section id="concepts">
<h2>The six concepts</h2>
{''.join(concept(c) for c in CONCEPTS)}
</section>

<section id="cost">
<h2>What each one costs to make</h2>
<div class="tbl"><table><thead><tr><th>Concept</th><th>Lands on</th><th>Length</th><th>Ad Studio credits and other spend</th></tr></thead><tbody>{cost_rows}</tbody></table></div>
<p class="callout">All six together need about 2,100 Ad Studio credits; the account has 1,416. 03 and 10 are the expensive ones because every creator in them is generated in Ad Studio. Seedance for the three hosts is about $45 of the $109.81 treg balance.</p>
<p>Next, once you pick 4 or 5: a storyboard for each one (style frames for every shot plus a timed animatic with scratch narration), then production.</p>
</section>
<footer>v1 report (product usage, recorded journeys, references): <a href="../">farooqchisty-hub.github.io/ad-studio-meta-ads</a>. Glowday, Drift and the cold-brew brand are fictional demo brands.</footer>
</div>'''

extra_css = '''
.lp{font-size:12px;font-weight:800;padding:3px 10px;border-radius:999px;color:#fff}.lpA{background:#1D5FA8}.lpB{background:#6B2BB5}
.script{display:grid;gap:10px;margin:8px 0 16px}.line{display:grid;grid-template-columns:170px 1fr;gap:14px;background:var(--soft);border-radius:12px;padding:12px 14px}
.line .who{font-weight:700;font-size:14px}.line .who small{display:block;font:500 12px "JetBrains Mono",monospace;color:var(--mute);margin-top:2px}
.line p{margin:0;font-size:16px;line-height:1.65}
@media (max-width:640px){.line{grid-template-columns:1fr;gap:4px}}
.mv h4{margin:4px 0 6px}.mv p{font-size:14.5px;color:var(--mute)}
.concept td b{color:var(--forest)}
.concept ul{margin:0;padding-left:18px}
'''
shell = open('shell.html').read().replace('</style>', extra_css + '</style>').replace('<title>Ad Studio Meta Ads</title>', '<title>Ad Studio Concepts v2</title>')
page = shell.replace('{{BODY}}', body)
for bad in ('—', '–'):
    assert bad not in page, f'dash {bad!r}'
os.makedirs('v2', exist_ok=True)
open('v2/index.html', 'w').write(page)
print('v2/index.html', len(page) // 1024, 'KB')
