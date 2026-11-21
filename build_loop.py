#!/usr/bin/env python3
"""Builds loop/index.html: Fastlane film teardown, style playbook, and the Brevo Ads 'The Loop' script + screenplay."""
import pathlib, re

ROOT = pathlib.Path(__file__).parent
TIMELINE = pathlib.Path('/Users/azirahat/claude fc/brevo-fastlane-style/timeline.svg').read_text()
SRC = 'https://x.com/usefastlane/status/2116024028708196432'

def table(cols, rows, cls=''):
    h = ''.join(f'<th>{c}</th>' for c in cols)
    body = []
    for r in rows:
        if isinstance(r, str):
            body.append(f'<tr class="band"><td colspan="{len(cols)}">{r}</td></tr>')
            continue
        tds = ''.join(f'<td data-l="{cols[i]}">{v}</td>' for i, v in enumerate(r))
        body.append(f'<tr>{tds}</tr>')
    return f'<div class="tw"><table class="st {cls}"><thead><tr>{h}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'

def ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

# ---------------------------------------------------------------- teardown
TEAR = [
 'Station A: onboarding (0.00 to 9.60 s)',
 ['0.00', 'Warm off-white field. Helmet fades in at centre-top, blurred. Its LED visor reads "SENNA".', 'Blur 20 px to 0 and scale 0.9 to 1 over 0.5 s. A blue blob (left) and orange blob (right) drift.', 'Soft pad, almost silent.'],
 ['0.50', 'Input bar rises under the helmet: "Enter your website".', 'Fade and 12 px rise, 0.3 s.', ''],
 ['0.80', 'Headline "Enter the Fastlane, Grace". "Fastlane" in orange.', 'Blur-in, word by word, 0.3 s.', ''],
 ['1.30', 'Typing starts. The arrow button turns orange on the first key.', 'About one letter every 0.08 s.', 'Key ticks.'],
 ['1.75', '<b>Hard cut.</b> Macro close-up of the input bar, low angle. Helmet glow out of focus, top right.', 'Camera trucks right with the caret. Each letter ghosts in at 40 percent, then goes solid.', ''],
 ['2.90', 'Mouse cursor glides in from bottom right to the button.', '0.4 s ease-out.', ''],
 ['3.30', 'Click. Button dips. A dotted ring ripples out.', 'Press 0.1 s, ring 0.3 s.', 'Click hit.'],
 ['3.45', 'The URL breaks into orange particles. They stream up into the helmet. Visor scrolls "DRINKAG1".', 'Particle stream 0.4 s. Dolly back 0.5 s.', ''],
 ['4.00', 'Fly-through: product shots, UGC and ads stream from camera depth into the helmet. Mono status line: "Pulling product shots 22%", "Mapping the audience", "Learning the voice 100%".', 'Z-axis particle field with heavy motion blur. Dotted progress bar fills.', 'Build.'],
 ['5.50', 'Glow behind the helmet turns from orange to green: the AG1 brand colour.', '0.5 s colour cross-fade.', ''],
 ['6.00', 'Visor reads "READY".', 'LED snap.', '<b>Drop.</b> Full beat.'],
 ['6.30', 'A green brand-kit folder rises. Card 1 slides out: "Product", AG1 pouch, "Hero SKU", "Daily Foundational Nutrition".', 'Card rises 0.3 s. The folder lip overlaps it.', ''],
 ['7.60', 'Card flicks to "Palette": 6 greens with hex codes, "Deep greens, clean whites".', 'Flick swap, vertical blur, 0.15 s.', ''],
 ['8.00', '"Tone of voice": Science-backed, Simple, Warm, Never hypey, plus 3 sliders.', 'Flick swap. Slider dots settle.', ''],
 ['8.90', '"Your ads": 1,032 ads scanned, 528 days for the top ad, 48 percent discount-led, 2 organic posts a week.', 'Flick swap. Numbers count up.', ''],
 ['9.50', 'Cards drop into the folder. Label: "AG1, Brand learned" with a check.', 'Drop 0.2 s with a small overshoot.', ''],
 'Transition: the track swoop (9.60 to 11.00 s)',
 ['9.60', 'Camera cranes up. The folder sits on a dotted race track, seen from above.', 'Crane up and tilt down, 0.6 s.', ''],
 ['10.20', 'Swoop down to car level. A red F1 car races along the track. Dots behind it turn orange.', 'Whip with heavy directional blur.', 'Whoosh.'],
 ['11.00', 'Lands on a station pill: "B · Market research". A dotted stalk drops below it.', 'Ease-out settle, 0.3 s.', ''],
 'Station B: market research (11.00 to 17.30 s)',
 ['11.30', 'Header "Scanning competitor ads". A 3D arc carousel of real competitor ads.', 'Arc rotates. Far cards in soft focus.', ''],
 ['12.80', 'One ad comes forward: "How I beat afternoon sugar cravings". A stat card slides in: "278 to 482 days running. This one\'s printing money."', 'Push-in 0.4 s. Count-up 0.6 s. Orange underline draws.', ''],
 ['14.00', 'Chip: "Saved to memory", green check.', 'Pop, 0.2 s.', ''],
 ['14.60', 'Header morphs: "Reading 6,800 to 12,000+ reviews. Reddit, Amazon, Google".', 'Count-up over 1.2 s. The number is orange.', ''],
 ['15.20', 'Three review cards slide in. Key phrases highlighted. Tags: "+Energy", "+Taste", "+Convenience".', 'Stagger 0.15 s. Highlights wipe left to right.', ''],
 'Transition (17.30 to 18.50 s), then Station C: avatars (18.50 to 24.00 s)',
 ['17.30', 'Crane up to the track. Three cards (blue, green, red) ride on it. No pill: the cards are the station.', 'Crane and whip.', 'Whoosh.'],
 ['18.50', 'Header "Your Key Avatars". Blue card flips: "Biohacker, 25-45, 34%, $99/mo". Glow turns blue.', 'Y-axis flip 180 degrees, 0.5 s, motion blur.', ''],
 ['19.50', 'Three angle chips float around it, each with a source: "from your ads", "from organic trends", "from reviews".', 'Chips drift in from 3 sides, 0.3 s each.', ''],
 ['20.50', 'Green card flips: "Busy Professional", badge "Under-served". Glow turns green.', 'Same flip.', ''],
 ['22.00', 'Red card flips: "Fitness Lover". Glow turns red.', 'Same flip.', ''],
 ['23.00', 'All three line up, each with its own glow.', 'Settle.', ''],
 'Transition (24.00 to 25.20 s) to "D · Strategy"',
 'Station D, part 1: paid (25.20 to 47.80 s)',
 ['25.25', 'The station pill turns into a chat bubble. Helmet avatar on the left, name "Senna" above.', 'Pill pushes to camera, blurs and stretches into a bubble, 0.25 s. Orange glow blooms.', 'Beat cuts to stabs.'],
 ['25.70', 'Types: "Your top ads are fatiguing."', 'About 45 letters a second. Camera orbits slowly. Bubbles tilt about 10 degrees.', ''],
 ['26.50', 'Next bubble: "Let\'s launch 30 new ads. $5K a day, 7 days." "30" in orange.', 'Bubble stretches in from the left, skewed, 0.27 s.', ''],
 ['27.90', 'User reply, right side, solid orange: "Yes pls!" Avatar "G", name "Grace".', 'Pop, 0.15 s, overshoot. Camera tilts.', ''],
 ['28.40', '"Ok, remixing your competitors now."', '', ''],
 ['29.60', 'That bubble dissolves into swirling ink particles.', 'Particle swirl, 0.8 s.', ''],
 ['30.40', 'Particles re-form as a competitor ad: "Bloom, Competitor ad". A particle bridge labelled "Remixing for AG1" builds "AG1, Your remix" on the right.', 'Bridge flows left to right, 0.6 s.', '<b>Re-drop</b> at 30.0.'],
 ['31.80', 'Chips between the two: "Same hook". Under the remix: "For Fitness Lovers". Orange boxes outline the matching parts.', 'Box draws 0.2 s. Chips stagger.', ''],
 ['32.80', 'Next pair: "The truth about Huel" to "The truth about AG1". Chips: "Same headline", "Huel to AG1".', 'Fast slide swap.', ''],
 ['33.93', '<b>Hard cut.</b> "Want 40g protein" to "Want daily nutrition". "Same hook", "Same stat tiles".', 'Cut on the beat.', ''],
 ['35.03', '<b>Hard cut.</b> Creator Q&amp;A ad to the AG1 version. "Same Q&amp;A sticker", "Same study proof".', 'Cut on the beat.', ''],
 ['36.60', 'Bubble: "Plus some new ones based on winning formats today."', '', ''],
 ['38.00', 'A video card slides over the bubble. A 3D carousel of new formats, each with a chip "format, for avatar": AI podcast (a baby in headphones), Claymation, Chalkboard, Papermation, Breaking news, iMessage, Text on body.', 'Cylinder carousel. Cuts speed up: 2.3 s, 1.5 s, 0.3 s, 0.27 s.', 'The baby podcast plays with sound. Music ducks.'],
 ['43.00', 'The last card bursts into about 30 thumbnails. They spin in a vortex, then fly past camera. Only the glow is left.', 'Explosion 1.8 s, heavy blur.', ''],
 ['45.00', 'Bubble: "All 30 are ready to go live." An orange "Publish" button sits inside it.', '', ''],
 ['45.60', 'Cursor clicks Publish.', '', 'Click.'],
 ['46.00', 'Meta Ads Manager table, tilted in 3D. Camera scrolls 30 rows: toggles on, "Active".', 'Perspective about 25 degrees. Scroll 1.5 s.', ''],
 ['47.60', 'Chip: "Done. 30 ads are live."', '', ''],
 'Station D, part 2: organic (47.80 to 69.50 s)',
 ['48.00', 'The table shrinks up and out. Chat: "Competitors are lapping you on organic." "Let\'s launch 5 AI creators on IG, TikTok and Shorts."', '', 'Stabs again.'],
 ['50.50', 'Grace: "Wow bit harsh... but yes"', 'Comic beat.', ''],
 ['51.50', '"One creator per avatar. Approve the cast?"', '', ''],
 ['52.00', 'Five AI creator cards in a row, each with a handle and avatar tag. Cursor hovers "Jack".', 'Cards fan in.', '<b>Re-drop</b> at 52.0.'],
 ['53.50', 'Grace: "Can we make Jack a bit older?" Senna: "Sure."', '', ''],
 ['54.80', 'Push into Jack\'s card. His face changes through a pixel-mosaic dissolve. Counter: "Age 26, 27, 29, 33, 38".', 'Mosaic 0.9 s. Counter ticks.', ''],
 ['56.00', 'Grace: "Perfect, approve all". Green checks pop on all five cards.', 'Stagger 0.1 s, left to right.', 'Chime per check.'],
 ['56.50', 'Phone with a creator\'s IG profile. Bubble: "These are the videos I generated for you." Three videos play: "Day in the life", "Supplement stack", "Meme".', '', 'Creator audio: "This used to be my morning, 10 different pills. Now, one stick of AG1." Music ducks.'],
 ['62.00', 'The phone fans out into five phones. "Our US team are creating the accounts on your behalf now."', 'Profiles swap on cuts every 0.45 s (64.05 to 65.83).', ''],
 ['65.50', '"They will warm them up for 7 days, then post the content."', 'Video sets swap on 0.3 s cuts (66.3 to 67.2).', ''],
 ['67.00', 'Whip. "Scheduled to TikTok, Instagram and YouTube for you."', 'Whip blur, 0.2 s.', ''],
 ['67.80', 'Tilted "November 2026" calendar. Thumbnails fly into each day. Counter: "95 to 150 posts scheduled".', 'Fill over 1.5 s.', ''],
 'Transition (69.50 to 70.80 s), then Station E: insights (70.80 to 89.40 s)',
 ['70.80', 'Pill turns into a bubble. A checkered flag rises and waves behind it: "Lap 1 results are in."', '3D cloth flag.', 'Stab.'],
 ['71.90', 'Camera dives into the flag. The squares fill the frame, then shrink into tiles that clear away.', 'Dive 0.3 s. Hard cut at 72.0. Tiles clear in 0.4 s.', ''],
 ['72.40', '"Ad set 3 cooked. Felt like a FaceTime, not an ad." Video left. 3D bars right: Thumbstop 41% vs 25%, Hold rate 18% vs 8%, CPA $32 vs $59, ROAS 5.4x vs 2.1x.', 'Bars grow in a stagger. Numbers count up. Deltas in green.', ''],
 ['75.50', '"For lap 2, let\'s run 6 remixes of this winner." Six variants fan out behind it.', 'Fan, 0.4 s.', ''],
 ['76.50', '"And dw, I know about the Andromeda update. They\'re all visually distinct" with one emoji.', '', ''],
 ['78.50', 'Header: "Sophia had a breakout organic video." Views tick from 108K to 122K.', '', ''],
 ['79.50', '"For lap 2, let\'s run it as a Spark ad."', '', ''],
 ['81.00', 'The video flips into a Spark ad with a "Shop now" bar.', 'Y-flip, 0.5 s.', ''],
 ['82.50', 'Whip. "Btw, this is going viral right now. Check it out." A trend header with "1 of 3". Stats column: +640% this week, 48M views, 3.1x engagement, 0 brands using it.', 'Trend examples cycle: 1 of 3, 2 of 3, 3 of 3.', ''],
 ['86.00', '"I made a version for you." The card flips to "AG1, your version".', 'Y-flip.', '<b>Re-drop</b> at 87.0.'],
 ['88.60', '"Ready for Lap 2?"', '', ''],
 'Outro (89.40 to 97.25 s)',
 ['90.10', 'The helmet avatar flies out of the bubble to centre and grows.', '0.4 s.', 'Stabs.'],
 ['90.50', 'Visor scrolls "SENNA", then "PREPARING LAP 2".', 'LED marquee.', ''],
 ['92.00', 'Visor: "READY".', '', '<b>Re-drop</b> at 92.0.'],
 ['92.50', 'Crane up to the track. The car laps it, trailing every ad it made. Station pills tick green.', 'Crane and whip.', ''],
 ['94.75', '<b>Hard cut.</b> The car crosses "Point A". A ring of orange and green ticks bursts out.', 'Ring, 0.4 s.', ''],
 ['95.00', 'Hold on "Point A" and its dotted stalk. No logo.', 'Slow push.', 'Music resolves, fades from 95.5.'],
]

