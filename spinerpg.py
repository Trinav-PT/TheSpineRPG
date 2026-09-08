import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="RPG Treasure Hunt Quest", page_icon="📜", layout="centered")

# --- CUSTOM RPG STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1815;
        color: #e0d5c1;
        font-family: 'Georgia', serif;
    }
    .stButton>button {
        background-color: #4a3b2c;
        color: #f3e5ab;
        border: 2px solid #8b5a2b;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #8b5a2b;
        color: #ffffff;
    }
    .scroll-box {
        background-color: #2b261f;
        border: 3px double #c5a059;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(197, 160, 89, 0.2);
        margin-bottom: 20px;
    }
    .wordle-correct { background-color: #2e7d32; color: white; padding: 10px; font-weight: bold; border-radius: 5px; text-align: center; }
    .wordle-present { background-color: #f9a825; color: white; padding: 10px; font-weight: bold; border-radius: 5px; text-align: center; }
    .wordle-absent { background-color: #424242; color: white; padding: 10px; font-weight: bold; border-radius: 5px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'stage' not in st.session_state:
    st.session_state.stage = 1
if 'wordle_guesses' not in st.session_state:
    st.session_state.wordle_guesses = []
if 'piano_sequence' not in st.session_state:
    st.session_state.piano_sequence = []
if 'piano_start_time' not in st.session_state:
    st.session_state.piano_start_time = None

# --- HEADER ---
st.title("🗡️ Quest of the Ancient Scrolls 🛡️")
st.markdown("---")

# ==========================================
# PUZZLE 1: WORDLE
# ==========================================
if st.session_state.stage == 1:
    st.markdown("<div class='scroll-box'><h3>📜 Scroll I: The Sealed Word</h3><p>Guess the 5-letter ancient password to break the first spell. You have <b>3 attempts</b>!</p></div>", unsafe_allow_html=True)
    
    target_word = "SPINE"
    max_turns = 3
    
    col1, col2 = st.columns([3, 1])
    with col1:
        guess = st.text_input("Enter 5-letter word:", max_chars=5, key="wordle_input").upper()
    with col2:
        st.write("")
        st.write("")
        submit_guess = st.button("Cast Spell")

    if submit_guess and guess:
        if len(guess) != 5:
            st.warning("The spell requires exactly 5 letters!")
        elif len(st.session_state.wordle_guesses) < max_turns:
            st.session_state.wordle_guesses.append(guess)

    # Display Guesses
    for g in st.session_state.wordle_guesses:
        cols = st.columns(5)
        for i in range(5):
            char = g[i]
            if char == target_word[i]:
                cols[i].markdown(f"<div class='wordle-correct'>{char}</div>", unsafe_allow_html=True)
            elif char in target_word:
                cols[i].markdown(f"<div class='wordle-present'>{char}</div>", unsafe_allow_html=True)
            else:
                cols[i].markdown(f"<div class='wordle-absent'>{char}</div>", unsafe_allow_html=True)
        st.write("")

    if len(st.session_state.wordle_guesses) > 0 and st.session_state.wordle_guesses[-1] == target_word:
        st.success("🎉 Correct! Scroll I unseals: *'Knowledge is the backbone of power.'*")
        if st.button("Proceed to Next Puzzle ➡️"):
            st.session_state.stage = 2
            st.rerun()
    elif len(st.session_state.wordle_guesses) >= max_turns:
        st.error("The magic failed! You ran out of turns.")
        if st.button("Retry Scroll I"):
            st.session_state.wordle_guesses = []
            st.rerun()

# ==========================================
# PUZZLE 2: CROSSWORD
# ==========================================
elif st.session_state.stage == 2:
    st.markdown("<div class='scroll-box'><h3>📜 Scroll II: The Lexicon Grid</h3><p>Fill in the answers to solve the Ancient Crossword grid!</p></div>", unsafe_allow_html=True)
    
    st.markdown("""
    **Clues:**
    1. Written works of artistic value (Across) - *10 letters*
    2. Written work bound together (Across) - *4 letters*
    3. Look at and comprehend written text (Down) - *4 letters*
    4. Mark letters or words on paper (Across) - *5 letters*
    5. Tool used for writing/drawing (Down) - *6 letters*
    6. Taxonomic rank below Kingdom (Across) - *6 letters*
    7. Vertebrates belong to this phylum (Across) - *8 letters*
    """)

    c1, c2 = st.columns(2)
    with c1:
        ans1 = st.text_input("1. Across:", key="cw1").strip().capitalize()
        ans2 = st.text_input("2. Across:", key="cw2").strip().capitalize()
        ans3 = st.text_input("3. Down:", key="cw3").strip().capitalize()
        ans4 = st.text_input("4. Across:", key="cw4").strip().capitalize()
    with c2:
        ans5 = st.text_input("5. Down:", key="cw5").strip().capitalize()
        ans6 = st.text_input("6. Across:", key="cw6").strip().capitalize()
        ans7 = st.text_input("7. Across:", key="cw7").strip().capitalize()

    if st.button("Unlock Scroll II"):
        if (ans1 == "Literature" and ans2 == "Book" and ans3 == "Read" and 
            ans4 == "Write" and ans5 == "Pencil" and ans6 == "Phylum" and ans7 == "Chordata"):
            st.success("🎉 Brilliant! Scroll II unseals: *'Words are keys to ancient mysteries.'*")
            st.session_state.cw_passed = True
        else:
            st.error("Some answers are incorrect. Check your spelling and try again!")

    if st.session_state.get('cw_passed', False):
        if st.button("Proceed to Final Puzzle ➡️"):
            st.session_state.stage = 3
            st.rerun()

# ==========================================
# PUZZLE 3: MUSIC PIANO CHALLENGE
# ==========================================
elif st.session_state.stage == 3:
    st.markdown("<div class='scroll-box'><h3>📜 Scroll III: The Bard's Melody</h3><p>Play the target melody below on the piano keys. Hit <b>no wrong notes</b> and finish within <b>30 seconds</b>!</p></div>", unsafe_allow_html=True)

    melody = [
        "3rdG#", "3rdA", "4thC#", "3rdC#", "3rdE", "3rdD#", "3rdC#", "3rdC",
        "2ndG#", "2ndA", "2ndA#", "2ndB", "3rdC", "3rdC#", "3rdE", "3rdF"
    ]
    
    time_limit = 30 # seconds

    st.subheader("Target Melody:")
    st.code(" ➔ ".join(melody))

    if st.session_state.piano_start_time is None:
        if st.button("🎹 Start Timer & Play"):
            st.session_state.piano_start_time = time.time()
            st.session_state.piano_sequence = []
            st.rerun()
    else:
        elapsed = int(time.time() - st.session_state.piano_start_time)
        remaining = time_limit - elapsed

        if remaining <= 0:
            st.error("⏰ Time's up! The melody dissolved into silence.")
            if st.button("Retry Melody"):
                st.session_state.piano_start_time = None
                st.session_state.piano_sequence = []
                st.rerun()
        else:
            st.warning(f"⏳ Time Remaining: **{remaining} seconds**")

            # Display progress
            st.write("**Notes played so far:**")
            st.info(" ➔ ".join(st.session_state.piano_sequence) if st.session_state.piano_sequence else "Click keys below to play...")

            # Piano Keyboard UI setup
            notes_lower = ["2ndG#", "2ndA", "2ndA#", "2ndB"]
            notes_high = ["3rdC", "3rdC#", "3rdD#", "3rdE", "3rdF", "3rdG#", "3rdA", "4thC#"]

            st.write("---")
            st.write("**Lower Octave (l):**")
            cols_l = st.columns(len(notes_lower))
            for idx, note in enumerate(notes_lower):
                if cols_l[idx].button(f"🎹 {note}", key=f"btn_l_{note}"):
                    st.session_state.piano_sequence.append(note)
                    st.rerun()

            st.write("**Higher Octave (h):**")
            cols_h = st.columns(len(notes_high))
            for idx, note in enumerate(notes_high):
                if cols_h[idx].button(f"🎹 {note}", key=f"btn_h_{note}"):
                    st.session_state.piano_sequence.append(note)
                    st.rerun()

            # Check sequence validation
            current_len = len(st.session_state.piano_sequence)
            if current_len > 0:
                # Check if current input matches the target melody prefix
                if st.session_state.piano_sequence != melody[:current_len]:
                    st.error("❌ Wrong note hit! The piano resets!")
                    st.session_state.piano_sequence = []
                    st.rerun()

                # Check for victory
                if st.session_state.piano_sequence == melody:
                    st.success("🎉 Flawless Performance! Scroll III has unsealed!")
                    if st.button("Claim Your Acceptance Letter 🏆"):
                        st.session_state.stage = 4
                        st.rerun()

# ==========================================
# FINAL REWARD: ACCEPTANCE LETTER
# ==========================================
elif st.session_state.stage == 4:
    st.balloons()
    st.markdown("<div class='scroll-box' style='text-align: center; border-color: #ffd700;'><h2>✨ THE GRAND ACCEPTANCE LETTER ✨</h2><p>You have proven your intellect, wisdom, and musical harmony!</p></div>", unsafe_allow_html=True)
    
    player_name = st.text_input("Enter your name for the Scroll of Honor:", "Brave Adventurer")
    
    letter_content = f"""
    =======================================================
               HEROIC ACADEMY ACCEPTANCE LETTER            
    =======================================================
    
    Be it known to all realm inhabitants that:
    
                       {player_name.upper()}
    
    Has successfully conquered the Wordle Spell, solved the 
    Ancient Lexicon Crossword, and harmonized the Bard's Piano.
    
    You are officially ACCEPTED into the High Order of 
    Master Adventurers with full honors!
    
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
    
    if st.button("🔄 Restart Quest"):
        st.session_state.stage = 1
        st.session_state.wordle_guesses = []
        st.session_state.piano_sequence = []
        st.session_state.piano_start_time = None
        st.session_state.cw_passed = False
        st.rerun()
