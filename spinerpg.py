import base64
import json
from pathlib import Path

import streamlit as st


def load_image_data_uri(basename):
    """Look for `basename.png` / `.jpg` / `.jpeg` / `.webp` / `.gif` next to
    this script and return a base64 data: URI for it, or None if no such
    file exists. Used for every local image (founder photos, the QR code,
    the chewie easter-egg) so they're embedded directly instead of relying
    on an internet connection at view time."""
    here = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")

    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        candidate = here / f"{basename}.{ext}"
        if candidate.exists():
            data = candidate.read_bytes()
            b64 = base64.b64encode(data).decode("utf-8")
            mime = "jpeg" if ext == "jpg" else ext
            return f"data:image/{mime};base64,{b64}"

    return None


def render_html_frame(html_string, height, scrolling=False):
    """Render raw HTML in an iframe, using the new st.iframe API when
    available and falling back to components.html on older Streamlit
    versions. st.iframe auto-sizes to content and has no `scrolling`
    argument, so that kwarg only applies to the legacy fallback."""
    try:
        st.iframe(html_string, height=height)
    except AttributeError:
        import streamlit.components.v1 as components
        components.html(html_string, height=height, scrolling=scrolling)


def get_qr_html():
    """Return an <img> tag for a real Instagram QR code if one has been
    dropped next to this script (qr.png/.jpg/.jpeg/...), otherwise fall
    back to a stylised placeholder graphic."""
    uri = load_image_data_uri("qr")

    if uri:
        return (
            f'<img src="{uri}" alt="Instagram QR code" '
            f'style="width:220px;height:220px;border-radius:10px;'
            f'border:2px solid #d8b878;">'
        )

    # Placeholder shown until a real QR image is added.
    return """
    <div style="width:220px;height:220px;margin:0 auto;border:2px dashed #a8875a;
                border-radius:10px;display:flex;align-items:center;justify-content:center;
                background:#221d17;">
        <svg viewBox="0 0 100 100" width="180" height="180" xmlns="http://www.w3.org/2000/svg">
          <rect width="100" height="100" fill="#f0e4cf"/>
          <rect x="6" y="6" width="24" height="24" fill="none" stroke="#221d17" stroke-width="6"/>
          <rect x="14" y="14" width="8" height="8" fill="#221d17"/>
          <rect x="70" y="6" width="24" height="24" fill="none" stroke="#221d17" stroke-width="6"/>
          <rect x="78" y="14" width="8" height="8" fill="#221d17"/>
          <rect x="6" y="70" width="24" height="24" fill="none" stroke="#221d17" stroke-width="6"/>
          <rect x="14" y="78" width="8" height="8" fill="#221d17"/>
          <rect x="40" y="10" width="6" height="6" fill="#221d17"/>
          <rect x="50" y="14" width="6" height="6" fill="#221d17"/>
          <rect x="60" y="22" width="6" height="6" fill="#221d17"/>
          <rect x="40" y="34" width="6" height="6" fill="#221d17"/>
          <rect x="52" y="40" width="6" height="6" fill="#221d17"/>
          <rect x="64" y="46" width="6" height="6" fill="#221d17"/>
          <rect x="42" y="58" width="6" height="6" fill="#221d17"/>
          <rect x="56" y="64" width="6" height="6" fill="#221d17"/>
          <rect x="70" y="58" width="6" height="6" fill="#221d17"/>
          <rect x="40" y="76" width="6" height="6" fill="#221d17"/>
          <rect x="54" y="82" width="6" height="6" fill="#221d17"/>
          <rect x="66" y="76" width="6" height="6" fill="#221d17"/>
          <rect x="80" y="40" width="6" height="6" fill="#221d17"/>
          <rect x="86" y="52" width="6" height="6" fill="#221d17"/>
          <rect x="80" y="64" width="6" height="6" fill="#221d17"/>
        </svg>
    </div>
    """


# Build the crossword grid
def build_new_crossword_grid():
    """
    Crossword grid only.
    None = black cell, letter = white cell.

    The words are placed so that all 8 answers form one connected
    crossword and the clue numbering below remains explicit.
    """
    rows = 13
    cols = 13
    grid = [[None] * cols for _ in range(rows)]

    # Answer placements:
    # 1 Down  : READING CIRCLE
    # 2 Down  : PHYLUM
    # 3 Across: MURDER BALLAD
    # 4 Down  : HOGWARTS
    # 5 Down  : BONEYARD
    # 6 Across: CHORDATA
    # 7 Across: READERS
    # 8 Across: CRANIUM

    placements = [
        ("READINGCIRCLE", "D", 0, 3),
        ("PHYLUM",        "D", 6, 10),
        ("MURDERBALLAD",  "A", 9, 1),
        ("HOGWARTS",      "D", 5, 8),
        ("BONEYARD",      "D", 4, 11),
        ("CHORDATA",      "A", 0, 0),
        ("READERS",       "A", 12, 2),
        ("CRANIUM",       "A", 5, 0),
    ]

    for word, direction, row, col in placements:
        for i, letter in enumerate(word):
            r = row + (i if direction == "D" else 0)
            c = col + (i if direction == "A" else 0)
            grid[r][c] = letter

    return grid


CROSSWORD_GRID = build_new_crossword_grid()

CROSSWORD_CLUES = {
    "across": [
        {
            "num": 3,
            "clue": "The Spine's flagship event, held every year for Fitoor. This event had the highest external participation last year!",
            "length": 12,
            "row": 9,
            "col": 1
        },
        {
            "num": 6,
            "clue": "This word is the answer to the phylum clue  — the third-largest phylum in the animal kingdom.",
            "length": 8,
            "row": 0,
            "col": 0
        },
        {
            "num": 7,
            "clue": "Most people in this club are ________.",
            "length": 7,
            "row": 12,
            "col": 2
        },
        {
            "num": 8,
            "clue": "A bony enclosure around the brain of a vertebrate. This is also what the core of the Spine calls itself.",
            "length": 7,
            "row": 5,
            "col": 0
        },
    ],
    "down": [
        {
            "num": 1,
            "clue": "We get together, sometimes weekly, to read. What do we call this (mini) event?",
            "length": 13,
            "row": 0,
            "col": 3
        },
        {
            "num": 2,
            "clue": "This and the clue 6 are 2 words, part of 1 big phrase. For this word: a group into which animals, plants, etc. are divided, smaller than a kingdom and larger than a class.",
            "length": 6,
            "row": 6,
            "col": 10
        },
        {
            "num": 4,
            "clue": "We brought this wizarding and witchcraft boarding school to Plaksha in one of our earlier events.",
            "length": 8,
            "row": 5,
            "col": 8
        },
        {
            "num": 5,
            "clue": "The Spine's very own magazine is called __________.",
            "length": 8,
            "row": 4,
            "col": 11
        },
    ]
}

CROSSWORD_JSON = json.dumps({
    "grid": CROSSWORD_GRID,
    "rows": 13,
    "cols": 13,
    "clues": CROSSWORD_CLUES
})

QR_IMAGE_HTML = get_qr_html()

# ----------------------------------------------------------------------------
# FOUNDER PHOTOS + CHEWIE EASTER EGG
# ----------------------------------------------------------------------------

FOUNDER_PHOTO_BASENAMES = {
    "maanal": ["maanal1", "maanal2", "maanal3"],
    "aman": ["aman1", "aman2", "aman3"],
    "trinav": ["trinav1", "trinav2", "trinav3"],
}

founder_photos = {}

for member, basenames in FOUNDER_PHOTO_BASENAMES.items():
    srcs = []
    for i, basename in enumerate(basenames, start=1):
        uri = load_image_data_uri(basename)
        srcs.append(
            uri
            if uri
            else f"https://via.placeholder.com/180x200?text={member.capitalize()}+{i}"
        )
    founder_photos[member] = srcs

FOUNDER_PHOTOS_JSON = json.dumps(founder_photos)

CHEWIE_IMAGE_URI = load_image_data_uri("chewie")
CHEWIE_URI_JSON = json.dumps(CHEWIE_IMAGE_URI)

# ----------------------------------------------------------------------------
# PUZZLE III DATA (The Melody) — generated exactly as in the standalone
# SPINE Chronicles Puzzle III script, unchanged.
# ----------------------------------------------------------------------------

melody_sequence = [
    "G#3", "A3", "C#4", "C#3",
    "E3", "D#3", "C#3", "C3",
    "G#2", "A2", "A#2", "B2",
    "C3", "C#3", "E3", "F#3"
]