# ---------------------------------------------------------------- playbook
MOVES = [
 ['Blur-in reveal', 'Agent, headlines', '0.3 to 0.5 s. Blur 20 px to 0, scale 0.9 to 1.'],
 ['Ghost-letter typing', 'URL, every chat line', 'About 40 to 45 letters a second. Each letter at 40 percent, then solid.'],
 ['Text-to-particles absorb', 'URL into the agent', '0.4 s stream, then dolly back 0.5 s.'],
 ['Depth fly-through', 'Pulling assets', '2 s. Images fly from camera into the agent, heavy blur.'],
 ['Glow recolour', 'Brand learned, each persona', '0.5 s cross-fade. Colour means something.'],
 ['Card flick-swap', 'Brand kit', '0.15 s with vertical blur.'],
 ['Track swoop', 'Every section change', '1.0 to 1.4 s: crane up, chase the vehicle, land on a pill.'],
 ['Pill-to-bubble morph', 'Station into chat', '0.25 s. The label becomes the first bubble.'],
 ['Bubble stretch-in', 'Every chat line', '0.27 s, skewed, from the speaker\'s side.'],
 ['Dissolve and re-form', 'Chat into media', '0.8 s out as particles, 0.4 s back in as a card.'],
 ['Particle bridge', 'Source ad into new ad', '0.6 s, with a label on the bridge.'],
 ['Proof boxes and chips', 'Side-by-side pairs', 'Boxes draw in 0.2 s. Chips stagger 0.15 s.'],
 ['Accelerating carousel', 'Format reel', 'Cuts at 2.3, 1.5, 0.3, 0.27 s, then a burst.'],
 ['Shatter vortex', '30 ads made', '1.8 s. Thumbnails spin, then fly past camera.'],
 ['Pixel-mosaic change', 'Creator tweak', '0.9 s with a ticking counter.'],
 ['Y-flip reveal', 'Persona, Spark ad, your version', '0.5 s, 180 degrees, motion blur.'],
 ['3D bars with count-up', 'Results', 'Stagger 0.15 s a bar. Winner bars in the accent.'],
 ['Also used', 'Various', 'LED marquee, check-mark pops, beat-synced swaps, tilted table scroll, dive into a texture, radial burst ring.'],
]

