import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="RPG Treasure Hunt Quest", page_icon="📜", layout="centered")

# --- CUSTOM RPG, WORDLE & CROSSWORD STYLING ---
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
    /* Wordle Styling */
    .wordle-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 55px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 6px;
        margin: 2px;
        color: white;
        text-transform: uppercase;
    }
    .tile-correct { background-color: #2e7d32; border: 2px solid #1b5e20; }
    .tile-present { background-color: #f9a825; border: 2px solid #f57f17; }
    .tile-absent { background-color: #37474f; border: 2px solid #263238; }
    .tile-empty { background-color: #1a1815; border: 2px solid #4a3b2c; color: #4a3b2c; }

    /* Crossword Grid Styling */
    .cw-cell {
        width: 32px;
        height: 32px;
        border: 1px solid #8b5a2b;
        background-color: #2b261f;
        color: #f3e5ab;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        position: relative;
        display: inline-block;
        line-height: 30px;
        vertical-align: middle;
        margin: 1px;
    }
    .cw-block {
        width: 32px;
        height: 32px;
        background-color: #12100e;
        border: 1px solid #1a1815;
        display: inline-block;
        margin: 1px;
        vertical-align: middle;
    }
    .cw-num {
        position: absolute;
        top: 1px;
        left: 2px;
        font-size: 9px;
        color: #c5a059;
        line-height: 1;
    }
    .cw-row {
        white-space: nowrap;
        height: 35px;
    }
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
# PUZZLE 1: WORDLE (3 TURNS, TARGET: SPINE)
# ==========================================
if st.session_state.stage == 1:
    st.markdown("""
        <div class='scroll-box'>
            <h3>📜 Scroll I: The Wordle Spell</h3>
            <p>Guess the 5-letter ancient word to break the first seal. You have only <b>3 attempts</b>!</p>
            <p>🟢 <b>Green</b>: Right letter, right spot.<br>
               🟡 <b>Yellow</b>: Right letter, wrong spot.<br>
               3️⃣ <b>Gray</b>: Letter not in word.</p>
        </div>
    """, unsafe_allow_html=True)
    
    target_word = "SPINE"
    max_turns = 3

    # Input form
    with st.form(key="wordle_form", clear_on_submit=True):
        col_in, col_btn = st.columns([3, 1])
        with col_in:
            guess_input = st.text_input("Enter 5-letter guess:", max_chars=5).strip().upper()
        with col_btn:
            st.write("")
            st.write("")
            submit_guess = st.form_submit_button("Submit Guess")

    if submit_guess:
        if len(guess_input) != 5 or not guess_input.isalpha():
            st.warning("⚠️ Please enter a valid 5-letter word!")
        elif len(st.session_state.wordle_guesses) < max_turns:
            st.session_state.wordle_guesses.append(guess_input)

    # Render Wordle Grid (3 Rows x 5 Columns)
    st.write("### 🧩 Wordle Grid")
    for row_idx in range(max_turns):
        cols = st.columns(5)
        
        # If guess exists for this row
        if row_idx < len(st.session_state.wordle_guesses):
            current_guess = st.session_state.wordle_guesses[row_idx]
            for col_idx in range(5):
                char = current_guess[col_idx]
                if char == target_word[col_idx]:
                    tile_class = "tile-correct"
                elif char in target_word:
                    tile_class = "tile-present"
                else:
                    tile_class = "tile-absent"
                cols[col_idx].markdown(f"<div class='wordle-box {tile_class}'>{char}</div>", unsafe_allow_html=True)
        else:
            # Empty row placeholder
            for col_idx in range(5):
                cols[col_idx].markdown("<div class='wordle-box tile-empty'>-</div>", unsafe_allow_html=True)

    st.write("")

    # Victory / Failure evaluation
    if len(st.session_state.wordle_guesses) > 0 and st.session_state.wordle_guesses[-1] == target_word:
        st.success("🎉 Correct! Scroll I unseals: *'Knowledge is the backbone of power.'*")
        if st.button("Proceed to Scroll II ➡️"):
            st.session_state.stage = 2
            st.rerun()
    elif len(st.session_state.wordle_guesses) >= max_turns:
        st.error(f"💥 The spell shattered! You used all {max_turns} attempts.")
        if st.button("Retry Scroll I 🔄"):
            st.session_state.wordle_guesses = []
            st.rerun()

# ==========================================
# PUZZLE 2: CROSSWORD WITH VISUAL GRID
# ==========================================
elif st.session_state.stage == 2:
    st.markdown("<div class='scroll-box'><h3>📜 Scroll II: The Lexicon Grid</h3><p>Fill in the answers below to complete the Ancient Crossword grid!</p></div>", unsafe_allow_html=True)
    
    st.markdown("""
    **Clues:**
    * **1 Across:** Written works of artistic value (10 letters)
    * **2 Across:** Written work bound together (4 letters)
    * **3 Down:** Look at and comprehend written text (4 letters)
    * **4 Across:** Mark letters or words on paper (5 letters)
    * **5 Down:** Tool used for writing/drawing (6 letters)
    * **6 Across:** Taxonomic rank below Kingdom (6 letters)
    * **7 Across:** Vertebrates belong to this phylum (8 letters)
    """)

    c1, c2 = st.columns(2)
    with c1:
        ans1 = st.text_input("1. Across:", key="cw1").strip().upper()
        ans2 = st.text_input("2. Across:", key="cw2").strip().upper()
        ans3 = st.text_input("3. Down:", key="cw3").strip().upper()
        ans4 = st.text_input("4. Across:", key="cw4").strip().upper()
    with c2:
        ans5 = st.text_input("5. Down:", key="cw5").strip().upper()
        ans6 = st.text_input("6. Across:", key="cw6").strip().upper()
        ans7 = st.text_input("7. Across:", key="cw7").strip().upper()

    # Build 10x12 Visual Grid Layout
    grid = [[" " for _ in range(12)] for _ in range(10)]
    numbers = {}

    def fill_word(word, row, col, is_across, number=None):
        if number:
            numbers[(row, col)] = number
        for idx, char in enumerate(word):
            r = row if is_across else row + idx
            c = col + idx if is_across else col
            if r < 10 and c < 12:
                grid[r][c] = char

    # Map user inputs into grid coordinates
    if ans1: fill_word(ans1, 0, 0, True, 1)        # LITERATURE
    else:    fill_word(" "*10, 0, 0, True, 1)
    
    if ans2: fill_word(ans2, 2, 7, True, 2)        # BOOK
    else:    fill_word(" "*4, 2, 7, True, 2)
    
    if ans3: fill_word(ans3, 0, 4, False, 3)       # READ (intersects LITERATURE at E)
    else:    fill_word(" "*4, 0, 4, False, 3)
    
    if ans4: fill_word(ans4, 3, 4, True, 4)        # WRITE (intersects READ at D)
    else:    fill_word(" "*5, 3, 4, True, 4)
    
    if ans5: fill_word(ans5, 3, 8, False, 5)       # PENCIL (intersects WRITE at E)
    else:    fill_word(" "*6, 3, 8, False, 5)
    
    if ans6: fill_word(ans6, 3, 8, True, 6)        # PHYLUM (intersects PENCIL at P)
    else:    fill_word(" "*6, 3, 8, True, 6)
    
    if ans7: fill_word(ans7, 7, 0, True, 7)        # CHORDATA
    else:    fill_word(" "*8, 7, 0, True, 7)

    # Render Visual HTML Grid
    st.write("### 🧩 Visual Crossword Map")
    grid_html = "<div style='display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;'>"
    for r in range(10):
        grid_html += "<div class='cw-row'>"
        for c in range(12):
            char = grid[r][c]
            num_str = f"<span class='cw-num'>{numbers[(r,c)]}</span>" if (r,c) in numbers else ""
            if char != " ":
                display_char = char if char != " " else ""
                grid_html += f"<div class='cw-cell'>{num_str}{display_char}</div>"
            else:
                grid_html += "<div class='cw-block'></div>"
        grid_html += "</div>"
    grid_html += "</div>"
    
    st.markdown(grid_html, unsafe_allow_html=True)

    if st.button("Unlock Scroll II"):
        if (ans1 == "LITERATURE" and ans2 == "BOOK" and ans3 == "READ" and 
            ans4 == "WRITE" and ans5 == "PENCIL" and ans6 == "PHYLUM" and ans7 == "CHORDATA"):
            st.success("🎉 Brilliant! Scroll II unseals: *'Words are keys to ancient mysteries.'*")
            st.session_state.cw_passed = True
        else:
            st.error("Some answers are incorrect. Check your answers and try again!")

    if st.session_state.get('cw_passed', False):
        if st.button("Proceed to Scroll III ➡️"):
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