notes = [
    ("C#2", 69.30),
    ("D2", 73.42),
    ("D#2", 77.78),
    ("E2", 82.41),
    ("F2", 87.31),
    ("F#2", 92.50),
    ("G2", 98.00),
    ("G#2", 103.83),
    ("A2", 110.00),
    ("A#2", 116.54),
    ("B2", 123.47),
    ("C3", 130.81),
    ("C#3", 138.59),
    ("D3", 146.83),
    ("D#3", 155.56),
    ("E3", 164.81),
    ("F3", 174.61),
    ("F#3", 185.00),
    ("G3", 196.00),
    ("G#3", 207.65),
    ("A3", 220.00),
    ("A#3", 233.08),
    ("B3", 246.94),
    ("C4", 261.63),
    ("C#4", 277.18),
]

keyboard_letters = list("abcdefghijklmnopqrstuvwxy")

white_notes = {"C", "D", "E", "F", "G", "A", "B"}

piano_keys = []
white_index = 0

for note, freq in notes:
    pitch = note[:-1]
    octave = int(note[-1])
    is_black = "#" in pitch

    if is_black:
        left = white_index * 48 - 16

        piano_keys.append({
            "note": note,
            "freq": freq,
            "key": keyboard_letters[len(piano_keys)],
            "type": "black",
            "left": left
        })

    else:
        piano_keys.append({
            "note": note,
            "freq": freq,
            "key": keyboard_letters[len(piano_keys)],
            "type": "white",
            "left": white_index * 48
        })

        white_index += 1

white_counter = 0
key_html = []

for i, (note, freq) in enumerate(notes):

    letter = keyboard_letters[i].upper()
    pitch = note[:-1]
    is_black = "#" in pitch

    if not is_black:

        key_html.append(
            f'<div class="piano-key white-key" '
            f'data-note="{note}" '
            f'data-freq="{freq}" '
            f'data-key="{keyboard_letters[i]}" '
            f'style="left:{white_counter * 48}px;">'
            f'<span class="note-label">{note}</span>'
            f'<span class="computer-key">{letter}</span>'
            f'</div>'
        )

        white_counter += 1

white_counter = 0
black_html = []

for i, (note, freq) in enumerate(notes):

    pitch = note[:-1]
    is_black = "#" in pitch

    if is_black:

        black_left = white_counter * 48 - 14
        letter = keyboard_letters[i].upper()

        black_html.append(
            f'<div class="piano-key black-key" '
            f'data-note="{note}" '
            f'data-freq="{freq}" '
            f'data-key="{keyboard_letters[i]}" '
            f'style="left:{black_left}px;">'
            f'<span class="note-label">{note}</span>'
            f'<span class="computer-key">{letter}</span>'
            f'</div>'
        )

    else:
        white_counter += 1

st.set_page_config(
    page_title="SPINE Chronicles",
    layout="wide"
)

# ----------------------------------------------------------------------------
# GLOBAL THEME (browns & beiges)
# ----------------------------------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: #211d17;
    color: #f0e4cf;
    font-family: Georgia, serif;
}

/* hide default streamlit chrome a bit so the intro feels more like a scroll */
header[data-testid="stHeader"] {
    background: transparent;
}

.scroll-box {
    background: #362f24;
    border: 3px double #d8b878;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(216,184,120,.2);
    margin-bottom: 20px;
}

.sequence-box {
    background: #2b261d;
    border: 2px solid #a8875a;
    border-radius: 10px;
    padding: 16px;
    margin-top: 18px;
}

/* --- Intro / landing --- */

.intro-wrap {
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 40px 20px 60px;
}

.greetings-title {
    font-size: 96px;
    font-weight: bold;
    letter-spacing: 4px;
    color: #f5e9c8;
    text-shadow: 0 0 25px rgba(216,184,120,.35);
    margin-bottom: 10px;
    opacity: 0;
    animation: fadeInUp 1.4s ease-out forwards;
}

.intro-line {
    max-width: 780px;
    font-size: 20px;
    line-height: 1.7;
    color: #f0e4cf;
    margin: 18px auto;
    opacity: 0;
    animation: fadeInUp 1.4s ease-out forwards;
}

.intro-line.delay-1 { animation-delay: 1.6s; }
.intro-line.delay-2 { animation-delay: 3.4s; }
.intro-line.delay-3 { animation-delay: 5.2s; }

.intro-warning {
    display: inline-block;
    margin-top: 10px;
    padding: 10px 22px;
    border: 1px solid #a8875a;
    border-radius: 6px;
    background: #2b261d;
    color: #e8c777;
    font-style: italic;
    letter-spacing: 1px;
    opacity: 0;
    animation: fadeInUp 1.4s ease-out forwards;
    animation-delay: 7s;
}