# ---------------------------------------------------------------- brevo decisions
DECIDE = [
 ['Product', 'Fastlane, "Claude for Ads"', '<b>Brevo Ads</b> (ads.brevo.com)', 'Same category: an ad agent.'],
 ['Metaphor', 'F1 race track, laps', '<b>A metro loop line, weeks</b>', 'Original look. Ads run on a weekly loop. Stations already mean stops.'],
 ['Agent face', 'Helmet with an LED visor', '<b>The Brevo Ads capsule</b>: a glossy deep-green pod with a mint LED window, like the nose of a metro car', 'Own hero object. Keeps the LED trick.'],
 ['Vehicle', 'Red F1 car', 'The capsule rides the line itself', 'One hero, not two.'],
 ['Section marker', 'Checkered flag', 'Split-flap departure board', 'Native to the metro world.'],
 ['Accent', 'Orange #E56B20', 'Brevo green #0B996E. User bubbles deep green #006A43. LED mint #C0FFA5.', 'Brevo palette.'],
 ['"It learned you"', 'Glow turns AG1 green', 'Glow turns Rilo coral #E8674F', 'Same payoff.'],
 ['Demo brand', 'AG1 (real)', 'Rilo Peach Yuzu Prebiotic Soda (fictional, our store page)', 'No implied endorsement. 18 static clones and 1 video clone already made in-app on 10 Nov.'],
 ['User', 'Grace', 'Maya, Rilo\'s founder', ''],
 ['Competitor ads', 'Bloom, Huel', 'Olipop, Poppi, Liquid Death, Athletic Brewing (unblurred, per your rule)', 'Our clone sources already.'],
 ['Ending', '"Point A", no logo', 'The loop closes, then a 3.25 s launch lockup: "Introducing Brevo Ads. Clone any winning ad." plus the free-ads offer', 'A launch film must end on the name and where to get it.'],
 ['Format', '1280 x 720, 60 fps, music only', '1920 x 1080, 60 fps, 113.2 s, voiceover', 'Longer than the source because the voice leads the picture.'],
]
SWAPS = [
 ['Reads 12,000+ reviews', 'Takes apart 40 winners: hooks, layouts, offers', 'Matches "the agent takes it apart".'],
 ['Customer avatars from data', 'Three angles', 'Brevo Ads quick-create works by angle.'],
 ['Publishes to Meta Ads Manager', 'Exports all 30 to the Library, every size', 'Swap back if direct publishing exists.'],
 ['US team creates and warms accounts', 'Captions per platform and a 30-day post plan', 'No account-creation claim.'],
 ['Agent reads results itself', 'Maya drops her Week 1 report into the chat', 'The human brings the data. The agent acts on it.'],
 ['Age slider on a creator', 'Re-cast from the presenter library', '"Try someone older" instead of aging a face.'],
 ['Viral trend radar', 'Ad Radar caught a new winner this morning', 'A real Brevo Ads feature.'],
 ['Organic breakout to Spark ad', 'Winning video also made as a static', 'Uses static creation, not Spark ads.'],
]

# ---------------------------------------------------------------- script
SCRIPT = [
 'A · Start: your brand',
 ['0.80', 'Headline', 'Welcome to <span class="g">Brevo Ads</span>, Maya'],
 ['0.00', 'LED', 'HELLO'],
 ['1.30', 'Input', 'drinkrilo.com'],
 ['3.45', 'LED', 'DRINKRILO.COM'],
 ['4.00', 'Status', 'Pulling product photos 22% · Reading the store page 54% · Finding your offer 78% · Learning the voice 100%'],
 ['6.00', 'LED', 'READY'],
 ['6.60', 'Card', 'Product · Peach Yuzu Prebiotic Soda · Hero SKU · 12-pack, $36'],
 ['7.60', 'Card', 'Colours · Coral, cream, ripe peach'],
 ['8.00', 'Card', 'Voice · Bright · Playful · Never preachy'],
 ['8.90', 'Card', 'Facts · 9 g prebiotic fiber · 3 g sugar · 35 calories a can'],
 ['9.50', 'Folder', 'Rilo · Brand learned ✓'],
 'B · Ad Radar',
 ['11.00', 'Station', 'B · Ad Radar'],
 ['11.30', 'Header', 'Scanning winning ads in your category'],
 ['12.80', 'Stat card', 'Olipop · Live for <span class="g">182 days</span> · Still running. That\'s a winner.'],
 ['14.00', 'Chip', 'Saved to Radar ✓'],
 ['14.60', 'Header', 'Taking apart <span class="g">40</span> winners · Hooks · Layouts · Offers'],
 ['15.20', 'Tags', '+Hook · +Layout · +Offer · Saved to Radar ✓'],
 'C · Angles',
 ['18.50', 'Header', 'Your three angles'],
 ['18.80', 'Card 1', 'Gut-health fans · chips: "9 g prebiotic fiber" (from your label) · "A soda your gut likes" (from Radar winners) · "Tastes like summer" (from your reviews)'],
 ['20.50', 'Card 2', 'Soda quitters · badge: Under-served · chips: "3 g sugar, full fizz" (from your label) · "The 3 pm soda swap" (from Radar winners) · "No artificial sweeteners" (from your store page)'],
 ['22.00', 'Card 3', 'Mocktail hosts · chips: "Peach yuzu spritz" (from Radar winners) · "Caffeine-free, so 9 pm is fine" (from your store page) · "Looks fancy on the table" (from your photos)'],
 'D · Make',
 ['25.25', 'Brevo Ads', 'You saved 6 winners.'],
 ['26.50', 'Brevo Ads', 'Let\'s make <span class="g">30</span> ads from them. Statics and video.'],
 ['27.90', 'Maya', 'Yes pls!'],
 ['28.40', 'Brevo Ads', 'Cloning them for Rilo now.'],
 ['30.40', 'Chips', 'Olipop · Winning ad → "Cloning for Rilo" → Rilo · Your clone · Same hook · For Gut-health fans'],
 ['32.80', 'Chips', 'Graza → Rilo · Same headline · For Soda quitters'],
 ['33.93', 'Chips', 'Liquid Death → Rilo · Same comparison · Same proof tiles · For Soda quitters'],
 ['35.03', 'Chips', 'Poppi video → Rilo video · Scene by scene · Same pacing · For Mocktail hosts'],
 ['36.60', 'Brevo Ads', 'Plus new videos, made from your <span class="g">product photos</span>.'],
 ['38.00', 'Format chips', 'Creator-style · Product drop · Stop motion · Dolly shot · Sliding products · Bold and cinematic (each "for" an angle)'],
 ['38.20', 'Creator clip', '"Wait, wait, this is soda? It literally tastes like a peach ring. Three grams of sugar? Okay, I\'m switching. Bye."'],
 ['45.00', 'Brevo Ads', 'All <span class="g">30</span> are ready to launch. [Export all]'],
 ['47.60', 'Chip', 'Done. 30 ads, every size.'],
 ['48.40', 'Brevo Ads', 'Your rivals post creator videos daily. You post <span class="g">monthly</span>.'],
 ['49.40', 'Brevo Ads', 'Let\'s cast <span class="g">5</span> AI creators for TikTok, Reels and Shorts.'],
 ['50.50', 'Maya', 'Ouch. Fair. Yes.'],
 ['51.50', 'Brevo Ads', 'Here\'s the cast. Approve?'],
 ['52.00', 'Cards', '@jess.sips (Soda quitters) · @mia.mocktails (Mocktail hosts) · @leo.lifts (Gut-health fans) · @ava.after5 (Mocktail hosts) · @sam.swaps (Soda quitters)'],
 ['53.50', 'Maya', 'Can we try someone older for Leo?'],
 ['54.50', 'Brevo Ads', 'Sure.'],
 ['54.80', 'Counter', 'Option 1 of 4 · 2 of 4 · 3 of 4'],
 ['56.00', 'Maya', 'Perfect, approve all'],
 ['56.50', 'Brevo Ads', 'These are the videos I made for you.'],
 ['56.80', 'Chips', 'Day in the life · 3 pm swap · Taste test'],
 ['57.00', 'Creator clip', '"Honestly? This used to be my 3 p.m. soda. Now it\'s a Rilo. Way better."'],
 ['62.00', 'Brevo Ads', 'Captions written for TikTok, Instagram and YouTube.'],
 ['65.50', 'Brevo Ads', '5 creators, 12 videos each. <span class="g">60</span> in all.'],
 ['67.00', 'Brevo Ads', 'Your next <span class="g">30 days</span>, planned.'],
 ['67.60', 'Counter', '0 → 60 posts ready'],
 'E · Week 1',
 ['70.80', 'Maya', '[file: week-1-results.csv] Week 1 is in!'],
 ['71.20', 'Board', 'WEEK 1 RESULTS'],
 ['72.40', 'Header', '<span class="g">Ad 4</span> won. · It felt like a friend\'s story, not an ad.'],
 ['72.80', 'Chart', 'Thumbstop 38% (vs 22% avg) · Hold rate 16% (vs 7% avg) · CPA $24 (vs $41) · ROAS 4.8x (vs 2.0x) · Demo data'],
 ['75.50', 'Brevo Ads', 'For week 2, let\'s make <span class="g">6</span> clones of your own winner.'],
 ['76.50', 'Brevo Ads', 'New creators, new kitchens. Same winning script 🍑'],
 ['78.50', 'Brevo Ads', 'Your winner works as a <span class="g">static</span> too.'],
 ['79.60', 'Chip', 'Ad 4 · Static · For your feed (the Rilo "Crush your cravings" static)'],
 ['82.50', 'Brevo Ads', 'Btw, Radar caught a <span class="g">new winner</span> this morning.'],
 ['83.30', 'Stats', 'Real ads from the Meta Ad Library: Vita Pop (2 days live, 5 versions running) · wildwonder (1 day live) · Kivvy (5 days live)'],
 ['86.70', 'Chip', 'Rilo · Your version · Same format, your can, your creator'],
 ['86.00', 'Brevo Ads', 'I made a <span class="g">Rilo version</span> for you.'],
 ['88.60', 'Brevo Ads', 'Ready for week 2?'],
 'Outro',
 ['90.50', 'LED', 'BREVO ADS → NEXT: WEEK 2'],
 ['92.00', 'LED', 'READY'],
 ['93.40', 'Station', 'A · Start'],
 ['94.05', 'Kicker', 'Introducing'],
 ['94.12', 'Wordmark', 'Brevo Ads (capsule beside it, LED READY)'],
 ['94.85', 'Line', 'Clone any winning ad.'],
 ['95.15', 'CTA', 'ads.brevo.com · Your first 3 ads are free'],
]


