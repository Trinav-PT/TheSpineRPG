import base64
import json
from pathlib import Path

import streamlit as st

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
    dropped next to this script (instagram_qr.png/.jpg/.jpeg), otherwise
    fall back to a stylised placeholder graphic."""
    here = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")

    for filename in ("instagram_qr.png", "instagram_qr.jpg", "instagram_qr.jpeg"):
        candidate = here / filename
        if candidate.exists():
            data = candidate.read_bytes()
            b64 = base64.b64encode(data).decode("utf-8")
            ext = candidate.suffix.lstrip(".").lower()
            mime = "jpeg" if ext in ("jpg", "jpeg") else ext
            return (
                f'<img src="data:image/{mime};base64,{b64}" alt="Instagram QR code" '
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
            "clue": "This word is the answer to the phylum clue above — the third-largest phylum in the animal kingdom.",
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
            "clue": "This and the next clue are 2 words, part of 1 big phrase. For this word: a group into which animals, plants, etc. are divided, smaller than a kingdom and larger than a class.",
            "length": 6,
            "row": 6,
            "col": 10
        },
        {
            "num": 4,
            "clue": "We brought this boarding school to Plaksha in one of our earlier events.",
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
To fully enter, you must solve 3 puzzles, each of which
unlocks more knowledge about the club. At the very end,
you will receive the link to join the group.
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

#qrBox, #crosswordBox, #foundersBox {{
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

#qrBox.show, #crosswordBox.show, #foundersBox.show {{
    display: block;
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
            <p>The following are the founding members of The Spine. Without any of them, the heart and soul of the club remains missing. They began the club, and did writing circles before the club was even solidified. As UG28 joined, we have only elaborated from the ground work that they set. These people are also (completely unrelated) extremely smart.</p>
        </div>
        
        <div class="founders-grid">
            <div class="founder-card">
                <div class="founder-name">Maanal Gauri <span class="founder-batch">UG25</span></div>
                <div class="founder-photos">
                    <img src="https://via.placeholder.com/180x200?text=Maanal+1" class="founder-photo" onclick="openLightbox('maanal', 0)" alt="Maanal Gauri 1">
                    <img src="https://via.placeholder.com/180x200?text=Maanal+2" class="founder-photo" onclick="openLightbox('maanal', 1)" alt="Maanal Gauri 2">
                    <img src="https://via.placeholder.com/180x200?text=Maanal+3" class="founder-photo" onclick="openLightbox('maanal', 2)" alt="Maanal Gauri 3">
                </div>
            </div>

            <div class="founder-card">
                <div class="founder-name">Aman Paliwal <span class="founder-batch">UG26</span></div>
                <div class="founder-photos">
                    <img src="https://via.placeholder.com/180x200?text=Aman+1" class="founder-photo" onclick="openLightbox('aman', 0)" alt="Aman Paliwal 1">
                    <img src="https://via.placeholder.com/180x200?text=Aman+2" class="founder-photo" onclick="openLightbox('aman', 1)" alt="Aman Paliwal 2">
                    <img src="https://via.placeholder.com/180x200?text=Aman+3" class="founder-photo" onclick="openLightbox('aman', 2)" alt="Aman Paliwal 3">
                </div>
            </div>

            <div class="founder-card">
                <div class="founder-name">Trinav Talukdar <span class="founder-batch">UG27</span></div>
                <div class="founder-photos">
                    <img src="https://via.placeholder.com/180x200?text=Trinav+1" class="founder-photo" onclick="openLightbox('trinav', 0)" alt="Trinav Talukdar 1">
                    <img src="https://via.placeholder.com/180x200?text=Trinav+2" class="founder-photo" onclick="openLightbox('trinav', 1)" alt="Trinav Talukdar 2">
                    <img src="https://via.placeholder.com/180x200?text=Trinav+3" class="founder-photo" onclick="openLightbox('trinav', 2)" alt="Trinav Talukdar 3">
                </div>
            </div>
        </div>

        <button class="cta-button" id="toPuzzle3Btn">Take me to puzzle 3</button>
    </div>

    <div id="lightbox" class="lightbox" onclick="closeLightbox(event)">
        <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
        <button class="lightbox-nav lightbox-prev" onclick="prevPhoto(event)">&#10094;</button>
        <img class="lightbox-image" id="lightboxImage" src="" alt="">
        <button class="lightbox-nav lightbox-next" onclick="nextPhoto(event)">&#10095;</button>
        <div class="lightbox-counter" id="lightboxCounter"></div>
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

function buildCrossword() {
    if (xwordBuilt) return;
    xwordBuilt = true;

    const grid = CROSSWORD_DATA.grid;
    const rows = CROSSWORD_DATA.rows;
    const cols = CROSSWORD_DATA.cols;

    for (let r = 0; r < rows; r++) {
        xwordCellEls.push(new Array(cols).fill(null));
        xwordCellWords.push(
            new Array(cols).fill(null).map(() => ({ A: null, D: null }))
        );
    }

    // Use the explicit clue numbers from CROSSWORD_DATA.
    // Do not generate numbers from grid position, because the clue
    // numbers are part of the puzzle itself.
    const numMap = {};

    Object.keys(CROSSWORD_DATA.clues).forEach(dir => {
        CROSSWORD_DATA.clues[dir].forEach(clue => {
            numMap[clue.row + "_" + clue.col] = clue.num;
        });
    });

    // Assign word indices to cells.
    const clues = CROSSWORD_DATA.clues;

    clues.across.forEach((clue, idx) => {
        const r = clue.row;
        const c = clue.col;

        for (let i = 0; i < clue.length; i++) {
            if (
                r >= 0 && r < rows &&
                c + i >= 0 && c + i < cols &&
                grid[r][c + i] !== null
            ) {
                xwordCellWords[r][c + i].A = idx;
            }
        }
    });

    clues.down.forEach((clue, idx) => {
        const r = clue.row;
        const c = clue.col;

        for (let i = 0; i < clue.length; i++) {
            if (
                r + i >= 0 && r + i < rows &&
                c >= 0 && c < cols &&
                grid[r + i][c] !== null
            ) {
                xwordCellWords[r + i][c].D = idx;
            }
        }
    });

    // Render grid.
    const gridEl = document.getElementById("xwordGrid");
    gridEl.style.gridTemplateColumns = "repeat(" + cols + ", 30px)";
    gridEl.style.gridTemplateRows = "repeat(" + rows + ", 30px)";

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {

            const cellWrap = document.createElement("div");
            cellWrap.className = "xword-cell";

            if (grid[r][c] === null) {
                cellWrap.classList.add("blocked");
                gridEl.appendChild(cellWrap);
                continue;
            }

            const key = r + "_" + c;

            if (numMap[key]) {
                const numEl = document.createElement("span");
                numEl.className = "xword-num";
                numEl.textContent = numMap[key];
                cellWrap.appendChild(numEl);
            }

            const input = document.createElement("input");
            input.maxLength = 1;
            input.dataset.row = r;
            input.dataset.col = c;
            input.autocomplete = "off";

            input.addEventListener("focus", () => setActiveCell(r, c));

            input.addEventListener("click", () => {
                const cellInfo = xwordCellWords[r][c];

                if (cellInfo.A !== null && cellInfo.D !== null) {
                    xwordCurrentDir = (xwordCurrentDir === "A") ? "D" : "A";
                } else if (cellInfo.A !== null) {
                    xwordCurrentDir = "A";
                } else if (cellInfo.D !== null) {
                    xwordCurrentDir = "D";
                }

                setActiveCell(r, c);
            });

            input.addEventListener("keydown", (e) => onXwordKeydown(e, r, c));
            input.addEventListener("input", (e) => onXwordInput(e, r, c));

            cellWrap.appendChild(input);
            gridEl.appendChild(cellWrap);
            xwordCellEls[r][c] = input;
        }
    }

    renderClues();
    document.getElementById("checkCrosswordBtn").addEventListener("click", checkCrossword);
}

function renderClues() {
    const acrossCluesEl = document.getElementById("acrossClues");
    const downCluesEl = document.getElementById("downClues");

    acrossCluesEl.innerHTML = "";
    downCluesEl.innerHTML = "";

    CROSSWORD_DATA.clues.across.forEach((clue, idx) => {
        const li = document.createElement("li");
        li.className = "clue-item";
        li.dataset.num = clue.num;
        li.dataset.dir = "A";
        li.dataset.idx = idx;

        li.innerHTML =
            `<span class="clue-num">${clue.num}.</span> ` +
            `${clue.clue} ` +
            `<span class="clue-len">(${clue.length})</span>`;

        li.addEventListener("click", () => jumpToClue("A", idx));
        acrossCluesEl.appendChild(li);
    });

    CROSSWORD_DATA.clues.down.forEach((clue, idx) => {
        const li = document.createElement("li");
        li.className = "clue-item";
        li.dataset.num = clue.num;
        li.dataset.dir = "D";
        li.dataset.idx = idx;

        li.innerHTML =
            `<span class="clue-num">${clue.num}.</span> ` +
            `${clue.clue} ` +
            `<span class="clue-len">(${clue.length})</span>`;

        li.addEventListener("click", () => jumpToClue("D", idx));
        downCluesEl.appendChild(li);
    });
}

function jumpToClue(dir, idx) {
    const clue = CROSSWORD_DATA.clues[dir === "A" ? "across" : "down"][idx];

    xwordCurrentDir = dir;

    const el = xwordCellEls[clue.row][clue.col];

    if (el) el.focus();

    setActiveCell(clue.row, clue.col);
}

function clearActiveHighlight() {
    document.querySelectorAll(".xword-cell input.active-word")
        .forEach(el => el.classList.remove("active-word"));

    document.querySelectorAll(".clue-item.active-clue")
        .forEach(el => el.classList.remove("active-clue"));
}

function setActiveCell(r, c) {
    if (xwordSolved) return;

    clearActiveHighlight();

    const cellInfo = xwordCellWords[r][c];

    let dir = xwordCurrentDir;

    if (cellInfo[dir] === null) {
        dir = (dir === "A") ? "D" : "A";

        if (cellInfo[dir] !== null) {
            xwordCurrentDir = dir;
        }
    }

    const wordIdx = cellInfo[xwordCurrentDir];

    if (wordIdx === null) return;

    const clue =
        CROSSWORD_DATA.clues[
            xwordCurrentDir === "A" ? "across" : "down"
        ][wordIdx];

    // Highlight exactly clue.length cells.
    for (let k = 0; k < clue.length; k++) {
        const rr = xwordCurrentDir === "A" ? clue.row : clue.row + k;
        const cc = xwordCurrentDir === "A" ? clue.col + k : clue.col;

        if (xwordCellEls[rr] && xwordCellEls[rr][cc]) {
            xwordCellEls[rr][cc].classList.add("active-word");
        }
    }

    const clueEl = document.querySelector(
        '.clue-item[data-num="' +
        clue.num +
        '"][data-dir="' +
        xwordCurrentDir +
        '"]'
    );

    if (clueEl) clueEl.classList.add("active-clue");
}

function moveFocus(r, c, dir, step) {
    let rr = r;
    let cc = c;

    while (true) {
        rr += (dir === "D") ? step : 0;
        cc += (dir === "A") ? step : 0;

        if (
            rr < 0 ||
            rr >= CROSSWORD_DATA.rows ||
            cc < 0 ||
            cc >= CROSSWORD_DATA.cols
        ) {
            return;
        }

        if (xwordCellEls[rr][cc]) {
            xwordCellEls[rr][cc].focus();
            return;
        }

        return;
    }
}

function onXwordInput(e, r, c) {
    const val = e.target.value.toUpperCase().replace(/[^A-Z]/g, "");

    e.target.value = val.slice(-1);
    e.target.classList.remove("correct", "wrong");

    if (val) {
        moveFocus(r, c, xwordCurrentDir, 1);
    }
}

function onXwordKeydown(e, r, c) {
    if (xwordSolved) return;

    if (e.key === "Backspace") {
        if (!e.target.value) {
            e.preventDefault();
            moveFocus(r, c, xwordCurrentDir, -1);
        }
        return;
    }

    if (e.key === "ArrowRight") {
        e.preventDefault();
        xwordCurrentDir = "A";
        moveFocus(r, c, "A", 1);
        return;
    }

    if (e.key === "ArrowLeft") {
        e.preventDefault();
        xwordCurrentDir = "A";
        moveFocus(r, c, "A", -1);
        return;
    }

    if (e.key === "ArrowDown") {
        e.preventDefault();
        xwordCurrentDir = "D";
        moveFocus(r, c, "D", 1);
        return;
    }

    if (e.key === "ArrowUp") {
        e.preventDefault();
        xwordCurrentDir = "D";
        moveFocus(r, c, "D", -1);
        return;
    }
}

function checkCrossword() {
    const grid = CROSSWORD_DATA.grid;

    let allFilled = true;
    let allCorrect = true;

    for (let r = 0; r < CROSSWORD_DATA.rows; r++) {
        for (let c = 0; c < CROSSWORD_DATA.cols; c++) {

            if (grid[r][c] === null) continue;

            const el = xwordCellEls[r][c];
            const val = el.value.toUpperCase();

            if (!val) {
                allFilled = false;
                continue;
            }

            if (val === grid[r][c]) {
                el.classList.add("correct");
                el.classList.remove("wrong");
            } else {
                allCorrect = false;
                el.classList.remove("correct");
                el.classList.add("wrong");
            }
        }
    }

    const feedbackEl = document.getElementById("xwordFeedback");

    if (!allFilled) {
        feedbackEl.innerHTML =
            '<span style="color:#e57373;">Fill in every cell first.</span>';
        return;
    }

    if (!allCorrect) {
        feedbackEl.innerHTML =
            '<span style="color:#e57373;">Some letters are off — green is correct, red is wrong.</span>';
        return;
    }

    xwordSolved = true;

    feedbackEl.innerHTML =
        '<span style="color:#81c784;">FLAWLESS! Puzzle II solved.</span>';

    if (window.confetti) {
        confetti({
            particleCount: 200,
            spread: 100,
            origin: { y: 0.5 },
            colors: ["#d8b878", "#f0e4cf", "#6d8a5b", "#c4a04a"]
        });
    }

    setTimeout(() => {
        document.getElementById("foundersBox").classList.add("show");
        setTimeout(resizeFrame, 50);

        document.getElementById("foundersBox").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }, 1000);

    window.parent.postMessage(
        { type: "STREAMLIT_CROSSWORD_PASSED" },
        "*"
    );
}

/* ============= Lightbox for founder photos ============= */

const lighboxPhotos = {{
    maanal: [
        "https://via.placeholder.com/180x200?text=Maanal+1",
        "https://via.placeholder.com/180x200?text=Maanal+2",
        "https://via.placeholder.com/180x200?text=Maanal+3"
    ],
    aman: [
        "https://via.placeholder.com/180x200?text=Aman+1",
        "https://via.placeholder.com/180x200?text=Aman+2",
        "https://via.placeholder.com/180x200?text=Aman+3"
    ],
    trinav: [
        "https://via.placeholder.com/180x200?text=Trinav+1",
        "https://via.placeholder.com/180x200?text=Trinav+2",
        "https://via.placeholder.com/180x200?text=Trinav+3"
    ]
}};

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
    // Placeholder for Puzzle III
    alert("Puzzle III coming soon!");
}});

</script>

</body>
</html>
"""

render_html_frame(wordle_html, height=820, scrolling=True)
