import base64
import json
from pathlib import Path

import streamlit as st

def render_html_frame(html_string, height, scrolling=False):
    """Render raw HTML in an iframe, using the new st.iframe API when
    available and falling back to components.html on older Streamlit
    versions."""
    try:
        st.iframe(html_string, height=height)
    except AttributeError:
        import streamlit.components.v1 as components
        components.html(html_string, height=height, scrolling=scrolling)


def get_qr_html():
    """Return an <img> tag for a real Instagram QR code if available,
    otherwise fall back to a placeholder visual."""
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


def build_new_crossword_grid():
    rows, cols = 13, 10
    grid = [[None] * cols for _ in range(rows)]
    
    white_cells = {
        # Col 0: READINGCIRCLE
        (0, 0): 'R', (1, 0): 'E', (2, 0): 'A', (3, 0): 'D',
        (4, 0): 'I', (5, 0): 'N', (6, 0): 'G', (7, 0): 'C',
        (8, 0): 'I', (9, 0): 'R', (10, 0): 'C', (11, 0): 'L', (12, 0): 'E',
        
        # Intermediate sparse letters
        (0, 2): 'P', (7, 2): 'C',
        (0, 3): 'H', (7, 3): 'H',
        (0, 4): 'Y', (7, 4): 'O',
        (0, 5): 'L', (7, 5): 'R',
        (0, 6): 'U', (7, 6): 'D',
        
        # Col 7: MURDERBALLAD
        (0, 7): 'M', (1, 7): 'U', (2, 7): 'R', (3, 7): 'D',
        (4, 7): 'E', (5, 7): 'R', (6, 7): 'B', (7, 7): 'A',
        (8, 7): 'L', (9, 7): 'L', (10, 7): 'A', (11, 7): 'D',
        
        # Col 8: HOGWARTS
        (1, 8): 'H', (2, 8): 'O', (3, 8): 'G', (4, 8): 'W',
        (5, 8): 'A', (6, 8): 'R', (7, 8): 'T', (8, 8): 'S',
        
        # Col 9: BONEYARD
        (2, 9): 'B', (3, 9): 'O', (4, 9): 'N', (5, 9): 'E',
        (6, 9): 'Y', (7, 9): 'A', (8, 9): 'R', (9, 9): 'D',
        
        # Row 9: READERS
        (9, 1): 'E', (9, 2): 'A', (9, 3): 'D', (9, 4): 'E', (9, 5): 'R', (9, 6): 'S',
        
        # Row 10: CRANIUM
        (10, 1): 'R', (10, 2): 'A', (10, 3): 'N', (10, 4): 'I', (10, 5): 'U', (10, 6): 'M',
    }
    
    for (r, c), letter in white_cells.items():
        grid[r][c] = letter
        
    return grid


CROSSWORD_GRID = build_new_crossword_grid()

CROSSWORD_CLUES = {
    "across": [
        {"num": 2, "clue": "This and the next clue are 2 words, part of 1 big phrase. For this word: a group into which animals, plants, etc. are divided.", "length": 6, "row": 0, "col": 2},
        {"num": 6, "clue": "This word is the answer to the phylum clue above — the third-largest phylum in the animal kingdom.", "length": 8, "row": 7, "col": 2},
        {"num": 7, "clue": "Most people in this club are ________.", "length": 7, "row": 9, "col": 0},
        {"num": 8, "clue": "A bony enclosure around the brain of a vertebrate.", "length": 7, "row": 10, "col": 0},
    ],
    "down": [
        {"num": 1, "clue": "We get together, sometimes weekly, to read. What do we call this (mini) event?", "length": "7,6", "row": 0, "col": 0},
        {"num": 3, "clue": "The Spine's flagship event, held every year for Fitoor.", "length": "6,6", "row": 0, "col": 7},
        {"num": 4, "clue": "We brought this boarding school to Plaksha in one of our earlier events.", "length": 8, "row": 1, "col": 8},
        {"num": 5, "clue": "The Spine's very own magazine is called __________.", "length": 8, "row": 2, "col": 9},
    ]
}

