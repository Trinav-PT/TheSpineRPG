import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="RPG Piano Quest",
    page_icon="🎹",
    layout="wide"
)

# ============================================================
# STYLING
# ============================================================
st.markdown("""
<style>
.stApp {
    background: #1a1815;
    color: #e0d5c1;
    font-family: Georgia, serif;
}

.scroll-box {
    background: #2b261f;
    border: 3px double #c5a059;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(197,160,89,.2);
    margin-bottom: 20px;
}

.sequence-box {
    background: #211e1a;
    border: 2px solid #80652e;
    border-radius: 10px;
    padding: 16px;
    margin-top: 18px;
}

.note {
    display: inline-block;
    padding: 7px 10px;
    margin: 3px;
    border-radius: 5px;
    background: #3a3328;
    border: 1px solid #80652e;
    font-family: monospace;
}

.note.current {
    background: #c5a059;
    color: #17130e;
}

.note.done {
    background: #536b45;
    color: white;
}

.note.wrong {
    background: #8b3a3a;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🗡️ Scroll of the Bard's Piano 🛡️")
st.markdown("---")

# ============================================================
# TARGET MELODY
# ============================================================
melody_sequence = [
    "G#2", "A2", "C#4", "C#3",
    "E3", "D#3", "C#3", "C3",
    "G#2", "A2", "A#2", "B2",
    "C3", "C#3", "E3", "F3"
]

st.markdown("""
<div class="scroll-box">
    <h3>📜 Scroll III: The Bard's Melody</h3>
    <p>
        Play the ancient sequence using the <b>letter keys A–Y</b>
        or click the piano keys. The piano covers every note from
        <b>C#2 to C#4</b>.
    </p>
    <p>
        <b>Click anywhere on the piano first</b> to activate the
        computer-keyboard controls.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FULL CHROMATIC RANGE: C#2 -> C#4
# 25 notes, mapped to A-Y (25 letters).
# ============================================================
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

# A-Y gives exactly 25 keyboard letters.
keyboard_letters = list("abcdefghijklmnopqrstuvwxy")

# ============================================================
# BUILD PIANO HTML
# ============================================================
# Use a real piano layout: white keys underneath, black keys
# positioned over the appropriate gaps.
white_notes = {"C", "D", "E", "F", "G", "A", "B"}

piano_keys = []
white_index = 0

for note, freq in notes:
    pitch = note[:-1]
    octave = int(note[-1])
    is_black = "#" in pitch

    if is_black:
        # Position black key over the gap after the preceding white key.
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

# The black-key positioning above needs to account for the fact that
# black keys don't consume white-key positions. Generate clean HTML
# separately so every chromatic note gets the correct letter mapping.
white_counter = 0
key_html = []

for i, (note, freq) in enumerate(notes):
    letter = keyboard_letters[i].upper()
    pitch = note[:-1]
    is_black = "#" in pitch

    if not is_black:
        key_html.append(
            f'<div class="piano-key white-key" data-note="{note}" '
            f'data-freq="{freq}" data-key="{keyboard_letters[i]}" '
            f'style="left:{white_counter * 48}px;">'
            f'<span class="note-label">{note}</span>'
            f'<span class="computer-key">{letter}</span>'
            f'</div>'
        )
        white_counter += 1

# Black keys are placed after the corresponding white key.
# Number of white keys before each black key determines position.
white_counter = 0
black_html = []

for i, (note, freq) in enumerate(notes):
    pitch = note[:-1]
    is_black = "#" in pitch

    if is_black:
        black_left = white_counter * 48 - 14
        letter = keyboard_letters[i].upper()
        black_html.append(
            f'<div class="piano-key black-key" data-note="{note}" '
            f'data-freq="{freq}" data-key="{keyboard_letters[i]}" '
            f'style="left:{black_left}px;">'
            f'<span class="note-label">{note}</span>'
            f'<span class="computer-key">{letter}</span>'
            f'</div>'
        )
    else:
        white_counter += 1

piano_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    * {{
        box-sizing: border-box;
    }}

    html, body {{
        margin: 0;
        padding: 0;
        background: #1a1815;
        color: #e0d5c1;
        font-family: Georgia, serif;
    }}

    body {{
        width: 100%;
        overflow-x: auto;
        outline: none;
    }}

    #app {{
        width: max-content;
        min-width: 100%;
        padding: 8px 10px 20px;
        outline: none;
    }}

    #status {{
        background: #2b261f;
        border: 1px solid #c5a059;
        border-radius: 7px;
        padding: 10px 14px;
        margin-bottom: 14px;
        text-align: center;
        min-width: 1250px;
    }}

    #activation {{
        color: #f3e5ab;
        font-size: 13px;
        margin-top: 4px;
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
</style>
</head>

<body tabindex="0">
<div id="app" tabindex="0">

    <div id="status">
        <div><b>Notes Played:</b> <span id="playedNotes">None</span></div>
        <div id="activation">Click the piano once, then use A–Y on your keyboard.</div>
        <div id="feedback">Ready.</div>
    </div>

    <div class="piano-wrapper" id="pianoWrapper">
        <div class="piano" id="piano">
            {''.join(white_html)}
            {''.join(black_html)}
        </div>
    </div>

    <div id="sequence">
        <div class="sequence-title">🎶 Notes to Play</div>
        <div id="targetSequence"></div>
    </div>

</div>

<script>
const melody = {melody_sequence!r};

const noteElements = {{}};
const keyMap = {{}};

let playedSequence = [];
let audioCtx = null;
let activeOscillators = {{}};

function initAudio() {{
    if (!audioCtx) {{
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }}

    if (audioCtx.state === "suspended") {{
        audioCtx.resume();
    }}
}}