# ---------------------------------------------------------------- voice and picture (v5, the voice leads)
VOP = [
 ['0.0 to 8.4', 'This is Maya. She makes a really good peach soda called Rilo, but she never has time for ads. So she pastes one link into <span class="g">Brevo Ads</span>.', 'Her store in a browser. Slow push on the can. Her to-do note: New flavor ✓, Restock cans ✓, Make ads ☐ circled in red. She selects the URL, "Copied". Cut to the real Brevo Ads "Paste a link" dialog. Her link is pasted, the camera runs along it, and the cursor clicks "Fetch product".'],
 ['8.8 to 16.9', 'Brevo Ads reads her store like a very keen new hire, and learns her product, her colours, her tone, and every fact on the can.', 'The URL streams into the capsule as dots. Her photos fly past. LED READY, the beat drops. The real Rilo product memory page rises. Each word gets a mark on the real page: Her product (header), Her colors (How it must look), Her tone (What we can say), Every fact on the can (Facts).'],
 ['17.5 to 28.6', 'Then <span class="g">Ad Radar</span> finds ads that are already winning in her category. This Olipop ad has run for a hundred and eighty-two days, and nobody pays for an ad that long unless it sells.', 'Ride to B. The real Ad Radar opens on Food & Drink: "Long-running winners" and "Her category" are marked. The real Olipop ad opens with its own video playing; "6 months active" is marked as 182 days live, then "Active" as still running.'],
 ['29.0 to 32.9', 'So it takes the winners apart: the hook, the layout and the offer.', '"Taking apart 40 winners". Hook, Layout and Offer are outlined on three real winners as each word is spoken.'],
 ['33.6 to 41.2', 'Next, it finds three ways to talk about Rilo: to gut-health fans, to people quitting soda, and to whoever hosts mocktail night.', 'Ride to C. Three angle cards flip to video, one per phrase, each with two reasons on leader lines.'],
 ['42.0 to 54.7', 'Then it suggests thirty new ads, and Maya says yes, obviously. Every winner gets cloned for Rilo: the same hook here, the same layout there, and her own numbers on this one. It even clones video, scene by scene.', 'Ride to D. "Let\'s make 30 new ads from your winners." Maya: "Yes pls!" Four pairs, each joined by a drawn bridge on its phrase: Olipop, Same hook. Graza, Same layout. Liquid Death, Her own numbers. Poppi video, Scene by scene.'],
 ['55.2 to 63.3', 'It makes fresh videos from her product photos too. <i>Jess: "Wait, wait, this is soda? It literally tastes like a peach ring."</i> That\'s thirty ads, ready to launch, in every size.', '"Made from your product photos": six video styles. Jess\'s take plays with its own sound. 30 ads burst out. The real Rilo product page, Ads tab: "30 ads, ready to launch" is marked and the Ads made grid scrolls. "Every size: 1:1 · 4:5 · 9:16".'],
 ['64.1 to 75.0', 'Her rivals post creator videos every day. Maya posts about once a month. So Brevo Ads casts five A.I. creators, and when she wants someone a little older, it swaps him in.', '"Your rivals post creator videos daily. You post monthly." Maya: "Ouch. Fair. Yes." "Let\'s cast 5 AI creators for TikTok, Reels and Shorts." Five creators. "Can we try someone older for Leo?" The mosaic re-casts him. "Perfect, approve all."'],
 ['76.1 to 83.7', 'The creators film the videos. <i>Leo: "Honestly, this used to be my 3 p.m. soda."</i> It writes the captions, and her next thirty days are planned.', '"These are the videos I made for you." Three creator videos; Leo\'s line plays. Captions for TikTok, Instagram and YouTube. "Your next 30 days, planned." The calendar fills.'],
 ['84.6 to 89.6', 'A week later, Maya drops in her results. Ad four won, because it felt like a friend\'s story.', 'Ride to E, Week 1. "Week 1 is in!" Split-flap board: WEEK 1 RESULTS. "Ad 4 won." Bars rise against the account average (labelled Demo data).'],
 ['90.1 to 95.1', 'So for week two, it makes six fresh takes on that winner, plus a static for her feed.', '"For week 2, let\'s make 6 clones of your own winner." The real Experiments dialog: variations of her winner are marked and the cursor clicks "Generate variations". Six cards fan out on "six". "Your winner works as a static too." The card flips to the static.'],
 ['95.8 to 101.2', 'And this morning, Ad Radar spotted a new winner, so a Rilo version is already waiting.', '"Btw, Radar caught a new winner this morning." A real ad from the Meta Ad Library: Vita Pop, 2 days live, 5 versions running. It flips: "I made a Rilo version for you."'],
 ['101.7 to 106.2', 'That\'s the loop: find what wins, make it yours, and do it again next week.', 'The capsule laps the whole line with a train of ads behind it. A ring bursts at A · Start. LED READY.'],
 ['107.5 to 113.2', '<b>Brevo Ads.</b> Clone any winning ad. Your first three ads are free.', 'Introducing / Brevo Ads / Clone any winning ad. / ads.brevo.com · Your first 3 ads are free. The last chord lands on the lockup and rings out.'],
]