.scroll-hint {
    margin-top: 40px;
    color: #a8875a;
    font-size: 14px;
    letter-spacing: 3px;
    text-transform: uppercase;
    opacity: 0;
    animation: fadeInUp 1.4s ease-out forwards, bob 2s ease-in-out infinite;
    animation-delay: 8.2s;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(24px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes bob {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(6px); }
}

.divider-gold {
    border: none;
    border-top: 2px solid #a8875a;
    margin: 50px 0 30px;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# INTRO / LANDING SECTION
# ----------------------------------------------------------------------------
st.markdown("""
<div class="intro-wrap">
<div class="greetings-title">Greetings.</div>
<div class="intro-line delay-1">
We see that you have made it past the interview round.
Congratulations, and welcome to the club.
</div>
<div class="intro-line delay-2">
To prove yourself truly worthy, you must solve 3 puzzles, each of which
unlocks more knowledge about the club. At the very end,
you will receive the letter of acceptance!
</div>
<div class="intro-line delay-3">
<span class="intro-warning">Do not cheat, and enjoy.</span>
</div>
<div class="scroll-hint">↓ scroll down to begin ↓</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider-gold">', unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# PUZZLE I — WORDLE (answer: SPINE)
# ----------------------------------------------------------------------------
st.markdown("""
<div class="scroll-box">
<h3>Puzzle I: The Word</h3>
<p>
A five-letter word lies at the heart of this club.
Guess it within <b>6 tries</b> to move forward.
</p>
<p>
Type letters, press <b>Enter</b> to submit a guess,
and <b>Backspace</b> to delete. You can also use the
on-screen keyboard. <b>Click the puzzle box below first</b>
so your keyboard connects to it.
</p>
<p>
<span style="color:#7fae6c;">Green</span> = right letter, right spot &nbsp;·&nbsp;
<span style="color:#c5a059;">Gold</span> = right letter, wrong spot &nbsp;·&nbsp;
<span style="color:#8a8378;">Grey</span> = not in the word.
</p>
</div>
""", unsafe_allow_html=True)

WORDLE_ANSWER = "SPINE"

wordle_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
<style>

* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    background: #211d17;
    color: #f0e4cf;
    font-family: Georgia, serif;
}}

body {{
    outline: none;
}}

#app {{
    padding: 10px 10px 24px;
    outline: none;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

#status {{
    background: #362f24;
    border: 1px solid #d8b878;
    border-radius: 7px;
    padding: 10px 14px;
    margin-bottom: 18px;
    text-align: center;
    width: 100%;
    max-width: 520px;
}}

#feedback {{
    margin-top: 6px;
    min-height: 20px;
    font-weight: bold;
}}

.success {{
    color: #81c784;
}}

.error {{
    color: #e57373;
}}

#grid {{
    display: grid;
    grid-template-rows: repeat(6, 1fr);
    gap: 8px;
    margin-bottom: 22px;
}}

.grid-row {{
    display: grid;
    grid-template-columns: repeat(5, 54px);
    gap: 8px;
}}

.tile {{
    width: 54px;
    height: 54px;
    border: 2px solid #a8875a;
    border-radius: 6px;
    background: #2b261d;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    font-weight: bold;
    text-transform: uppercase;
    color: #f0e4cf;
    transition: transform .15s, background .2s, border-color .2s;
}}

.tile.filled {{
    border-color: #d8b878;
}}

.tile.pop {{
    transform: scale(1.08);
}}

.tile.correct {{
    background: #6d8a5b;
    border-color: #6d8a5b;
    color: #fff;
}}

.tile.present {{
    background: #c4a04a;
    border-color: #c4a04a;
    color: #2b2216;
}}

.tile.absent {{
    background: #4a4132;
    border-color: #4a4132;
    color: #d9cdb4;
}}

.tile.shake {{
    animation: shake .35s;
}}

@keyframes shake {{
    10%, 90% {{ transform: translateX(-2px); }}
    20%, 80% {{ transform: translateX(4px); }}
    30%, 50%, 70% {{ transform: translateX(-8px); }}
    40%, 60% {{ transform: translateX(8px); }}
}}

#keyboard {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: center;
}}

.kb-row {{
    display: flex;
    gap: 6px;
}}

.kb-key {{
    min-width: 36px;
    height: 46px;
    padding: 0 8px;
    border: none;
    border-radius: 5px;
    background: #4a4132;
    color: #f0e4cf;
    font-family: Georgia, serif;
    font-weight: bold;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    user-select: none;
    text-transform: uppercase;
}}

.kb-key.wide {{
    min-width: 60px;
    font-size: 11px;
}}

.kb-key.correct {{
    background: #6d8a5b;
    color: #fff;
}}

.kb-key.present {{
    background: #c4a04a;
    color: #2b2216;
}}

.kb-key.absent {{
    background: #2b271f;
    color: #857b64;
}}

.kb-key:active {{
    transform: translateY(1px);
}}

#unlockBox {{
    margin-top: 22px;
    padding: 22px;
    background: #3c2a1c;
    border: 2px solid #d8b878;
    border-radius: 10px;
    text-align: center;
    width: 100%;
    max-width: 520px;
    display: none;
}}

#unlockBox.show {{
    display: block;
}}

.unlock-title {{
    font-size: 20px;
    font-weight: bold;
    color: #ffe9a8;
    margin-bottom: 8px;
    text-align: center;
}}

.unlock-lore {{
    font-size: 16px;
    line-height: 1.8;
    color: #f0e4cf;
    font-family: "Times New Roman", Times, serif;
    text-align: center;
}}

.cta-button {{
    margin-top: 18px;
    padding: 12px 26px;
    border: none;
    border-radius: 6px;
    background: #d8b878;
    color: #221d17;
    font-family: Georgia, serif;
    font-weight: bold;
    font-size: 15px;
    cursor: pointer;
}}

.cta-button:hover {{
    background: #ffe9a8;
}}

#qrBox, #crosswordBox, #foundersBox, #pianoBox {{
    margin-top: 22px;
    padding: 22px;
    background: #3c2a1c;
    border: 2px solid #d8b878;
    border-radius: 10px;
    text-align: center;
    width: 100%;
    max-width: 620px;
    display: none;
}}

#qrBox.show, #crosswordBox.show, #foundersBox.show, #pianoBox.show {{
    display: block;
}}

#pianoBox {{
    max-width: 1300px;
}}

.founders-lore {{
    font-size: 15px;
    line-height: 1.8;
    color: #f0e4cf;
    font-family: "Times New Roman", Times, serif;
    margin-bottom: 22px;
    text-align: left;
}}

.founders-grid {{
    display: flex;
    flex-direction: column;
    gap: 28px;
    margin-bottom: 22px;
    align-items: center;
}}

.founder-card {{
    text-align: center;
    width: 100%;
    max-width: 350px;
}}

.founder-name {{
    font-size: 16px;
    font-weight: bold;
    color: #ffe9a8;
    margin-bottom: 12px;
    letter-spacing: 1px;
}}

.founder-batch {{
    display: block;
    font-size: 13px;
    color: #d8b878;
    font-weight: normal;
    margin-top: 4px;
    letter-spacing: 0.5px;
}}

.founder-photos {{
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
}}

.founder-photo {{
    width: 100px;
    height: 120px;
    object-fit: cover;
    border: 2px solid #d8b878;
    border-radius: 6px;
    cursor: pointer;
    transition: transform .2s, box-shadow .2s;
}}

.founder-photo:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 12px rgba(216, 184, 120, 0.4);
}}

.lightbox {{
    display: none;
    position: fixed;
    z-index: 9999;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.9);
    animation: fadeIn .2s;
}}

.lightbox.show {{
    display: flex;
    align-items: center;
    justify-content: center;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

.lightbox-image {{
    max-width: 90%;
    max-height: 80vh;
    object-fit: contain;
    border-radius: 6px;
    border: 3px solid #d8b878;
}}

.lightbox-close {{
    position: absolute;
    top: 20px;
    right: 30px;
    color: #f0e4cf;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
    transition: color .2s;
}}

.lightbox-close:hover {{
    color: #ffe9a8;
}}

.lightbox-nav {{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(216, 184, 120, 0.2);
    color: #f0e4cf;
    border: none;
    font-size: 28px;
    padding: 12px 18px;
    cursor: pointer;
    border-radius: 4px;
    transition: background .2s;
    z-index: 10000;
}}

.lightbox-nav:hover {{
    background: rgba(216, 184, 120, 0.4);
}}

.lightbox-prev {{
    left: 20px;
}}

.lightbox-next {{
    right: 20px;
}}

.lightbox-counter {{
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    color: #f0e4cf;
    font-size: 14px;
    background: rgba(0, 0, 0, 0.5);
    padding: 8px 16px;
    border-radius: 4px;
    letter-spacing: 1px;
}}

.qr-caption {{
    margin-top: 14px;
    font-size: 15px;
    line-height: 1.7;
    color: #f0e4cf;
    font-family: "Times New Roman", Times, serif;
}}

.xword-title {{
    font-size: 20px;
    font-weight: bold;
    color: #ffe9a8;
    margin-bottom: 14px;
}}

.xword-layout {{
    display: flex;
    flex-wrap: wrap;
    gap: 26px;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
}}

.xword-grid {{
    display: grid;
    gap: 2px;
    background: #221d17;
    padding: 6px;
    border-radius: 6px;
}}

.xword-cell {{
    position: relative;
    width: 30px;
    height: 30px;
}}

.xword-cell input {{
    width: 100%;
    height: 100%;
    border: 1px solid #a8875a;
    background: #f0e4cf;
    color: #221d17;
    text-align: center;
    font-family: Georgia, serif;
    font-weight: bold;
    font-size: 15px;
    text-transform: uppercase;
    padding: 0;
    outline: none;
}}

.xword-cell input.active-word {{
    background: #e8d3a0;
}}

.xword-cell input:focus {{
    background: #ffe9a8;
}}

.xword-cell input.correct {{
    background: #6d8a5b;
    color: #fff;
}}

.xword-cell input.wrong {{
    background: #8b3a3a;
    color: #fff;
}}

.xword-cell.blocked {{
    background: #221d17;
}}

.xword-num {{
    position: absolute;
    top: 0;
    left: 2px;
    font-size: 8px;
    color: #221d17;
    z-index: 2;
    pointer-events: none;
}}

.clue-cols {{
    display: flex;
    gap: 26px;
    flex-wrap: wrap;
    max-width: 450px;
}}

.clue-col {{
    min-width: 200px;
}}

.clue-title {{
    font-weight: bold;
    color: #ffe9a8;
    margin-bottom: 6px;
    font-size: 14px;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.clue-list {{
    list-style: none;
    margin: 0 0 16px 0;
    padding: 0;
}}

.clue-item {{
    font-size: 13px;
    line-height: 1.5;
    color: #f0e4cf;
    margin-bottom: 10px;
    padding: 4px;
    border-radius: 3px;
}}

.clue-item.active-clue {{
    background: rgba(216, 184, 120, 0.2);
    color: #ffe9a8;
}}

.clue-num {{
    font-weight: bold;
    color: #d8b878;
}}

.clue-len {{
    color: #a8875a;
    font-style: italic;
}}

/* --- Puzzle III: The Melody (piano) --- */

#pianoApp {{
    width: max-content;
    min-width: 100%;
    padding: 8px 10px 20px;
    outline: none;
}}

#pianoStatus {{
    background: #2b261f;
    border: 1px solid #c5a059;
    border-radius: 7px;
    padding: 10px 14px;
    margin-bottom: 14px;
    text-align: center;
    min-width: 1250px;
}}

#pianoActivation {{
    color: #f3e5ab;
    font-size: 13px;
    margin-top: 4px;
}}

#pianoFeedback {{
    margin-top: 6px;
    min-height: 20px;
    font-weight: bold;
}}

.piano-wrapper {{
    position: relative;
    height: 245px;
    width: 1250px;
    background: #050505;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0 12px 25px rgba(0,0,0,.65);
    user-select: none;
    cursor: pointer;
}}

.piano {{
    position: relative;
    height: 225px;
    width: 1200px;
}}

.piano-key {{
    position: absolute;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    cursor: pointer;
    user-select: none;
    transition: background .04s, transform .04s;
}}

.white-key {{
    top: 0;
    width: 48px;
    height: 225px;
    background: linear-gradient(to bottom, #fff 0%, #e5e5e5 100%);
    border: 1px solid #111;
    border-radius: 0 0 5px 5px;
    color: #222;
    z-index: 1;
    padding-bottom: 12px;
}}

.black-key {{
    top: 0;
    width: 29px;
    height: 140px;
    background: linear-gradient(to bottom, #333 0%, #050505 100%);
    border: 1px solid #000;
    border-radius: 0 0 5px 5px;
    color: #f3e5ab;
    z-index: 3;
    padding-bottom: 9px;
}}

.white-key.active {{
    background: #cfcfcf;
    transform: translateY(2px);
}}

.black-key.active {{
    background: #666;
    transform: translateY(2px);
}}

.white-key.target {{
    box-shadow: inset 0 -7px 0 #c5a059;
}}

.black-key.target {{
    box-shadow: inset 0 -7px 0 #c5a059;
}}

.piano-key.wrong {{
    background: #8b3a3a !important;
    color: white;
}}

.note-label {{
    font-size: 11px;
    font-weight: bold;
}}

.computer-key {{
    margin-top: 5px;
    padding: 3px 6px;
    border-radius: 4px;
    background: #8b5a2b;
    color: white;
    font-size: 11px;
    font-family: Arial, sans-serif;
    font-weight: bold;
}}

.black-key .computer-key {{
    background: #8b5a2b;
}}

#sequence {{
    min-width: 1250px;
    margin-top: 18px;
    padding: 14px;
    background: #211e1a;
    border: 2px solid #80652e;
    border-radius: 9px;
    text-align: center;
}}

.sequence-title {{
    font-weight: bold;
    color: #f3e5ab;
    margin-bottom: 10px;
}}

.seq-note {{
    display: inline-block;
    min-width: 42px;
    padding: 7px 5px;
    margin: 3px;
    border-radius: 5px;
    background: #3a3328;
    border: 1px solid #80652e;
    font-family: monospace;
    font-size: 12px;
}}

.seq-note.current {{
    background: #c5a059;
    color: #17130e;
    font-weight: bold;
}}

.seq-note.done {{
    background: #536b45;
    color: white;
}}

.seq-note.wrong {{
    background: #8b3a3a;
    color: white;
}}

#acceptanceLetter {{
    min-width: 1250px;
    margin-top: 22px;
    padding: 25px;
    background: #211e1a;
    border: 2px solid #80652e;
    border-radius: 10px;
    text-align: center;
    color: #e0d5c1;
}}

#acceptanceLetter.locked {{
    opacity: 0.7;
}}

#letterLockedMessage {{
    font-size: 18px;
    color: #c5a059;
    padding: 20px;
}}

#letterContent {{
    border: 3px double #c5a059;
    padding: 25px;
    background: #2b261f;
}}

.letter-title {{
    font-size: 24px;
    font-weight: bold;
    color: #ffd700;
    margin-bottom: 15px;
}}

#playerName {{
    display: block;
    margin: 12px auto;
    padding: 10px;
    width: 300px;
    font-family: Georgia, serif;
    font-size: 16px;
    background: #17130e;
    color: #e0d5c1;
    border: 1px solid #c5a059;
    border-radius: 5px;
}}

#downloadLetter {{
    margin-top: 10px;
    padding: 12px 20px;
    background: #c5a059;
    color: #17130e;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    font-size: 15px;
    cursor: pointer;
}}

#downloadLetter:hover {{
    background: #ffd700;
}}

#letterPreview {{
    text-align: left;
    white-space: pre-wrap;
    margin-top: 20px;
    padding: 20px;
    background: #17130e;
    border: 1px solid #80652e;
    color: #e0d5c1;
}}

/* --- Chewie easter egg ---
   NOTE: this used to be `position: fixed` covering the whole screen.
   Inside a Streamlit components.html/st.iframe, the iframe is resized
   to exactly the height of its content (see resizeFrame() below) and
   never scrolls internally — the OUTER Streamlit page is what scrolls.
   That means a `position: fixed` element inside the iframe is pinned to
   the top of the (very tall) iframe box, not to the visible part of the
   browser window. By the time someone finishes Puzzle III they've
   scrolled far down the outer page, so the "fixed" popup was rendering
   off-screen, above the visible area — that's why it never appeared.
   Fix: render it as a normal in-flow card right after the piano/letter
   section (where the player already is) and scroll it into view. */

.chewie-overlay {{
    display: none;
    margin: 26px auto 0;
    padding: 30px 24px;
    max-width: 620px;
    width: 100%;
    border-radius: 14px;
    background: rgba(0, 0, 0, 0.85);
    cursor: pointer;
    text-align: center;
}}

.chewie-overlay.show {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.chewie-card {{
    text-align: center;
    cursor: default;
}}

.chewie-photo {{
    max-width: 320px;
    max-height: 60vh;
    object-fit: contain;
    border-radius: 14px;
    border: 4px solid #d8b878;
    box-shadow: 0 0 40px rgba(216, 184, 120, 0.5);
    animation: chewiePopIn 0.6s cubic-bezier(.34, 1.56, .64, 1) forwards;
}}

@keyframes chewiePopIn {{
    0% {{ transform: scale(0) rotate(-20deg); opacity: 0; }}
    55% {{ transform: scale(1.2) rotate(10deg); opacity: 1; }}
    75% {{ transform: scale(0.92) rotate(-5deg); }}
    100% {{ transform: scale(1) rotate(0deg); }}
}}

.chewie-caption {{
    margin-top: 16px;
    font-size: 22px;
    font-weight: bold;
    color: #ffe9a8;
    letter-spacing: 1px;
    text-shadow: 0 0 12px rgba(216, 184, 120, 0.6);
    animation: chewieWiggle 1.8s ease-in-out infinite;
}}

@keyframes chewieWiggle {{
    0%, 100% {{ transform: rotate(-2deg); }}
    50% {{ transform: rotate(2deg); }}
}}

.chewie-hint {{
    margin-top: 8px;
    font-size: 12px;
    color: #c9b98d;
    font-style: italic;
}}

/* --- Site credits footer --- */

.site-credits {{
    margin-top: 50px;
    padding-top: 22px;
    border-top: 1px solid #4a4132;
    width: 100%;
    max-width: 520px;
    text-align: center;
    font-size: 13px;
    line-height: 1.9;
    color: #a8875a;
    font-style: italic;
    letter-spacing: 0.5px;
}}

</style>
</head>

<body tabindex="0">

<div id="app" tabindex="0">

    <div id="status">
        <div id="feedback">Click the board below, then guess the 5-letter word.</div>
    </div>

    <div id="grid"></div>

    <div id="keyboard"></div>

    <div id="unlockBox">
        <div class="unlock-title">PUZZLE I — SOLVED</div>
        <div class="unlock-lore">
            <p>Welcome to Spine. We, the literature club of Plaksha
            University, call ourselves The Spine. Just like the spine
            of a novel binds the pages together, we hold together the
            literature culture in Plaksha.</p>
            <p>The name is inspired from a quote by Vladimir Nabokov,
            who says in his novel "Lectures on Literature", "A wise
            reader reads the book of genius not with his heart, not so
            much with his brain, but with his spine." He proceeds to
            not elaborate on this metaphor at all.</p>
        </div>
        <button class="cta-button" id="toPuzzle2Btn">Take me to puzzle 2</button>
    </div>

    <div id="qrBox">
        {QR_IMAGE_HTML}
        <div class="qr-caption">
            Here's the link to our Instagram. Follow, for it will also
            help you in the puzzles going forward.
        </div>
        <button class="cta-button" id="toCrosswordBtn">Continue to Puzzle II</button>
    </div>

    <div id="crosswordBox">
        <div class="xword-title">Puzzle II: The Crossword</div>
        <div class="xword-layout">
            <div class="xword-grid" id="xwordGrid"></div>
            <div class="clue-cols">
                <div class="clue-col">
                    <div class="clue-title">Across</div>
                    <ul class="clue-list" id="acrossClues"></ul>
                </div>
                <div class="clue-col">
                    <div class="clue-title">Down</div>
                    <ul class="clue-list" id="downClues"></ul>
                </div>
            </div>
        </div>
        <div id="xwordFeedback" style="margin-top:14px; font-weight:bold;"></div>
        <button class="cta-button" id="checkCrosswordBtn">Check Crossword</button>
    </div>

    <div id="foundersBox">
        <div class="xword-title">The Founding Members</div>
        <div class="founders-lore">
            <p>The following are the founding members of The Spine. Without any of them, the heart and soul of the club remains missing. They began the club, and did writing circles before the club was even solidified. As UG28 joined, we have only elaborated from the ground work that they set. These people are also (completely unrelated) extremely smart. [this was written by Avani]</p>
        </div>
        
        <div class="founders-grid">
            <div class="founder-card">
                <div class="founder-name">Maanal Gauri <span class="founder-batch">UG25</span></div>
                <div class="founder-photos">
                    <img src="{founder_photos['maanal'][0]}" class="founder-photo" onclick="openLightbox('maanal', 0)" alt="Maanal Gauri 1">
                    <img src="{founder_photos['maanal'][1]}" class="founder-photo" onclick="openLightbox('maanal', 1)" alt="Maanal Gauri 2">
                    <img src="{founder_photos['maanal'][2]}" class="founder-photo" onclick="openLightbox('maanal', 2)" alt="Maanal Gauri 3">
                </div>
            </div>

            <div class="founder-card">
                <div class="founder-name">Aman Paliwal <span class="founder-batch">UG26</span></div>
                <div class="founder-photos">
                    <img src="{founder_photos['aman'][0]}" class="founder-photo" onclick="openLightbox('aman', 0)" alt="Aman Paliwal 1">
                    <img src="{founder_photos['aman'][1]}" class="founder-photo" onclick="openLightbox('aman', 1)" alt="Aman Paliwal 2">
                    <img src="{founder_photos['aman'][2]}" class="founder-photo" onclick="openLightbox('aman', 2)" alt="Aman Paliwal 3">
                </div>
            </div>

            <div class="founder-card">
                <div class="founder-name">Trinav Talukdar <span class="founder-batch">UG27</span></div>
                <div class="founder-photos">
                    <img src="{founder_photos['trinav'][0]}" class="founder-photo" onclick="openLightbox('trinav', 0)" alt="Trinav Talukdar 1">
                    <img src="{founder_photos['trinav'][1]}" class="founder-photo" onclick="openLightbox('trinav', 1)" alt="Trinav Talukdar 2">
                    <img src="{founder_photos['trinav'][2]}" class="founder-photo" onclick="openLightbox('trinav', 2)" alt="Trinav Talukdar 3">
                </div>
            </div>
        </div>

        <button class="cta-button" id="toPuzzle3Btn">Take me to puzzle 3</button>
    </div>

    <div id="pianoBox">

        <div class="xword-title">Puzzle III: The Melody</div>

        <div class="unlock-lore" style="margin-bottom:18px;">
            <p>Play the secret melody of the ballad as your final challenge!
            Play the sequence using the <b>letter keys A–Y</b> or click the
            piano keys. The piano covers every note from <b>C#2 to C#4</b>.</p>
            <p><b>Click anywhere on the piano first</b> to activate the
            computer-keyboard controls.</p>
            <p><b>Beware:</b> If you play even one wrong note, the sequence
            will restart from the beginning.</p>
        </div>

        <div id="pianoApp" tabindex="0">

            <div id="pianoStatus">

                <div>
                    <b>Notes Played:</b>
                    <span id="playedNotes">None</span>
                </div>

                <div id="pianoActivation">
                    Click the piano once, then use A–Y to play.
                </div>

                <div id="pianoFeedback">
                    Ready.
                </div>

            </div>

            <div class="piano-wrapper" id="pianoWrapper">

                <div class="piano" id="piano">

                    {''.join(key_html)}

                    {''.join(black_html)}

                </div>

            </div>

            <div id="sequence">

                <div class="sequence-title">
                    Notes to Play
                </div>

                <div id="targetSequence"></div>

            </div>

            <div id="acceptanceLetter" class="locked">

                <div id="letterLockedMessage">

                    The Acceptance Letter is sealed.

                    <br>

                    <small>
                        Master the secret Melody to unlock it.
                    </small>

                </div>

                <div id="letterContent" style="display:none;">

                    <div class="letter-title">
                        THE GRAND ACCEPTANCE LETTER
                    </div>

                    <p>
                        You have successfully cleared the third and final trial
                    </p>

                    <label for="playerName">
                        Enter your name for the Scroll of Honor:
                    </label>

                    <input
                        id="playerName"
                        type="text"
                        value="Chewie"
                        maxlength="50"
                    >

                    <button id="downloadLetter">
                        Download Acceptance Letter
                    </button>

                    <pre id="letterPreview"></pre>

                </div>

            </div>

        </div>

    </div>

    <div id="lightbox" class="lightbox" onclick="closeLightbox(event)">
        <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
        <button class="lightbox-nav lightbox-prev" onclick="prevPhoto(event)">&#10094;</button>
        <img class="lightbox-image" id="lightboxImage" src="" alt="">
        <button class="lightbox-nav lightbox-next" onclick="nextPhoto(event)">&#10095;</button>
        <div class="lightbox-counter" id="lightboxCounter"></div>
    </div>

    <div id="chewieOverlay" class="chewie-overlay" onclick="closeChewie()">
        <div class="chewie-card">
            <img id="chewieImg" class="chewie-photo" src="" alt="Chewie">
            <div class="chewie-caption">😈 CHEWIE APPROVES! 😈</div>
            <div class="chewie-hint">(tap anywhere to dismiss)</div>
        </div>
    </div>

    <div class="site-credits">
        Website made by<br>
        Avani Mahawar<br>
        Malini Sen<br>
        Trinav Talukdar<br>
        with love &lt;3
    </div>

</div>

<script>

const CROSSWORD_DATA = {CROSSWORD_JSON};

const ANSWER = "{WORDLE_ANSWER}".toUpperCase();
const WORD_LEN = ANSWER.length;
const MAX_TRIES = 6;

let currentGuess = "";
let guesses = [];
let solved = false;
let locked = false;

const gridEl = document.getElementById("grid");
const feedbackEl = document.getElementById("feedback");
const keyboardEl = document.getElementById("keyboard");
const unlockBox = document.getElementById("unlockBox");

const keyStatus = {{}};

const rows = [];

function buildGrid() {{

    for (let r = 0; r < MAX_TRIES; r++) {{

        const rowEl = document.createElement("div");
        rowEl.className = "grid-row";

        const tileEls = [];

        for (let c = 0; c < WORD_LEN; c++) {{

            const tile = document.createElement("div");
            tile.className = "tile";
            rowEl.appendChild(tile);
            tileEls.push(tile);

        }}

        gridEl.appendChild(rowEl);
        rows.push(tileEls);

    }}

}}

const kbLayout = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L"],
    ["ENTER","Z","X","C","V","B","N","M","BACK"]
];

const kbKeyEls = {{}};

function buildKeyboard() {{

    kbLayout.forEach(rowKeys => {{

        const rowEl = document.createElement("div");
        rowEl.className = "kb-row";

        rowKeys.forEach(k => {{

            const btn = document.createElement("button");
            btn.className = "kb-key";
            btn.textContent = (k === "BACK") ? "⌫" : (k === "ENTER" ? "Enter" : k);

            if (k === "ENTER" || k === "BACK") {{
                btn.classList.add("wide");
            }}

            btn.addEventListener("click", () => handleKey(k));
            rowEl.appendChild(btn);

            if (k !== "ENTER" && k !== "BACK") {{
                kbKeyEls[k] = btn;
            }}

        }});

        keyboardEl.appendChild(rowEl);

    }});

}}

function currentRowIndex() {{
    return guesses.length;
}}

function renderCurrentGuess() {{

    const rowIdx = currentRowIndex();
    if (rowIdx >= MAX_TRIES) return;

    const tiles = rows[rowIdx];

    for (let i = 0; i < WORD_LEN; i++) {{

        const letter = currentGuess[i] || "";
        tiles[i].textContent = letter;

        if (letter) {{
            tiles[i].classList.add("filled");
        }} else {{
            tiles[i].classList.remove("filled");
        }}

    }}

}}

function evaluateGuess(guess) {{

    const result = new Array(WORD_LEN).fill("absent");
    const answerArr = ANSWER.split("");
    const guessArr = guess.split("");
    const used = new Array(WORD_LEN).fill(false);

    for (let i = 0; i < WORD_LEN; i++) {{
        if (guessArr[i] === answerArr[i]) {{
            result[i] = "correct";
            used[i] = true;
        }}
    }}

    for (let i = 0; i < WORD_LEN; i++) {{

        if (result[i] === "correct") continue;

        for (let j = 0; j < WORD_LEN; j++) {{

            if (!used[j] && guessArr[i] === answerArr[j]) {{
                result[i] = "present";
                used[j] = true;
                break;
            }}

        }}

    }}

    return result;

}}

function updateKeyStatus(letter, status) {{

    const rank = {{ "absent": 0, "present": 1, "correct": 2 }};

    if (!(letter in keyStatus) || rank[status] > rank[keyStatus[letter]]) {{
        keyStatus[letter] = status;
    }}

    const btn = kbKeyEls[letter];
    if (!btn) return;

    btn.classList.remove("correct", "present", "absent");
    btn.classList.add(keyStatus[letter]);

}}

function submitGuess() {{

    if (locked) return;

    if (currentGuess.length !== WORD_LEN) {{

        shakeRow(currentRowIndex());
        feedbackEl.innerHTML = '<span class="error">Not enough letters.</span>';
        return;

    }}

    const rowIdx = currentRowIndex();
    const tiles = rows[rowIdx];
    const result = evaluateGuess(currentGuess);

    tiles.forEach((tile, i) => {{

        setTimeout(() => {{

            tile.classList.add(result[i]);
            tile.classList.add("pop");
            setTimeout(() => tile.classList.remove("pop"), 150);

        }}, i * 120);

        updateKeyStatus(currentGuess[i], result[i]);

    }});

    guesses.push(currentGuess);

    if (currentGuess === ANSWER) {{

        solved = true;
        locked = true;

        setTimeout(() => {{

            feedbackEl.innerHTML = '<span class="success">FLAWLESS! The word was ' + ANSWER + '.</span>';
            unlockBox.classList.add("show");

            if (window.confetti) {{
                confetti({{
                    particleCount: 160,
                    spread: 90,
                    origin: {{ y: 0.5 }},
                    colors: ["#d8b878", "#f0e4cf", "#6d8a5b", "#c4a04a"]
                }});
            }}

            window.parent.postMessage(
                {{ type: "STREAMLIT_WORDLE_PASSED" }},
                "*"
            );

        }}, WORD_LEN * 120 + 200);

    }}

    else if (guesses.length >= MAX_TRIES) {{

        locked = true;

        setTimeout(() => {{

            feedbackEl.innerHTML = '<span class="error">Out of tries. The word was ' + ANSWER + '.</span>';

        }}, WORD_LEN * 120 + 200);

    }}

    else {{

        setTimeout(() => {{
            feedbackEl.textContent = "Keep guessing.";
        }}, WORD_LEN * 120 + 200);

    }}

    currentGuess = "";

}}

function shakeRow(rowIdx) {{

    const tiles = rows[rowIdx];

    tiles.forEach(tile => {{
        tile.classList.add("shake");
        setTimeout(() => tile.classList.remove("shake"), 350);
    }});

}}

function handleKey(key) {{

    if (locked) return;

    if (key === "ENTER") {{
        submitGuess();
        return;
    }}

    if (key === "BACK") {{
        currentGuess = currentGuess.slice(0, -1);
        renderCurrentGuess();
        return;
    }}

    if (/^[A-Z]$/.test(key) && currentGuess.length < WORD_LEN) {{
        currentGuess += key;
        renderCurrentGuess();
    }}

}}

function activateKeyboard() {{

    document.getElementById("app").focus();

}}

document
    .getElementById("app")
    .addEventListener("mousedown", activateKeyboard);

document.addEventListener("keydown", (event) => {{

    if (locked) return;

    const key = event.key.toUpperCase();

    if (key === "ENTER") {{
        event.preventDefault();
        handleKey("ENTER");
        return;
    }}

    if (key === "BACKSPACE") {{
        event.preventDefault();
        handleKey("BACK");
        return;
    }}

    if (/^[A-Z]$/.test(key)) {{
        handleKey(key);
    }}

}});

buildGrid();
buildKeyboard();

/* ============= Crossword Setup ============= */

let xwordBuilt = false;
let xwordSolved = false;
let xwordCurrentDir = "A";
const xwordCellEls = [];
const xwordCellWords = [];

function buildCrossword() {{
    if (xwordBuilt) return;
    xwordBuilt = true;

    const grid = CROSSWORD_DATA.grid;
    const rows = CROSSWORD_DATA.rows;
    const cols = CROSSWORD_DATA.cols;

    for (let r = 0; r < rows; r++) {{
        xwordCellEls.push(new Array(cols).fill(null));
        xwordCellWords.push(
            new Array(cols).fill(null).map(() => ({{ A: null, D: null }}))
        );
    }}

    // Use the explicit clue numbers from CROSSWORD_DATA.
    // Do not generate numbers from grid position, because the clue
    // numbers are part of the puzzle itself.
    const numMap = {{}};

    Object.keys(CROSSWORD_DATA.clues).forEach(dir => {{
        CROSSWORD_DATA.clues[dir].forEach(clue => {{
            numMap[clue.row + "_" + clue.col] = clue.num;
        }});
    }});

    // Assign word indices to cells.
    const clues = CROSSWORD_DATA.clues;

    clues.across.forEach((clue, idx) => {{
        const r = clue.row;
        const c = clue.col;

        for (let i = 0; i < clue.length; i++) {{
            if (
                r >= 0 && r < rows &&
                c + i >= 0 && c + i < cols &&
                grid[r][c + i] !== null
            ) {{
                xwordCellWords[r][c + i].A = idx;
            }}
        }}
    }});

    clues.down.forEach((clue, idx) => {{
        const r = clue.row;
        const c = clue.col;

        for (let i = 0; i < clue.length; i++) {{
            if (
                r + i >= 0 && r + i < rows &&
                c >= 0 && c < cols &&
                grid[r + i][c] !== null
            ) {{
                xwordCellWords[r + i][c].D = idx;
            }}
        }}
    }});

    // Render grid.
    const gridEl = document.getElementById("xwordGrid");
    gridEl.style.gridTemplateColumns = "repeat(" + cols + ", 30px)";
    gridEl.style.gridTemplateRows = "repeat(" + rows + ", 30px)";

    for (let r = 0; r < rows; r++) {{
        for (let c = 0; c < cols; c++) {{

            const cellWrap = document.createElement("div");
            cellWrap.className = "xword-cell";

            if (grid[r][c] === null) {{
                cellWrap.classList.add("blocked");
                gridEl.appendChild(cellWrap);
                continue;
            }}

            const key = r + "_" + c;

            if (numMap[key]) {{
                const numEl = document.createElement("span");
                numEl.className = "xword-num";
                numEl.textContent = numMap[key];
                cellWrap.appendChild(numEl);
            }}

            const input = document.createElement("input");
            input.maxLength = 1;
            input.dataset.row = r;
            input.dataset.col = c;
            input.autocomplete = "off";

            input.addEventListener("focus", () => setActiveCell(r, c));

            input.addEventListener("click", () => {{
                const cellInfo = xwordCellWords[r][c];

                if (cellInfo.A !== null && cellInfo.D !== null) {{
                    xwordCurrentDir = (xwordCurrentDir === "A") ? "D" : "A";
                }} else if (cellInfo.A !== null) {{
                    xwordCurrentDir = "A";
                }} else if (cellInfo.D !== null) {{
                    xwordCurrentDir = "D";
                }}

                setActiveCell(r, c);
            }});

            input.addEventListener("keydown", (e) => onXwordKeydown(e, r, c));
            input.addEventListener("input", (e) => onXwordInput(e, r, c));

            cellWrap.appendChild(input);
            gridEl.appendChild(cellWrap);
            xwordCellEls[r][c] = input;
        }}
    }}

    renderClues();
    document.getElementById("checkCrosswordBtn").addEventListener("click", checkCrossword);
}}

function renderClues() {{
    const acrossCluesEl = document.getElementById("acrossClues");
    const downCluesEl = document.getElementById("downClues");

    acrossCluesEl.innerHTML = "";
    downCluesEl.innerHTML = "";

    CROSSWORD_DATA.clues.across.forEach((clue, idx) => {{
        const li = document.createElement("li");
        li.className = "clue-item";
        li.dataset.num = clue.num;
        li.dataset.dir = "A";
        li.dataset.idx = idx;

        li.innerHTML =
            `<span class="clue-num">${{clue.num}}.</span> ` +
            `${{clue.clue}} ` +
            `<span class="clue-len">(${{clue.length}})</span>`;

        li.addEventListener("click", () => jumpToClue("A", idx));
        acrossCluesEl.appendChild(li);
    }});

    CROSSWORD_DATA.clues.down.forEach((clue, idx) => {{
        const li = document.createElement("li");
        li.className = "clue-item";
        li.dataset.num = clue.num;
        li.dataset.dir = "D";
        li.dataset.idx = idx;

        li.innerHTML =
            `<span class="clue-num">${{clue.num}}.</span> ` +
            `${{clue.clue}} ` +
            `<span class="clue-len">(${{clue.length}})</span>`;

        li.addEventListener("click", () => jumpToClue("D", idx));
        downCluesEl.appendChild(li);
    }});
}}

function jumpToClue(dir, idx) {{
    const clue = CROSSWORD_DATA.clues[dir === "A" ? "across" : "down"][idx];

    xwordCurrentDir = dir;

    const el = xwordCellEls[clue.row][clue.col];

    if (el) el.focus();

    setActiveCell(clue.row, clue.col);
}}

function clearActiveHighlight() {{
    document.querySelectorAll(".xword-cell input.active-word")
        .forEach(el => el.classList.remove("active-word"));

    document.querySelectorAll(".clue-item.active-clue")
        .forEach(el => el.classList.remove("active-clue"));
}}

function setActiveCell(r, c) {{
    if (xwordSolved) return;

    clearActiveHighlight();

    const cellInfo = xwordCellWords[r][c];

    let dir = xwordCurrentDir;

    if (cellInfo[dir] === null) {{
        dir = (dir === "A") ? "D" : "A";

        if (cellInfo[dir] !== null) {{
            xwordCurrentDir = dir;
        }}
    }}

    const wordIdx = cellInfo[xwordCurrentDir];

    if (wordIdx === null) return;

    const clue =
        CROSSWORD_DATA.clues[
            xwordCurrentDir === "A" ? "across" : "down"
        ][wordIdx];

    // Highlight exactly clue.length cells.
    for (let k = 0; k < clue.length; k++) {{
        const rr = xwordCurrentDir === "A" ? clue.row : clue.row + k;
        const cc = xwordCurrentDir === "A" ? clue.col + k : clue.col;

        if (xwordCellEls[rr] && xwordCellEls[rr][cc]) {{
            xwordCellEls[rr][cc].classList.add("active-word");
        }}
    }}

    const clueEl = document.querySelector(
        '.clue-item[data-num="' +
        clue.num +
        '"][data-dir="' +
        xwordCurrentDir +
        '"]'
    );

    if (clueEl) clueEl.classList.add("active-clue");
}}

function moveFocus(r, c, dir, step) {{
    let rr = r;
    let cc = c;

    while (true) {{
        rr += (dir === "D") ? step : 0;
        cc += (dir === "A") ? step : 0;

        if (
            rr < 0 ||
            rr >= CROSSWORD_DATA.rows ||
            cc < 0 ||
            cc >= CROSSWORD_DATA.cols
        ) {{
            return;
        }}

        if (xwordCellEls[rr][cc]) {{
            xwordCellEls[rr][cc].focus();
            return;
        }}

        return;
    }}
}}

function onXwordInput(e, r, c) {{
    const val = e.target.value.toUpperCase().replace(/[^A-Z]/g, "");

    e.target.value = val.slice(-1);
    e.target.classList.remove("correct", "wrong");

    if (val) {{
        moveFocus(r, c, xwordCurrentDir, 1);
    }}
}}

function onXwordKeydown(e, r, c) {{
    if (xwordSolved) return;

    if (e.key === "Backspace") {{
        if (!e.target.value) {{
            e.preventDefault();
            moveFocus(r, c, xwordCurrentDir, -1);
        }}
        return;
    }}

    if (e.key === "ArrowRight") {{
        e.preventDefault();
        xwordCurrentDir = "A";
        moveFocus(r, c, "A", 1);
        return;
    }}

    if (e.key === "ArrowLeft") {{
        e.preventDefault();
        xwordCurrentDir = "A";
        moveFocus(r, c, "A", -1);
        return;
    }}

    if (e.key === "ArrowDown") {{
        e.preventDefault();
        xwordCurrentDir = "D";
        moveFocus(r, c, "D", 1);
        return;
    }}

    if (e.key === "ArrowUp") {{
        e.preventDefault();
        xwordCurrentDir = "D";
        moveFocus(r, c, "D", -1);
        return;
    }}
}}

function checkCrossword() {{
    const grid = CROSSWORD_DATA.grid;

    let allFilled = true;
    let allCorrect = true;

    for (let r = 0; r < CROSSWORD_DATA.rows; r++) {{
        for (let c = 0; c < CROSSWORD_DATA.cols; c++) {{

            if (grid[r][c] === null) continue;

            const el = xwordCellEls[r][c];
            const val = el.value.toUpperCase();

            if (!val) {{
                allFilled = false;
                continue;
            }}

            if (val === grid[r][c]) {{
                el.classList.add("correct");
                el.classList.remove("wrong");
            }} else {{
                allCorrect = false;
                el.classList.remove("correct");
                el.classList.add("wrong");
            }}
        }}
    }}

    const feedbackEl = document.getElementById("xwordFeedback");

    if (!allFilled) {{
        feedbackEl.innerHTML =
            '<span style="color:#e57373;">Fill in every cell first.</span>';
        return;
    }}

    if (!allCorrect) {{
        feedbackEl.innerHTML =
            '<span style="color:#e57373;">Some letters are off — green is correct, red is wrong.</span>';
        return;
    }}

    xwordSolved = true;

    feedbackEl.innerHTML =
        '<span style="color:#81c784;">FLAWLESS! Puzzle II solved.</span>';

    if (window.confetti) {{
        confetti({{
            particleCount: 200,
            spread: 100,
            origin: {{ y: 0.5 }},
            colors: ["#d8b878", "#f0e4cf", "#6d8a5b", "#c4a04a"]
        }});
    }}

    setTimeout(() => {{
        document.getElementById("foundersBox").classList.add("show");
        setTimeout(resizeFrame, 50);

        document.getElementById("foundersBox").scrollIntoView({{
            behavior: "smooth",
            block: "start"
        }});
    }}, 1000);

    window.parent.postMessage(
        {{ type: "STREAMLIT_CROSSWORD_PASSED" }},
        "*"
    );
}}

/* ============= Lightbox for founder photos ============= */

const lighboxPhotos = {FOUNDER_PHOTOS_JSON};

let currentLightboxMember = null;
let currentLightboxIndex = 0;

function openLightbox(member, index) {{
    currentLightboxMember = member;
    currentLightboxIndex = index;
    const lightbox = document.getElementById("lightbox");
    const image = document.getElementById("lightboxImage");
    image.src = lighboxPhotos[member][index];
    updateLightboxCounter();
    lightbox.classList.add("show");
}}

function closeLightbox(event) {{
    if (event && event.target !== document.getElementById("lightbox")) return;
    document.getElementById("lightbox").classList.remove("show");
}}

function nextPhoto(event) {{
    event.stopPropagation();
    const photos = lighboxPhotos[currentLightboxMember];
    currentLightboxIndex = (currentLightboxIndex + 1) % photos.length;
    document.getElementById("lightboxImage").src = photos[currentLightboxIndex];
    updateLightboxCounter();
}}

function prevPhoto(event) {{
    event.stopPropagation();
    const photos = lighboxPhotos[currentLightboxMember];
    currentLightboxIndex = (currentLightboxIndex - 1 + photos.length) % photos.length;
    document.getElementById("lightboxImage").src = photos[currentLightboxIndex];
    updateLightboxCounter();
}}

function updateLightboxCounter() {{
    document.getElementById("lightboxCounter").textContent = 
        (currentLightboxIndex + 1) + " / " + lighboxPhotos[currentLightboxMember].length;
}}

// Close lightbox on ESC key
document.addEventListener("keydown", (e) => {{
    if (e.key === "Escape") closeLightbox();
}});

/* ============= Chewie easter egg ============= */

const CHEWIE_URI = {CHEWIE_URI_JSON};

function triggerChewiePopup() {{

    if (!CHEWIE_URI) {{
        console.warn(
            "Chewie image not found — make sure chewie.png/.jpg/.jpeg/" +
            ".webp/.gif exists in the same folder as this script."
        );
        return;
    }}

    const overlay = document.getElementById("chewieOverlay");
    const img = document.getElementById("chewieImg");

    // Restart the pop-in animation even if it already played once.
    img.style.animation = "none";
    img.offsetHeight;
    img.style.animation = "";

    img.src = CHEWIE_URI;
    overlay.classList.add("show");

    // The overlay is now visible in normal document flow (see the CSS
    // comment above for why `position: fixed` didn't work inside this
    // auto-resizing iframe). Resize the frame to fit the new content,
    // then scroll it into view so the player actually sees it without
    // having to scroll manually.
    resizeFrame();

    setTimeout(() => {{
        overlay.scrollIntoView({{ behavior: "smooth", block: "center" }});
    }}, 60);

    if (window.confetti) {{
        confetti({{
            particleCount: 140,
            spread: 110,
            origin: {{ y: 0.4 }},
            colors: ["#d8b878", "#f0e4cf", "#6d8a5b", "#c4a04a"]
        }});
    }}

}}

function closeChewie() {{
    document.getElementById("chewieOverlay").classList.remove("show");
    resizeFrame();
}}

// Close chewie popup on ESC key
document.addEventListener("keydown", (e) => {{
    if (e.key === "Escape") closeChewie();
}});

/* ============= Puzzle III: The Melody (piano) ============= */

const melody = {melody_sequence!r};

const noteElements = {{}};
const keyMap = {{}};

let playedSequence = [];

let pianoCompleted = false;

let audioCtx = null;

let activeOscillators = {{}};

let pianoBuilt = false;

function initAudio() {{

    if (!audioCtx) {{

        audioCtx =
            new (window.AudioContext ||
                 window.webkitAudioContext)();

    }}

    if (audioCtx.state === "suspended") {{

        audioCtx.resume();

    }}

}}

function playTone(freq, id) {{

    initAudio();

    const now = audioCtx.currentTime;

    // Soft synthesized piano tone: a fundamental plus a quiet
    // upper harmonic, shaped with a piano-like attack and decay.
    const masterGain = audioCtx.createGain();
    const filter = audioCtx.createBiquadFilter();

    filter.type = "lowpass";
    filter.frequency.setValueAtTime(4200, now);
    filter.Q.setValueAtTime(0.7, now);

    masterGain.gain.setValueAtTime(0.0001, now);
    masterGain.gain.exponentialRampToValueAtTime(0.20, now + 0.008);
    masterGain.gain.exponentialRampToValueAtTime(0.075, now + 0.16);
    masterGain.gain.exponentialRampToValueAtTime(0.0001, now + 1.05);

    const fundamental = audioCtx.createOscillator();
    const harmonic = audioCtx.createOscillator();

    fundamental.type = "triangle";
    harmonic.type = "sine";

    fundamental.frequency.setValueAtTime(freq, now);
    harmonic.frequency.setValueAtTime(freq * 2, now);

    const harmonicGain = audioCtx.createGain();
    harmonicGain.gain.setValueAtTime(0.0001, now);
    harmonicGain.gain.exponentialRampToValueAtTime(0.055, now + 0.006);
    harmonicGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.55);

    fundamental.connect(masterGain);
    harmonic.connect(harmonicGain);
    harmonicGain.connect(masterGain);
    masterGain.connect(filter);
    filter.connect(audioCtx.destination);

    fundamental.start(now);
    harmonic.start(now);

    fundamental.stop(now + 1.1);
    harmonic.stop(now + 0.65);

    activeOscillators[id] = [fundamental, harmonic];

    setTimeout(() => {{

        delete activeOscillators[id];

    }}, 1150);

}}

function renderTargetSequence() {{

    const container =
        document.getElementById("targetSequence");

    container.innerHTML = "";

    melody.forEach((note, index) => {{

        const el =
            document.createElement("span");

        el.className = "seq-note";

        el.id = "seq-" + index;

        el.textContent = note;

        container.appendChild(el);

    }});

    updateTargetHighlight();

}}

function updateTargetHighlight() {{

    melody.forEach((_, i) => {{

        const el =
            document.getElementById("seq-" + i);

        if (!el) return;

        el.classList.remove(
            "current",
            "done",
            "wrong"
        );

        if (i < playedSequence.length) {{

            el.classList.add("done");

        }}

        else if (i === playedSequence.length) {{

            el.classList.add("current");

        }}

    }});

}}

function flashKey(el) {{

    el.classList.add("active");

    setTimeout(() => {{

        el.classList.remove("active");

    }}, 130);

}}

function updatePlayedDisplay() {{

    document.getElementById("playedNotes").textContent =

        playedSequence.length

            ? playedSequence.join(" → ")

            : "None";

}}

function handleNotePlay(note, freq, element) {{

    if (pianoCompleted) return;

    initAudio();

    flashKey(element);

    playTone(
        freq,
        note + Date.now()
    );

    const expected =
        melody[playedSequence.length];

    if (note === expected) {{

        playedSequence.push(note);

        updatePlayedDisplay();

        updateTargetHighlight();

        if (
            playedSequence.length ===
            melody.length
        ) {{

            pianoCompleted = true;

            document.getElementById("pianoFeedback").innerHTML =

                '<span class="success">' +
                'FLAWLESS! Challenge passed!' +
                '</span>';

            const letter =
                document.getElementById(
                    "acceptanceLetter"
                );

            letter.classList.remove("locked");

            letter.classList.add("unlocked");

            document.getElementById(
                "letterLockedMessage"
            ).style.display = "none";

            document.getElementById(
                "letterContent"
            ).style.display = "block";

            updateLetterPreview();

            window.parent.postMessage(
                {{
                    type: "STREAMLIT_PIANO_PASSED"
                }},
                "*"
            );

            triggerChewiePopup();

        }}

        else {{

            document.getElementById(
                "pianoFeedback"
            ).textContent =
                "Correct — keep going!";

        }}

    }}

    else {{

        playedSequence = [];

        updatePlayedDisplay();

        updateTargetHighlight();

        document.getElementById(
            "pianoFeedback"
        ).innerHTML =

            '<span class="error">' +
            'Wrong note! The sequence has ' +
            'restarted from the beginning.' +
            '</span>';

        element.classList.add("wrong");

        setTimeout(() => {{

            element.classList.remove("wrong");

        }}, 500);

        setTimeout(() => {{

            updateTargetHighlight();

            document.getElementById(
                "pianoFeedback"
            ).textContent =
                "Ready — start again from the first note.";

        }}, 500);

    }}

}}

function activatePianoKeyboard() {{

    document.body.focus();

    document.getElementById("pianoApp").focus();

    document.getElementById(
        "pianoActivation"
    ).textContent =
        "Keyboard active : use A–Y to play the piano.";

}}

function generateLetter() {{

    const playerName =
        document
            .getElementById("playerName")
            .value
            .trim() || "Chewie";

    return `
=======================================================
          WELCOME TO THE RANKS OF THE SPINE
                  LITERATURE CLUB
=======================================================


                    ${{playerName.toUpperCase()}}

Who has successfully cleared all trials and proven 
themselves worthy!
=======================================================
`;

}}

function updateLetterPreview() {{

    document.getElementById(
        "letterPreview"
    ).textContent =
        generateLetter();

}}

function buildPiano() {{

    if (pianoBuilt) return;
    pianoBuilt = true;

    document
        .querySelectorAll(".piano-key")
        .forEach(el => {{

            const note =
                el.dataset.note;

            const freq =
                Number(el.dataset.freq);

            const key =
                el.dataset.key.toLowerCase();

            noteElements[note] = el;

            keyMap[key] = {{

                note: note,

                freq: freq,

                element: el

            }};

        }});

    document
        .getElementById("pianoWrapper")
        .addEventListener(
            "mousedown",
            () => {{

                activatePianoKeyboard();

            }}
        );

    document.addEventListener(
        "keydown",
        (event) => {{

            // Do not capture keyboard input while the user is typing
            // into the acceptance-letter name field.
            const target = event.target;
            if (
                target &&
                (target.tagName === "INPUT" ||
                 target.tagName === "TEXTAREA" ||
                 target.isContentEditable)
            ) {{
                return;
            }}

            const key =
                event.key.toLowerCase();

            if (!keyMap[key])
                return;

            if (event.repeat)
                return;

            event.preventDefault();

            activatePianoKeyboard();

            const item =
                keyMap[key];

            handleNotePlay(
                item.note,
                item.freq,
                item.element
            );

        }}
    );

    document
        .getElementById("playerName")
        .addEventListener(
            "input",
            updateLetterPreview
        );

    document
        .getElementById("downloadLetter")
        .addEventListener(
            "click",
            () => {{

                const letter =
                    generateLetter();

                const playerName =
                    document
                        .getElementById("playerName")
                        .value
                        .trim() || "Brave Bard";

                const blob =
                    new Blob(
                        [letter],
                        {{
                            type: "text/plain"
                        }}
                    );

                const url =
                    URL.createObjectURL(blob);

                const link =
                    document.createElement("a");

                link.href = url;

                link.download =
                    "Acceptance_Letter_" +
                    playerName.replace(
                        /\\s+/g,
                        "_"
                    ) +
                    ".txt";

                document
                    .body
                    .appendChild(link);

                link.click();

                document
                    .body
                    .removeChild(link);

                URL.revokeObjectURL(url);

            }}
        );

    renderTargetSequence();

    updateLetterPreview();

    activatePianoKeyboard();

}}

/* ---------- Frame resizing ---------- */

function resizeFrame() {{
    try {{
        if (window.frameElement) {{
            window.frameElement.style.height =
                document.documentElement.scrollHeight + "px";
        }}
    }} catch (e) {{}}
}}

window.addEventListener("load", resizeFrame);
window.addEventListener("resize", resizeFrame);

new MutationObserver(resizeFrame).observe(document.body, {{
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ["class", "style"]
}});

setTimeout(resizeFrame, 50);
setTimeout(resizeFrame, 300);
setTimeout(resizeFrame, 1000);

/* ---------- Reveal flow ---------- */

document.getElementById("toPuzzle2Btn").addEventListener("click", () => {{
    document.getElementById("qrBox").classList.add("show");
    setTimeout(resizeFrame, 50);
    setTimeout(() => {{
        document.getElementById("qrBox").scrollIntoView({{ behavior: "smooth", block: "center" }});
    }}, 100);
}});

document.getElementById("toCrosswordBtn").addEventListener("click", () => {{
    document.getElementById("crosswordBox").classList.add("show");
    buildCrossword();
    setTimeout(resizeFrame, 50);
    setTimeout(() => {{
        document.getElementById("crosswordBox").scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}, 100);
}});

document.getElementById("toPuzzle3Btn").addEventListener("click", () => {{
    document.getElementById("pianoBox").classList.add("show");
    buildPiano();
    setTimeout(resizeFrame, 50);
    setTimeout(() => {{
        document.getElementById("pianoBox").scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}, 100);
}});

</script>

</body>
</html>
"""

render_html_frame(wordle_html, height=820, scrolling=True)
