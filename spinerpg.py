import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="RPG Piano Quest", page_icon="🎹", layout="centered")

# --- CUSTOM RPG STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1815;
        color: #e0d5c1;
        font-family: 'Georgia', serif;
    }
    .scroll-box {
        background-color: #2b261f;
        border: 3px double #c5a059;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(197, 160, 89, 0.2);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🗡️ Scroll of the Bard's Piano 🛡️")
st.markdown("---")

# ==========================================
# PIANO GAME COMPONENT WITH WEB AUDIO API
# ==========================================

# Target Melody
melody_sequence = [
    "3rdG#", "3rdA", "4thC#", "3rdC#", "3rdE", "3rdD#", "3rdC#", "3rdC",
    "2ndG#", "2ndA", "2ndA#", "2ndB", "3rdC", "3rdC#", "3rdE", "3rdF"
]

st.markdown("""
    <div class='scroll-box'>
        <h3>📜 Scroll III: The Bard's Melody</h3>
        <p>Play the ancient sequence on your computer keyboard or click the keys below. Hit <b>no wrong notes</b>!</p>
    </div>
""", unsafe_allow_html=True)

st.write("### 🎶 Target Sequence to Play:")
st.code(" ➔ ".join(melody_sequence))

# Custom HTML/JS Web Audio Piano Component
piano_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        background-color: #1a1815;
        color: #e0d5c1;
        font-family: 'Georgia', serif;
        margin: 0;
        padding: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .status-box {
        background-color: #2b261f;
        border: 1px solid #c5a059;
        border-radius: 6px;
        padding: 10px;
        width: 90%;
        margin-bottom: 15px;
        font-size: 14px;
        text-align: center;
    }
    .piano-container {
        display: flex;
        position: relative;
        background: #000;
        padding: 10px 10px 0 10px;
        border-radius: 8px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.8);
        user-select: none;
    }
    .key {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: center;
        border-radius: 0 0 5px 5px;
        cursor: pointer;
        font-size: 11px;
        font-weight: bold;
        padding-bottom: 8px;
        box-sizing: border-box;
    }
    .white {
        width: 42px;
        height: 180px;
        background: linear-gradient(to bottom, #eeeeee 0%, #ffffff 100%);
        color: #333;
        border: 1px solid #000;
        z-index: 1;
    }
    .white:active, .white.active {
        background: #d3d3d3;
    }
    .black {
        width: 28px;
        height: 110px;
        background: linear-gradient(to bottom, #333333 0%, #000000 100%);
        color: #f3e5ab;
        border: 1px solid #000;
        margin-left: -14px;
        margin-right: -14px;
        z-index: 2;
    }
    .black:active, .black.active {
        background: #555555;
    }
    .key-cap {
        background: #8b5a2b;
        color: #fff;
        padding: 2px 4px;
        border-radius: 3px;
        margin-top: 4px;
        font-size: 10px;
    }
    .msg-success { color: #81c784; font-weight: bold; }
    .msg-error { color: #e57373; font-weight: bold; }
</style>
</head>
<body>

<div class="status-box" id="statusBox">
    <div><b>Notes Played:</b> <span id="playedNotes" style="color:#f3e5ab;">None</span></div>
    <div id="feedbackMsg" style="margin-top: 5px;">Click a key or press keyboard shortcuts to start!</div>
</div>

<div class="piano-container" id="keyboard">
    <!-- Keys mapped across 2 octaves -->
    <div class="key black" data-note="2ndG#" data-freq="207.65" data-key="a"><span class="key-note">2ndG#</span><span class="key-cap">A</span></div>
    <div class="key white" data-note="2ndA" data-freq="220.00" data-key="w"><span class="key-note">2ndA</span><span class="key-cap">W</span></div>
    <div class="key black" data-note="2ndA#" data-freq="233.08" data-key="s"><span class="key-note">2ndA#</span><span class="key-cap">S</span></div>
    <div class="key white" data-note="2ndB" data-freq="246.94" data-key="e"><span class="key-note">2ndB</span><span class="key-cap">E</span></div>
    <div class="key white" data-note="3rdC" data-freq="261.63" data-key="d"><span class="key-note">3rdC</span><span class="key-cap">D</span></div>
    <div class="key black" data-note="3rdC#" data-freq="277.18" data-key="f"><span class="key-note">3rdC#</span><span class="key-cap">F</span></div>
    <div class="key white" data-note="3rdD#" data-freq="311.13" data-key="t"><span class="key-note">3rdD#</span><span class="key-cap">T</span></div>
    <div class="key white" data-note="3rdE" data-freq="329.63" data-key="g"><span class="key-note">3rdE</span><span class="key-cap">G</span></div>
    <div class="key white" data-note="3rdF" data-freq="349.23" data-key="y"><span class="key-note">3rdF</span><span class="key-cap">Y</span></div>
    <div class="key black" data-note="3rdG#" data-freq="415.30" data-key="h"><span class="key-note">3rdG#</span><span class="key-cap">H</span></div>
    <div class="key white" data-note="3rdA" data-freq="440.00" data-key="u"><span class="key-note">3rdA</span><span class="key-cap">U</span></div>
    <div class="key black" data-note="4thC#" data-freq="554.37" data-key="j"><span class="key-note">4thC#</span><span class="key-cap">J</span></div>
</div>

<script>
    const melody = [
        "3rdG#", "3rdA", "4thC#", "3rdC#", "3rdE", "3rdD#", "3rdC#", "3rdC",
        "2ndG#", "2ndA", "2ndA#", "2ndB", "3rdC", "3rdC#", "3rdE", "3rdF"
    ];

    let playedSequence = [];
    let audioCtx = null;

    function initAudio() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    function playTone(freq) {
        initAudio();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.6);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start();
        osc.stop(audioCtx.currentTime + 0.6);
    }

    function handleNotePlay(note, freq, keyElem) {
        playTone(freq);
        
        // Visual key press animation
        keyElem.classList.add('active');
        setTimeout(() => keyElem.classList.remove('active'), 200);

        // Check Sequence
        playedSequence.push(note);
        document.getElementById('playedNotes').innerText = playedSequence.join(" ➔ ");

        const currentIndex = playedSequence.length - 1;

        if (playedSequence[currentIndex] !== melody[currentIndex]) {
            document.getElementById('feedbackMsg').innerHTML = "<span class='msg-error'>❌ WRONG NOTE! Resetting sequence...</span>";
            playedSequence = [];
            setTimeout(() => {
                document.getElementById('playedNotes').innerText = "None";
            }, 1000);
        } else if (playedSequence.length === melody.length) {
            document.getElementById('feedbackMsg').innerHTML = "<span class='msg-success'>🎉 FLAWLESS! You unlocked the scroll!</span>";
            window.parent.postMessage({type: 'STREAMLIT_PIANO_PASSED'}, '*');
        } else {
            document.getElementById('feedbackMsg').innerText = "Keep going...";
        }
    }

    // Attach click events
    const keys = document.querySelectorAll('.key');
    const keyMap = {};

    keys.forEach(k => {
        const note = k.getAttribute('data-note');
        const freq = parseFloat(k.getAttribute('data-freq'));
        const keyChar = k.getAttribute('data-key');
        
        keyMap[keyChar] = { note, freq, elem: k };

        k.addEventListener('click', () => {
            handleNotePlay(note, freq, k);
        });
    });

    // Attach Physical Keyboard events
    window.addEventListener('keydown', (e) => {
        const char = e.key.toLowerCase();
        if (keyMap[char]) {
            handleNotePlay(keyMap[char].note, keyMap[char].freq, keyMap[char].elem);
        }
    });
</script>
</body>
</html>
"""

# Embed JS component into Streamlit app
components.html(piano_html, height=360)

# ==========================================
# FINAL REWARD: ACCEPTANCE LETTER
# ==========================================
if 'piano_completed' not in st.session_state:
    st.session_state.piano_completed = False

st.write("---")
# Toggle completion checkbox or manual progression option
unlock_scroll = st.checkbox("Check here once you win the piano challenge to reveal letter:")

if unlock_scroll:
    st.balloons()
    st.markdown("""
        <div class='scroll-box' style='text-align: center; border-color: #ffd700;'>
            <h2>✨ THE GRAND ACCEPTANCE LETTER ✨</h2>
            <p>You have mastered the Bard's Piano and harmonized the ancient notes!</p>
        </div>
    """, unsafe_allow_html=True)
    
    player_name = st.text_input("Enter your name for the Scroll of Honor:", "Brave Bard")
    
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
    
    st.code(letter_content, language=None)
    
    st.download_button(
        label="📜 Download Acceptance Letter",
        data=letter_content,
        file_name=f"Acceptance_Letter_{player_name.replace(' ', '_')}.txt",
        mime="text/plain"
    )