# ---------------------------------------------------------------- screenplay
SCENES = [
 ('SC1 · Cold open', '0.00 to 1.75', [
   ('Camera', 'Locked wide, slow 2 percent push.'),
   ('Action', 'The capsule blur-ins at centre-top. LED reads "BREVO ADS". A mint blob drifts left, a soft coral blob right. The input bar rises: "Paste your product link". Headline blur-ins above.'),
   ('On screen', 'Welcome to <span class="g">Brevo Ads</span>, Maya'),
   ('Sound', 'Soft pad. Key ticks from 1.30.')]),
 ('SC2 · The link', '1.75 to 4.00', [
   ('Camera', 'Hard punch-in at 1.75 to a macro of the input bar. Low angle, shallow focus, capsule glow top right. Truck right with the caret.'),
   ('Action', 'Maya types "drinkrilo.com". The arrow button turns green. Cursor glides in at 2.90 and clicks at 3.30, dotted ring ripples. At 3.45 the URL breaks into mint particles that stream into the capsule\'s LED window. Pull back.'),
   ('On screen', 'drinkrilo.com · LED scrolls DRINKRILO.COM'),
   ('Sound', 'One click at 3.30.')]),
 ('SC3 · Learning', '4.00 to 6.00', [
   ('Camera', 'Locked on the capsule, slow orbit.'),
   ('Action', 'Rilo product photos, store-page sections and can close-ups fly from camera depth into the capsule. The glow behind it turns from Brevo mint to Rilo coral at 5.50.'),
   ('On screen', 'Mono status line with a dotted progress bar: Pulling product photos 22% · Reading the store page 54% · Finding your offer 78% · Learning the voice 100%'),
   ('Sound', 'Build, no riser.')]),
 ('SC4 · Brand kit', '6.00 to 9.60', [
   ('Camera', 'Slow push. Capsule small at top, LED "READY".'),
   ('Action', 'A coral kit folder rises. Four cards slide out and flick-swap: Product, Colours, Voice, Facts. Cards drop back in at 9.50.'),
   ('On screen', 'Product · Peach Yuzu Prebiotic Soda · 12-pack, $36 / Colours · Coral, cream, ripe peach / Voice · Bright · Playful · Never preachy / Facts · 9 g prebiotic fiber · 3 g sugar · 35 calories a can / Rilo · Brand learned ✓'),
   ('Sound', '<b>Music drop at 6.00</b> on READY.')]),
 ('T1 · Loop ride', '9.60 to 11.00', [
   ('Camera', 'Crane up: the folder sits on a dotted metro loop seen from above. Swoop down and chase the capsule along the line.'),
   ('Action', 'Dots ahead are grey. Dots behind the capsule turn green. It slows into station B.'),
   ('On screen', 'Station pill on a dotted stalk: <b>B · Ad Radar</b>'),
   ('Sound', 'One whoosh.')]),
 ('SC5 · Ad Radar', '11.00 to 17.30', [
   ('Camera', 'Arc carousel, slow rotate. Push-in at 12.80.'),
   ('Action', 'Real beverage ads on a 3D arc, two of them playing video. An Olipop static slides forward. A stat card slides in with a count-up. At 14.60 the carousel blurs back and three winners return with proof boxes over their hook, layout and offer.'),
   ('On screen', 'Scanning winning ads in your category / Olipop · Live for 182 days · Still running. That\'s a winner. / Saved to Radar ✓ / Taking apart 40 winners · Hooks · Layouts · Offers / +Hook · +Layout · +Offer'),
   ('Sound', 'Groove. Soft tick on each chip.')]),
 ('T2 · Loop ride', '17.30 to 18.50', [
   ('Camera', 'Crane and chase again.'),
   ('Action', 'Three angle cards (mint, coral, yuzu yellow) stand on the line. The capsule passes between them.'),
   ('On screen', 'No pill. The cards are the station.'),
   ('Sound', 'Whoosh.')]),
 ('SC6 · Angles', '18.50 to 24.00', [
   ('Camera', 'Centred card, slow push. Each card faces camera for at least 1.2 s.'),
   ('Action', 'Each card flips to reveal a looping AI video of that customer, not a still. Three source-tagged chips float around it. The glow takes the card\'s colour. Second card gets an "Under-served" badge. At 23.00 all three line up.'),
   ('On screen', 'Your three angles / Gut-health fans / Soda quitters / Mocktail hosts, with the chips from the script'),
   ('Sound', 'Soft flip on each card.')]),
 ('T3 · Loop ride', '24.00 to 25.20', [
   ('Camera', 'Crane and chase.'),
   ('Action', 'Lands on the next station.'),
   ('On screen', '<b>D · Make</b>'),
   ('Sound', 'Whoosh.')]),
 ('SC7 · The plan', '25.20 to 30.40', [
   ('Camera', 'Slow orbit. Bubbles tilt no more than 12 degrees. Reading lines hold 1.2 s.'),
   ('Action', 'The station pill stretches into the first agent bubble (capsule avatar, name "Brevo Ads"). Lines type in. Maya answers in a deep-green bubble on the right. At 29.60 the last bubble dissolves into mint particles.'),
   ('On screen', 'You saved 6 winners. / Let\'s make 30 ads from them. Statics and video. / Maya: Yes pls! / Cloning them for Rilo now.'),
   ('Sound', 'Beat drops to stabs while text types.')]),
 ('SC8 · Clones', '30.40 to 36.60', [
   ('Camera', 'Two cards side by side, square to camera.'),
   ('Action', 'Particles re-form as the Olipop winner. A labelled particle bridge builds the Rilo clone. Green proof boxes outline the matching hook in both. Hard cuts on the beat at 33.93 and 35.03. The last pair is the Poppi video and its Rilo clone, both playing.'),
   ('On screen', 'Pair chips from the script'),
   ('Sound', '<b>Re-drop at 30.00.</b>')]),
 ('SC9 · New videos and the burst', '36.60 to 45.00', [
   ('Camera', 'Cylinder carousel. Cuts speed up: 40.35, 41.85, 42.15, 42.42.'),
   ('Action', 'A video card slides over the agent bubble. Six Brevo Ads video styles play, each tagged with an angle. The creator-style clip speaks. At 43.00 the last card shatters into 30 thumbnails that spin and fly past camera.'),
   ('On screen', 'Plus new videos, made from your product photos. / style chips'),
   ('Sound', 'Creator line plays with its own audio, music ducked. Burst whoosh at 43.00.')]),
 ('SC10 · Export', '45.00 to 47.80', [
   ('Camera', 'Push on the bubble, then a tilt of at most 12 degrees over the grid.'),
   ('Action', 'Cursor clicks "Export all" at 45.60. The 30 ads land in a Library grid in three sizes. Camera scrolls it.'),
   ('On screen', 'All 30 are ready to launch. [Export all] / Done. 30 ads, every size.'),
   ('Sound', 'Click at 45.60.')]),
 ('SC11 · The cast', '47.80 to 56.50', [
   ('Camera', 'Grid shrinks up and away. Chat, then a row of 5 cards. Push into Leo at 54.80.'),
   ('Action', 'The agent\'s cheeky line. Maya\'s comic reply. Five AI creator cards fan in. Cursor hovers Leo. A pixel-mosaic dissolve swaps Leo through presenter options. Checks pop on all five at 56.00.'),
   ('On screen', 'Lines from the script. Counter: Option 1 of 4 to 3 of 4.'),
   ('Sound', 'Stabs, then <b>re-drop at 52.00</b>. One chime per check.')]),
 ('SC12 · Creator videos and plan', '56.50 to 69.50', [
   ('Camera', 'Phone left, three videos right. Then five phones fanned. Whip at 67.00. Calendar tilted at most 12 degrees.'),
   ('Action', 'Three creator videos play, one with its line. Five phones show each creator\'s captioned versions, swapping on cuts every 0.45 s (64.05 to 65.83) and 0.3 s (66.3 to 67.2). Thumbnails fly into a 30-day calendar.'),
   ('On screen', 'These are the videos I made for you. / Captions written for TikTok, Instagram and YouTube. / 5 creators, 12 videos each. 60 in all. / Your next 30 days, planned. / 38 → 60 posts ready'),
   ('Sound', 'Creator audio up, music ducked. Groove back at 62.00.')]),
 ('T4 · Loop ride', '69.50 to 70.80', [
   ('Camera', 'Crane and chase.'),
   ('Action', 'Lands on the last station.'),
   ('On screen', '<b>E · Week 1</b>'),
   ('Sound', 'Whoosh.')]),
 ('SC13 · Week 1 results', '70.80 to 75.50', [
   ('Camera', 'Push into the departure board, dive into one flap at 71.90, hard cut at 72.00, tiles clear.'),
   ('Action', 'The pill becomes Maya\'s bubble with a file chip. A split-flap board flips behind it. The winning video sits left; 3D bars grow on the right, winners in green.'),
   ('On screen', 'Week 1 is in! / WEEK 1 RESULTS / Ad 4 won. It felt like a friend\'s story, not an ad. / chart from the script, "Demo data" microline'),
   ('Sound', 'Stab on the board flip. Groove from 72.00.')]),
 ('SC14 · Week 2 moves', '75.50 to 82.50', [
   ('Camera', 'Fan spread, then a Y-flip at 81.00.'),
   ('Action', 'Six clones of the winner fan out behind it, each a different creator and kitchen. Then the winner flips into a static ad with the same hook.'),
   ('On screen', 'For week 2, let\'s make 6 clones of your own winner. / New creators, new kitchens. Same winning script 🍑 / Your winner works as a static too.'),
   ('Sound', 'Stabs under the chat lines.')]),
 ('SC15 · New winner', '82.50 to 89.40', [
   ('Camera', 'Whip at 82.50. Card cycles. Y-flip at 86.00.'),
   ('Action', 'Three fresh Radar winners cycle with a stats column. The last flips into "Rilo · your version", playing.'),
   ('On screen', 'Btw, Radar caught a new winner this morning. / New winner 1 of 3 · Live 9 days · 14 versions running / I made a Rilo version for you. / Ready for week 2?'),
   ('Sound', '<b>Re-drop at 87.00.</b>')]),
 ('SC16 · Ready', '89.40 to 92.50', [
   ('Camera', 'Locked centre, slow push.'),
   ('Action', 'The capsule avatar flies out of the bubble to centre and grows. The LED marquee scrolls, then snaps to READY.'),
   ('On screen', 'BREVO ADS → NEXT: WEEK 2 → READY'),
   ('Sound', 'Stabs, then <b>re-drop at 92.00</b> on READY.')]),
 ('SC17 · Loop closes', '92.50 to 94.00', [
   ('Camera', 'Crane to the full loop. Fast chase.'),
   ('Action', 'The capsule laps the line, trailing every ad it made. Stations A to E tick green. At 93.40 it pulls into "A · Start" and a ring of green ticks bursts out.'),
   ('On screen', 'A · Start'),
   ('Sound', 'Full groove.')]),
 ('SC18 · Launch lockup', '94.00 to 97.25', [
   ('Camera', 'Hard cut at 94.00 to a clean frame. Slow 3 percent push.'),
   ('Action', 'The capsule glides in and parks beside the wordmark, LED reading READY. The wordmark wipes in. "Introducing" fades in above. The line lands at 94.85, the call to action at 95.15. Hold to the end.'),
   ('On screen', 'Introducing / <b>Brevo Ads</b> / Clone any winning ad. / ads.brevo.com · Your first 3 ads are free'),
   ('Sound', 'The real last chord hits on the 94.00 cut and rings out. No stinger.')]),
]