function playTone(freq, id) {{
    initAudio();

    const now = audioCtx.currentTime;

    const oscillator = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    // A simple pleasant synth tone. It is intentionally not a piano
    // sample: it works entirely in the browser without external files.
    oscillator.type = "triangle";
    oscillator.frequency.setValueAtTime(freq, now);

    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.22, now + 0.012);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.75);

    oscillator.connect(gain);
    gain.connect(audioCtx.destination);

    oscillator.start(now);
    oscillator.stop(now + 0.8);

    activeOscillators[id] = oscillator;

    setTimeout(() => {{
        delete activeOscillators[id];
    }}, 850);
}}

function renderTargetSequence() {{
    const container = document.getElementById("targetSequence");
    container.innerHTML = "";

    melody.forEach((note, index) => {{
        const el = document.createElement("span");
        el.className = "seq-note";
        el.id = "seq-" + index;
        el.textContent = note;
        container.appendChild(el);
    }});

    updateTargetHighlight();
}}

function updateTargetHighlight() {{
    melody.forEach((_, i) => {{
        const el = document.getElementById("seq-" + i);
        if (!el) return;

        el.classList.remove("current", "done");

        if (i < playedSequence.length) {{
            el.classList.add("done");
        }} else if (i === playedSequence.length) {{
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
    initAudio();
    flashKey(element);
    playTone(freq, note + Date.now());

    const expected = melody[playedSequence.length];

    if (note === expected) {{
        playedSequence.push(note);
        updatePlayedDisplay();
        updateTargetHighlight();

        if (playedSequence.length === melody.length) {{
            document.getElementById("feedback").innerHTML =
                '<span class="success">🎉 FLAWLESS! You unlocked the scroll!</span>';

            window.parent.postMessage(
                {{type: "STREAMLIT_PIANO_PASSED"}},
                "*"
            );
        }} else {{
            document.getElementById("feedback").textContent =
                "✓ Correct — keep going!";
        }}
    }} else {{
        // Show the wrong note briefly, then completely restart.
        const wrongIndex = playedSequence.length;
        const wrongEl = document.getElementById("seq-" + wrongIndex);

        if (wrongEl) {{
            wrongEl.classList.add("wrong");
        }}

        document.getElementById("feedback").innerHTML =
            '<span class="error">❌ Wrong note! Start the sequence again.</span>';

        playedSequence = [];
        updatePlayedDisplay();

        setTimeout(() => {{
            updateTargetHighlight();
            document.getElementById("feedback").textContent = "Ready.";
        }}, 700);
    }}
}}

function activateKeyboard() {{
    document.body.focus();
    document.getElementById("app").focus();

    document.getElementById("activation").textContent =
        "⌨️ Keyboard active — use A–Y to play the piano.";
}}

document.querySelectorAll(".piano-key").forEach(el => {{
    const note = el.dataset.note;
    const freq = Number(el.dataset.freq);
    const key = el.dataset.key.toLowerCase();

    noteElements[note] = el;
    keyMap[key] = {{
        note: note,
        freq: freq,
        element: el
    }};

    el.addEventListener("mousedown", (event) => {{
        event.preventDefault();
        activateKeyboard();
        handleNotePlay(note, freq, el);
    }});

    // Also support touch screens.
    el.addEventListener("touchstart", (event) => {{
        event.preventDefault();
        activateKeyboard();
        handleNotePlay(note, freq, el);
    }}, {{passive: false}});
}});

// Clicking the piano activates the computer keyboard.
document.getElementById("pianoWrapper").addEventListener("mousedown", () => {{
    activateKeyboard();
}});

document.addEventListener("keydown", (event) => {{
    const key = event.key.toLowerCase();

    if (!keyMap[key]) return;

    // Don't repeat the same note continuously when a key is held down.
    if (event.repeat) return;

    event.preventDefault();

    activateKeyboard();

    const item = keyMap[key];
    handleNotePlay(item.note, item.freq, item.element);
}});

renderTargetSequence();
activateKeyboard();
</script>
</body>
</html>
"""

# ============================================================
# DISPLAY GAME
# ============================================================
components.html(piano_html, height=480, scrolling=True)

# ============================================================
# COMPLETION / ACCEPTANCE LETTER
# ============================================================
st.markdown("---")

if "piano_completed" not in st.session_state:
    st.session_state.piano_completed = False

unlock_scroll = st.checkbox(
    "Check here once you win the piano challenge to reveal the letter:"
)

if unlock_scroll:
    st.balloons()

    st.markdown("""
    <div class="scroll-box" style="text-align:center;border-color:#ffd700;">
        <h2>✨ THE GRAND ACCEPTANCE LETTER ✨</h2>
        <p>You have mastered the Bard's Piano and harmonized the ancient notes!</p>
    </div>
    """, unsafe_allow_html=True)

    player_name = st.text_input(
        "Enter your name for the Scroll of Honor:",
        "Brave Bard"
    )

    letter_content = f"""
=======================================================
           HEROIC ACADEMY ACCEPTANCE LETTER
=======================================================

Be it known to all realm inhabitants that:

                   {player_name.upper()}

Has successfully harmonized the Bard's Piano with complete
flawless perfection.

You are officially ACCEPTED into the High Order of
Master Musicians & Adventurers with full honors!

Given on this day in the RPG Realm.
=======================================================
"""

    st.code(letter_content)

    st.download_button(
        label="📜 Download Acceptance Letter",
        data=letter_content,
        file_name=f"Acceptance_Letter_{player_name.replace(' ', '_')}.txt",
        mime="text/plain"
    )