CROSSWORD_JSON = json.dumps({
    "grid": CROSSWORD_GRID,
    "rows": 13,
    "cols": 10,
    "clues": CROSSWORD_CLUES
})

QR_IMAGE_HTML = get_qr_html()

st.set_page_config(page_title="SPINE Chronicles", layout="wide")

WORDLE_ANSWER = "SPINE"

wordle_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #211d17; color: #f0e4cf; font-family: Georgia, serif; }}
#app {{ padding: 10px 10px 24px; outline: none; display: flex; flex-direction: column; align-items: center; }}
#status {{ background: #362f24; border: 1px solid #d8b878; border-radius: 7px; padding: 10px 14px; margin-bottom: 18px; text-align: center; width: 100%; max-width: 520px; }}
#feedback {{ margin-top: 6px; min-height: 20px; font-weight: bold; }}
.success {{ color: #81c784; }}
.error {{ color: #e57373; }}
#grid {{ display: grid; grid-template-rows: repeat(6, 1fr); gap: 8px; margin-bottom: 22px; }}
.grid-row {{ display: grid; grid-template-columns: repeat(5, 54px); gap: 8px; }}
.tile {{ width: 54px; height: 54px; border: 2px solid #a8875a; border-radius: 6px; background: #2b261d; display: flex; align-items: center; justify-content: center; font-size: 26px; font-weight: bold; text-transform: uppercase; color: #f0e4cf; transition: transform .15s, background .2s, border-color .2s; }}
.tile.filled {{ border-color: #d8b878; }}
.tile.correct {{ background: #6d8a5b; border-color: #6d8a5b; color: #fff; }}
.tile.present {{ background: #c4a04a; border-color: #c4a04a; color: #2b2216; }}
.tile.absent {{ background: #4a4132; border-color: #4a4132; color: #d9cdb4; }}
#keyboard {{ display: flex; flex-direction: column; gap: 8px; align-items: center; }}
.kb-row {{ display: flex; gap: 6px; }}
.kb-key {{ min-width: 36px; height: 46px; padding: 0 8px; border: none; border-radius: 5px; background: #4a4132; color: #f0e4cf; font-family: Georgia, serif; font-weight: bold; font-size: 14px; display: flex; align-items: center; justify-content: center; cursor: pointer; user-select: none; text-transform: uppercase; }}
.kb-key.wide {{ min-width: 60px; font-size: 11px; }}
.kb-key.correct {{ background: #6d8a5b; color: #fff; }}
.kb-key.present {{ background: #c4a04a; color: #2b2216; }}
.kb-key.absent {{ background: #2b271f; color: #857b64; }}
#unlockBox, #qrBox, #crosswordBox, #foundersBox {{ margin-top: 22px; padding: 22px; background: #3c2a1c; border: 2px solid #d8b878; border-radius: 10px; text-align: center; width: 100%; max-width: 620px; display: none; }}
#unlockBox.show, #qrBox.show, #crosswordBox.show, #foundersBox.show {{ display: block; }}
.cta-button {{ margin-top: 18px; padding: 12px 26px; border: none; border-radius: 6px; background: #d8b878; color: #221d17; font-family: Georgia, serif; font-weight: bold; font-size: 15px; cursor: pointer; }}
.cta-button:hover {{ background: #ffe9a8; }}
.xword-layout {{ display: flex; flex-wrap: wrap; gap: 26px; justify-content: center; align-items: flex-start; text-align: left; }}
.xword-grid {{ display: grid; gap: 2px; background: #221d17; padding: 6px; border-radius: 6px; grid-template-columns: repeat(10, 30px); }}
.xword-cell {{ position: relative; width: 30px; height: 30px; }}
.xword-cell input {{ width: 100%; height: 100%; border: 1px solid #a8875a; background: #f0e4cf; color: #221d17; text-align: center; font-family: Georgia, serif; font-weight: bold; font-size: 15px; text-transform: uppercase; padding: 0; outline: none; }}
.xword-cell input.correct {{ background: #6d8a5b; color: #fff; }}
.xword-cell input.wrong {{ background: #8b3a3a; color: #fff; }}
.xword-cell.blocked {{ background: #221d17; }}
.xword-num {{ position: absolute; top: 0; left: 2px; font-size: 8px; color: #221d17; z-index: 2; pointer-events: none; }}
.clue-cols {{ display: flex; gap: 26px; flex-wrap: wrap; max-width: 450px; }}
.clue-col {{ min-width: 200px; }}
.clue-title {{ font-weight: bold; color: #ffe9a8; margin-bottom: 6px; font-size: 14px; letter-spacing: 1px; text-transform: uppercase; }}
.clue-list {{ list-style: none; margin: 0 0 16px 0; padding: 0; }}
.clue-item {{ font-size: 13px; line-height: 1.5; color: #f0e4cf; margin-bottom: 10px; padding: 4px; border-radius: 3px; }}
</style>
</head>
<body>

<div id="app" tabindex="0">
    <div id="status">
        <div id="feedback">Click the board below, then guess the 5-letter word.</div>
    </div>
    <div id="grid"></div>
    <div id="keyboard"></div>

    <div id="unlockBox">
        <div style="font-size:20px; font-weight:bold; color:#ffe9a8; margin-bottom:8px;">PUZZLE I — SOLVED</div>
        <div style="font-size:16px; line-height:1.8;">
            <p>Welcome to Spine. Just like the spine of a novel binds the pages together, we hold together the literature culture in Plaksha.</p>
        </div>
        <button class="cta-button" id="toPuzzle2Btn">Take me to puzzle 2</button>
    </div>

    <div id="qrBox">
        {QR_IMAGE_HTML}
        <div style="margin-top:14px; font-size:15px; line-height:1.7;">
            Here's the link to our Instagram. Follow to stay updated.
        </div>
        <button class="cta-button" id="toCrosswordBtn">Continue to Puzzle II</button>
    </div>

    <div id="crosswordBox">
        <div style="font-size:20px; font-weight:bold; color:#ffe9a8; margin-bottom:14px;">Puzzle II: The Crossword</div>
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
</div>

<script>
const CROSSWORD_DATA = {CROSSWORD_JSON};
const ANSWER = "{WORDLE_ANSWER}".toUpperCase();
const WORD_LEN = ANSWER.length;
const MAX_TRIES = 6;

let currentGuess = "";
let guesses = [];
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
            if (k === "ENTER" || k === "BACK") btn.classList.add("wide");
            btn.addEventListener("click", () => handleKey(k));
            rowEl.appendChild(btn);
            if (k !== "ENTER" && k !== "BACK") kbKeyEls[k] = btn;
        }});
        keyboardEl.appendChild(rowEl);
    }});
}}

function handleKey(key) {{
    if (locked) return;
    if (key === "ENTER") {{
        submitGuess();
    }} else if (key === "BACK" || key === "BACKSPACE") {{
        currentGuess = currentGuess.slice(0, -1);
        renderCurrentGuess();
    }} else if (/^[A-Z]$/.test(key) && currentGuess.length < WORD_LEN) {{
        currentGuess += key;
        renderCurrentGuess();
    }}
}}

function renderCurrentGuess() {{
    const rowIdx = guesses.length;
    if (rowIdx >= MAX_TRIES) return;
    const tiles = rows[rowIdx];
    for (let i = 0; i < WORD_LEN; i++) {{
        const letter = currentGuess[i] || "";
        tiles[i].textContent = letter;
        tiles[i].classList.toggle("filled", !!letter);
    }}
}}

function submitGuess() {{
    if (locked || currentGuess.length !== WORD_LEN) return;
    const rowIdx = guesses.length;
    const tiles = rows[rowIdx];
    const answerArr = ANSWER.split("");
    const guessArr = currentGuess.split("");

    guessArr.forEach((char, i) => {{
        if (char === answerArr[i]) {{
            tiles[i].classList.add("correct");
        }} else if (answerArr.includes(char)) {{
            tiles[i].classList.add("present");
        }} else {{
            tiles[i].classList.add("absent");
        }}
    }});

    guesses.push(currentGuess);
    if (currentGuess === ANSWER) {{
        locked = true;
        feedbackEl.innerHTML = '<span class="success">FLAWLESS!</span>';
        unlockBox.classList.add("show");
        if (window.confetti) confetti({{ particleCount: 100, spread: 70, origin: {{ y: 0.6 }} }});
    }} else if (guesses.length >= MAX_TRIES) {{
        locked = true;
        feedbackEl.innerHTML = '<span class="error">Game over! Word was ' + ANSWER + '</span>';
    }}
    currentGuess = "";
}}

document.addEventListener("keydown", (e) => {{
    handleKey(e.key.toUpperCase());
}});

document.getElementById("toPuzzle2Btn").addEventListener("click", () => {{
    unlockBox.classList.remove("show");
    document.getElementById("qrBox").classList.add("show");
}});

document.getElementById("toCrosswordBtn").addEventListener("click", () => {{
    document.getElementById("qrBox").classList.remove("show");
    document.getElementById("crosswordBox").classList.add("show");
    buildCrossword();
}});

function buildCrossword() {{
    const gridContainer = document.getElementById("xwordGrid");
    gridContainer.innerHTML = "";
    const gridData = CROSSWORD_DATA.grid;
    
    for (let r = 0; r < CROSSWORD_DATA.rows; r++) {{
        for (let c = 0; c < CROSSWORD_DATA.cols; c++) {{
            const cellDiv = document.createElement("div");
            cellDiv.className = "xword-cell";
            if (gridData[r][c] === null) {{
                cellDiv.classList.add("blocked");
            }} else {{
                const input = document.createElement("input");
                input.maxLength = 1;
                input.dataset.row = r;
                input.dataset.col = c;
                cellDiv.appendChild(input);
            }}
            gridContainer.appendChild(cellDiv);
        }}
    }}

    const populateClues = (clues, elementId) => {{
        const ul = document.getElementById(elementId);
        ul.innerHTML = "";
        clues.forEach(c => {{
            const li = document.createElement("li");
            li.className = "clue-item";
            li.innerHTML = `<span class="clue-num">${{c.num}}.</span> ${{c.clue}} (${{c.length}})`;
            ul.appendChild(li);
        }});
    }};

    populateClues(CROSSWORD_DATA.clues.across, "acrossClues");
    populateClues(CROSSWORD_DATA.clues.down, "downClues");
}}

document.getElementById("checkCrosswordBtn").addEventListener("click", () => {{
    const inputs = document.querySelectorAll(".xword-cell input");
    let allCorrect = true;
    inputs.forEach(input => {{
        const r = input.dataset.row;
        const c = input.dataset.col;
        const val = input.value.toUpperCase();
        const expected = CROSSWORD_DATA.grid[r][c];
        if (val === expected) {{
            input.className = "correct";
        }} else {{
            input.className = "wrong";
            allCorrect = false;
        }}
    }});
    const fb = document.getElementById("xwordFeedback");
    if (allCorrect) {{
        fb.innerHTML = '<span class="success">Crossword solved!</span>';
    }} else {{
        fb.innerHTML = '<span class="error">Some answers are incorrect. Check highlighted red cells.</span>';
    }}
}});

buildGrid();
buildKeyboard();
</script>
</body>
</html>
"""

render_html_frame(wordle_html, height=1000)