CLAIMS = [
 ['Paste a product link to start', '<span class="ok">Verified</span>', 'Launch film, 10 Nov, made in-app.'],
 ['Clones statics: same hook, same layout, your brand', '<span class="ok">Verified</span>', '18 Rilo clones made 10 Nov.'],
 ['Clones video scene by scene', '<span class="ok">Verified</span>', 'Poppi to Rilo, 27 s, 10 Nov.'],
 ['Ad Radar finds winners in your category', '<span class="ok">Verified</span>', 'Hero feature since Oct.'],
 ['Days live on a winner', '<span class="ok">Verified</span>', 'One passing line only, per your rule.'],
 ['AI creators and presenters', '<span class="ok">Verified</span>', 'UGC and presenter videos.'],
 ['Six video styles named in SC9', '<span class="ok">Verified</span>', 'From the template library.'],
 ['Angles', '<span class="ok">Verified</span>', 'Quick create works by angle.'],
 ['Brand kit: colours and voice learned from the link', '<span class="chk">Confirm in-app</span>', 'Else keep Product and Facts cards only.'],
 ['"Taking apart 40 winners"', '<span class="chk">Confirm in-app</span>', 'Else count to the real number.'],
 ['Export all, every size', '<span class="chk">Confirm in-app</span>', 'Library exists. Bulk export to confirm.'],
 ['Captions per platform', '<span class="chk">Confirm in-app</span>', 'Social post agent exists.'],
 ['30-day post plan (calendar)', '<span class="chk">Confirm in-app</span>', 'Else cut the calendar, keep the phones.'],
 ['Re-cast a creator from options', '<span class="chk">Confirm in-app</span>', ''],
 ['Agent reads a dropped results file', '<span class="no">Not known</span>', 'Fallback: Maya says "Ad 4 won" herself. Chart stays.'],
 ['Week 1 chart numbers', '<span class="chk">Illustrative</span>', 'Fictional brand. "Demo data" microline on screen.'],
 ['"Your first 3 ads are free"', '<span class="ok">Confirmed</span>', 'Launch offer, confirmed 21 Nov.'],
]

LOOP_SVG = '''<svg viewBox="0 0 720 300" role="img" aria-label="The Loop: a metro loop line with stations A to E and the Brevo Ads capsule riding it" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">
<rect x="80" y="70" width="560" height="170" rx="85" fill="none" stroke="var(--line)" stroke-width="6" stroke-dasharray="2 10" stroke-linecap="round"/>
<path d="M165 70 H555 A85 85 0 0 1 640 155" fill="none" stroke="var(--forest)" stroke-width="6" stroke-dasharray="2 10" stroke-linecap="round"/>
<g font-size="13" font-weight="600" fill="var(--ink)">
<g transform="translate(165 70)"><line y1="0" y2="-26" stroke="var(--forest)" stroke-dasharray="2 3"/><rect x="-46" y="-50" width="92" height="26" rx="13" fill="var(--card)" stroke="var(--line)"/><circle cx="-33" cy="-37" r="4" fill="var(--forest)"/><text x="-24" y="-33">A · Start</text></g>
<g transform="translate(330 70)"><line y1="0" y2="-26" stroke="var(--forest)" stroke-dasharray="2 3"/><rect x="-56" y="-50" width="112" height="26" rx="13" fill="var(--card)" stroke="var(--line)"/><circle cx="-43" cy="-37" r="4" fill="var(--forest)"/><text x="-34" y="-33">B · Ad Radar</text></g>
<g transform="translate(500 70)"><line y1="0" y2="-26" stroke="var(--forest)" stroke-dasharray="2 3"/><rect x="-50" y="-50" width="100" height="26" rx="13" fill="var(--card)" stroke="var(--line)"/><circle cx="-37" cy="-37" r="4" fill="var(--forest)"/><text x="-28" y="-33">C · Angles</text></g>
<g transform="translate(640 155)"><line x1="0" x2="0" y1="0" y2="26" stroke="var(--line)" stroke-dasharray="2 3"/><rect x="-46" y="26" width="92" height="26" rx="13" fill="var(--card)" stroke="var(--forest)"/><circle cx="-33" cy="39" r="4" fill="none" stroke="var(--forest)" stroke-width="2"/><text x="-24" y="43">D · Make</text></g>
<g transform="translate(360 240)"><line y1="0" y2="26" stroke="var(--line)" stroke-dasharray="2 3"/><rect x="-52" y="26" width="104" height="26" rx="13" fill="var(--card)" stroke="var(--line)"/><circle cx="-39" cy="39" r="4" fill="var(--mute)"/><text x="-30" y="43">E · Week 1</text></g>
</g>
<g transform="translate(628 120) rotate(62)"><rect x="-26" y="-15" width="52" height="30" rx="15" fill="#006A43"/><rect x="-16" y="-8" width="32" height="16" rx="5" fill="#0E1411"/><g fill="#C0FFA5"><circle cx="-10" cy="0" r="1.6"/><circle cx="-5" cy="0" r="1.6"/><circle cx="0" cy="0" r="1.6"/><circle cx="5" cy="0" r="1.6"/><circle cx="10" cy="0" r="1.6"/></g></g>
<text x="360" y="160" text-anchor="middle" font-size="13" fill="var(--mute)">The capsule rides the line. Green dots = done.</text>
</svg>'''

def scenes_html():
    out = []
    for title, tc, rows in SCENES:
        r = ''.join(f'<div class="sr"><span class="sk">{k}</span><span>{v}</span></div>' for k, v in rows)
        out.append(f'<article class="scene"><header><h3>{title}</h3><span class="tc">{tc} s</span></header>{r}</article>')
    return ''.join(out)

CSS = '''
:root{--bg:#FAF7EF;--card:#FFFFFF;--ink:#1B1B1B;--mute:#5E625F;--line:#E6E1D4;--forest:#006A43;--g:#0B7A5B;--mint:#C0FFA5;--red:#C8433F;--soft:#EEF5EC;--chip:#F1EEE4;--amber:#9A6200}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0E1411;--card:#151D19;--ink:#ECEFEA;--mute:#A3ABA5;--line:#26302B;--forest:#3FBF85;--g:#5CD49B;--mint:#C0FFA5;--red:#F07A73;--soft:#16261D;--chip:#1C2621;--amber:#E8B35A}}
:root[data-theme="dark"]{--bg:#0E1411;--card:#151D19;--ink:#ECEFEA;--mute:#A3ABA5;--line:#26302B;--forest:#3FBF85;--g:#5CD49B;--mint:#C0FFA5;--red:#F07A73;--soft:#16261D;--chip:#1C2621;--amber:#E8B35A}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif}
a{color:var(--forest)}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
nav.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav.top .wrap{display:flex;gap:18px;overflow-x:auto;white-space:nowrap;padding-top:10px;padding-bottom:10px;font-size:14px;font-weight:600}
nav.top a{text-decoration:none;color:var(--mute)}nav.top a:hover{color:var(--forest)}
.kicker{font:500 12px/1 "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--forest);margin-top:40px}
h1{font-size:clamp(30px,5vw,50px);line-height:1.05;letter-spacing:-.03em;margin:12px 0 14px}
h2{font-size:clamp(24px,3.4vw,34px);letter-spacing:-.02em;margin:64px 0 10px;line-height:1.15}
h3{margin:0;font-size:18px;letter-spacing:-.01em}
h4{margin:26px 0 8px;font-size:17px}
.lede{font-size:18px;color:var(--mute);max-width:760px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:22px 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.stat b{display:block;font-size:24px;letter-spacing:-.02em}.stat span{font-size:13px;color:var(--mute)}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin:14px 0}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card);margin:14px 0}
table.st{border-collapse:collapse;width:100%;font-size:14px;line-height:1.5}
table.st th{text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);padding:10px 12px;border-bottom:1px solid var(--line);background:var(--chip)}
table.st td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
table.st tr:last-child td{border-bottom:0}
table.st td:first-child{font:600 13px/1.5 "JetBrains Mono",monospace;white-space:nowrap;color:var(--forest)}
table.st.wide td:first-child{font:600 14px/1.5 Inter,sans-serif;white-space:normal;color:var(--ink)}
tr.band td{background:var(--soft);font:700 13px/1.4 Inter,sans-serif!important;color:var(--forest)!important;letter-spacing:.02em}
.g{color:var(--g);font-weight:700}
.ok{color:var(--g);font-weight:700}.chk{color:var(--amber);font-weight:700}.no{color:var(--red);font-weight:700}
.scene{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin:12px 0}
.scene header{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:8px}
.tc{font:600 13px/1 "JetBrains Mono",monospace;color:var(--forest);background:var(--soft);padding:6px 9px;border-radius:999px}
.sr{display:grid;grid-template-columns:96px 1fr;gap:12px;padding:6px 0;border-top:1px solid var(--line);font-size:15px}
.sk{font:600 12px/1.9 "JetBrains Mono",monospace;text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}
.svgbox{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px;margin:14px 0;overflow-x:auto}
.svgbox.tl svg{min-width:720px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
ul{padding-left:20px}li{margin:5px 0}
footer{color:var(--mute);font-size:13px;padding:50px 0 60px}
@media (max-width:700px){
 .two{grid-template-columns:1fr}
 table.st thead{display:none}
 table.st,table.st tbody{display:block;width:100%}
 table.st tr{display:block;width:100%;border-bottom:1px solid var(--line);padding:6px 0}
 table.st td{display:block;width:100%;border:0;padding:4px 14px;overflow-wrap:anywhere}
 table.st td:empty{display:none}
 table.st td[data-l]::before{content:attr(data-l);display:block;font:600 11px/1.6 "JetBrains Mono",monospace;text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}
 table.st td:first-child::before{display:none}
 tr.band td{padding:10px 14px}
 .sr{grid-template-columns:1fr;gap:2px}
}
'''

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Loop: Brevo Ads film playbook</title>
<meta name="description" content="Frame-by-frame teardown of Fastlane's 97 s launch film, the style playbook, and the 113.2 s voiced launch film for Brevo Ads.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>
<nav class="top"><div class="wrap"><a href="#film">Film</a><a href="#source">Source</a><a href="#teardown">Teardown</a><a href="#playbook">Playbook</a><a href="#brevo">Brevo version</a><a href="#script">Voice and picture</a><a href="#post">Launch post</a><a href="#claims">Claims</a><a href="#production">Production</a></div></nav>
<main class="wrap">
<div class="kicker">Brevo Ads launch film · Playbook · 21 Nov 2026</div>
<h1>The Loop</h1>
<p class="lede">Fastlane's launch film, taken apart frame by frame. Then rebuilt as the launch film for Brevo Ads: 113.2 s with a voiceover that leads the picture, its own look, and only claims we can stand behind.</p>

<h2 id="film">The film: Brevo Ads launch, v6 with real product screens</h2>
<p>113.2 s, built in HyperFrames. The voice leads: every move, mark and line lands on the word that names it. Six beats now run on real Brevo Ads screens, captured from the live product on 21 Nov. This is a 720p copy for phones; the 1080p 60 fps master is sent separately.</p>
<video src="film.mp4" poster="poster.jpg" controls playsinline preload="metadata" style="width:100%;border-radius:16px;border:1px solid var(--line);background:#000;display:block"></video>
<div class="card"><h4 style="margin-top:0">What changed</h4>{ul([
 '<b>Real product screens (v6):</b> the Paste a link dialog, the Rilo product memory page (facts, look, claims), Ad Radar filtered to Food & Drink, the real Olipop winner with its own video and "6 months active", the Rilo Ads made page, and the Experiments variations dialog. Demo store link shown as drinkrilo.com.',
 '<b>Voiceover:</b> one warm narrator (ElevenLabs voice "Hope", 0.92 speed), recorded one paragraph per take so the sentences flow. Brevo is said BRAY-vo.',
 '<b>The voice leads:</b> the picture was re-timed to the voice, word by word. Nothing moves before it is named, and the film grew from 97.25 s to 113.2 s to give each idea room.',
 '<b>New opening:</b> Maya in her own store, her to-do list with "Make ads" circled, then the link pasted into Brevo Ads.',
 '<b>Markings redrawn:</b> outlines draw on with a soft halo and a light sweep, labels sit on leader lines, and each clone pair is joined by a drawn bridge with its label on the arc.',
 '<b>Calmer pace:</b> fewer, longer beats. Extra bubbles, the second Radar save and the phone swaps are gone; key frames hold while the voice explains them.',
])}</div>
<h2 id="source">1. The source at a glance</h2>
<p><a href="{SRC}">Fastlane on X: "Today we're introducing Claude for Ads"</a></p>
<div class="stats">
<div class="stat"><b>97.25 s</b><span>running time</span></div>
<div class="stat"><b>16:9</b><span>1280 x 720, 60 fps</span></div>
<div class="stat"><b>0 lines</b><span>of voiceover. Music only</span></div>
<div class="stat"><b>120 BPM</b><span>one bar every 2.0 s</span></div>
<div class="stat"><b>19 cuts</b><span>hard cuts. Plays as one camera move</span></div>
<div class="stat"><b>25 lines</b><span>of chat: 21 agent, 4 user</span></div>
</div>
<div class="card"><h4 style="margin-top:0">Why it works</h4>
{ul([
 'It shows the product as one loop, not a feature list. A URL goes in. One lap of work comes out. Then lap 2.',
 'The agent leads. The human types a URL, says yes 3 times and asks for one tweak. That is the pitch.',
 'One metaphor carries every transition: a race track with stations. You always know where you are.',
 'Never a still frame. The camera drifts, pushes or whips at every moment.',
 'Music does the talking. The beat drops to stabs while chat types, then slams back on each reveal.',
 'Every proposal ends in a number: 30 ads, $5K a day, 7 days, 5 creators, 6 remixes.',
])}</div>
<div class="svgbox tl">{TIMELINE}</div>

<h2 id="teardown">2. Frame-by-frame teardown</h2>
<p>Read from 2 frames a second across the film, then 10 to 15 frames a second at every transition. Times are seconds.</p>
{table(['Time', 'On screen', 'Motion', 'Sound'], TEAR)}

<h2 id="playbook">3. Style playbook</h2>
<div class="two">
<div class="card"><h4 style="margin-top:0">Story rules</h4>{ul([
 'Show one full loop: input, learn, research, plan, make, ship, measure, loop.',
 'Name each step with a station pill: a letter and two words.',
 'The agent proposes. The human approves. At most 5 human lines.',
 'End every proposal in a concrete number.',
 'One joke about every 20 s: "Yes pls!", "Wow bit harsh... but yes".',
 'Personalise in frame 1: the user\'s name in the headline.',
 'The client\'s brand takes over the colour once learned.',
 'End on the loop restarting.',
])}</div>
<div class="card"><h4 style="margin-top:0">Visual system</h4>{ul([
 'Canvas: warm off-white (#DDDDDB to #E8E4DF), never pure white. Light grain on everything.',
 'One big soft glow behind the focal object, dithered with grain. Its colour carries meaning.',
 'One accent colour only: brand word, key numbers, user bubbles, winning bars.',
 'Everything is a soft 3D object. Bubbles are thick extruded pills with a top highlight and soft shadow.',
 'Chips under every media card: coloured dot, bold label, grey sublabel.',
 'Type: neo-grotesk, tight tracking. Mono for status lines. Dot-matrix LED for the agent\'s face.',
 'Media always in rounded 9:16 cards. Never full-bleed.',
])}</div>
<div class="card"><h4 style="margin-top:0">Camera</h4>{ul([
 'Never static. A slow orbit or dolly runs under everything.',
 'Push-in on every reveal, about 15 percent over 0.4 s.',
 'Whip with directional blur at every section change.',
 'Shallow depth of field: background cards blur 6 to 12 px.',
 'Only one hard punch-in: the typed URL at 1.75 s.',
])}</div>
<div class="card"><h4 style="margin-top:0">Chat rules</h4>{ul([
 'Agent: frosted white bubble, left, avatar and name above the first line.',
 'User: solid accent bubble, white text, right, initial avatar.',
 'One idea per bubble. At most about 45 letters.',
 'One highlighted word or number per line, in the accent.',
 'Hold each finished line 0.6 to 1.0 s before the next.',
 'Casual register: "pls", "dw", "Btw", one emoji in the film.',
])}</div>
<div class="card"><h4 style="margin-top:0">Edit rhythm</h4>{ul([
 '120 BPM. A new idea lands about every bar (2.0 s).',
 'Hard cuts only on beats, and only inside montages.',
 'Speed up cuts into a climax (2.3, 1.5, 0.3, 0.27 s), then explode.',
 'About 45 beats in 97 s: one every 2.2 s.',
 'About 190 words on screen: roughly 2 words a second.',
 'Longest single camera move: 32 s (1.75 to 33.93 s).',
])}</div>
<div class="card"><h4 style="margin-top:0">Sound</h4>{ul([
 'Music only. No voiceover.',
 'Soft intro, then the drop on "READY" at 6.0 s.',
 'Chat breakdowns: the beat gates to stabs at 25.5, 47.0, 71.0, 81.0 and 90.5 s.',
 'Re-drops on each reveal: 30.0, 52.0, 87.0 and 92.0 s.',
 'Clip audio is the only human voice. Music ducks about 5 dB under it.',
 'SFX: key ticks, one click, whooshes on swoops, a chime per check.',
])}</div>
</div>
<h4>Motion vocabulary</h4>
{table(['Move', 'Used for', 'Timing'], MOVES, 'wide')}

<h2 id="brevo">4. The Brevo version: decisions</h2>
<p>Same length, same beat grid, same story shape. New world, new hero object, Brevo palette. Brand is <b>Brevo Ads</b>.</p>
<div class="svgbox">{LOOP_SVG}</div>
{table(['Element', 'Fastlane', 'Brevo Ads', 'Why'], DECIDE, 'wide')}
<h4>Truth swaps</h4>
<p>Fastlane shows features we can\'t claim for Brevo Ads. Each one gets a true replacement that keeps the beat.</p>
{table(['Fastlane beat', 'Brevo Ads beat', 'Note'], SWAPS, 'wide')}

<h2 id="script">5. Voiceover and picture</h2>
<p>The full narration, timed to the film. The right column is what the viewer sees while each line is spoken. Creator lines are the clips\' own sound.</p>
{table(['Time (s)', 'Voice', 'Picture'], VOP, 'wide')}

<h2 id="post">6. Launch post</h2>
<p>Fastlane's film never says "introducing". Its post does. Ours ships with one too. The film itself is built: see the delivery note below.</p>
<div class="two">
<div class="card"><h4 style="margin-top:0">X</h4><p style="white-space:pre-line;margin:0">Today we're launching Brevo Ads.

Paste your product link. It finds the ads already winning in your category. Then it clones them for your brand.

Statics, video and AI creators.

Your first 3 ads are free: ads.brevo.com</p></div>
<div class="card"><h4 style="margin-top:0">LinkedIn</h4><p style="white-space:pre-line;margin:0">Today we're launching Brevo Ads: an AI ad agent for ecommerce brands.

Paste your product link. Then it:
· learns your product, colours and voice
· finds the ads already winning in your category
· clones them for your brand, statics and video
· casts AI creators for TikTok, Reels and Shorts

Run it again next week. It finds new winners every time.

Your first 3 ads are free at ads.brevo.com</p></div>
</div>
<div class="card"><h4 style="margin-top:0">What changes because it is the launch</h4>{ul([
 'The product is named in the first second (LED and headline) and in the last 3.25 s.',
 'Every hero feature gets one beat: brand learning, Ad Radar, angles, static clones, video clones, video styles, AI creators.',
 'The film ends on a launch lockup, not a loop restart: Introducing, Brevo Ads, the line, the offer.',
 'Demo data stays labelled on screen. At launch, every number gets screenshotted.',
])}</div>
<h2 id="claims">7. Claims check</h2>
{table(['Claim', 'Status', 'Note'], CLAIMS, 'wide')}

<h2 id="production">8. Production notes</h2>
<div class="card">{ul([
 '<b>Build:</b> HyperFrames (HTML and GSAP), 1920 x 1080, 60 fps, 113.2 s. Reuse the Brevo Ads launch film kit: palette tokens and Inter.',
 '<b>Capsule:</b> one 3D render in three angles (front, three-quarter, side). The LED window is live HTML in a dot-matrix font, so it can scroll any text.',
 '<b>Loop line:</b> an SVG path in perspective. Grey dots ahead, green dots behind. Station pills are HTML.',
 '<b>Media we have:</b> 9 winning statics and the Poppi video (brevo-ads-launch/src), 18 Rilo static clones and 1 Rilo video clone, 3 Rilo photos.',
 '<b>Media to make:</b> 6 style videos, 5 AI creator portraits, 3 creator videos (2 with lines), 3 angle loops, 6 winner variants, 3 fresh Radar winners. Real AI video in every slot, never stills.',
 '<b>Sound:</b> voice at -16 LUFS on top. An original 120 BPM track sits under it and dips about 8 dB while she speaks. The drop lands on READY at 11.9 s, the last chord on the lockup at 107.9 s.',
 '<b>Your standing rules applied:</b> text tilts at most 12 degrees (Fastlane tilts its table about 25). Reading lines face camera for at least 1.2 s. 12 to 22 quiet SFX cues. Music ducks under creator lines. No dead air.',
 '<b>Domain check:</b> drinkrilo.com is unregistered today, so the typed URL points at no real business.',
])}</div>
<footer>Teardown measured on the 720p source: cut detection, 2 to 15 frames a second, loudness in 0.25 s steps. Built 21 Nov 2026.</footer>
</main></body></html>'''

bad = [c for c in ('—', '–') if c in html]
assert not bad, f'dash found: {bad}'
(ROOT / 'loop').mkdir(exist_ok=True)
(ROOT / 'loop' / 'index.html').write_text(html)
print('ok', len(html))
