import streamlit as st
import random

# ASCII images for each move
rock = '''    
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''
paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''
scissors ='''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

ASCII_IMAGES = [rock, paper, scissors]
CHOICES = ["Rock", "Paper", "Scissors"]

st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="✂️",
    layout="wide"
)

# Custom CSS for compact output and full width
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.3rem !important;
        padding-bottom: 1.3rem !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100vw !important;
        width: 100vw !important;
    }
    html, body, .main {
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    h1, h2 {
        font-weight: 800;
        margin-bottom: 0.9rem;
    }
    .score-area {font-size:1.15em; margin-top:12px;}
    .result-msg {font-size:1.3em; margin-top:18px; text-align:center;}
    .footer {color:#888; margin-top:24px; text-align:center;}
    .stButton > button {
        font-size: 1em;
        padding: 0.2em 1.2em;
        margin: 0.2em 0.4em 0.8em 0.4em;
        border-radius: 0.7em;
        min-width: 104px;
    }
    .choice-selected {
        border: 2px solid #d22;
        color: #fff;
        background: #222;
    }
    .output-cols {
        display: flex;
        gap: 1.2em;
        margin-bottom: 1.1em;
        justify-content: center;
        width: 100%;
    }
    .output-single {
        flex: 1;
        min-width: 120px;
        max-width: 270px;
        text-align: center;
        background: #181c20;
        border-radius: 9px;
        margin-top: 4px;
        margin-bottom: 4px;
        padding: 0.2em 0.1em 0.1em 0.1em;
        display: inline-block;
        vertical-align: top;
        font-size: 0.95em;
    }
    .ascii-art-block {
        font-size: 0.98em;
        font-family: 'Fira Mono', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', monospace;
        background: none;
        color: #ebebeb;
        margin: 0.15em 0.1em 0.22em 0.1em;
        border-radius: 7px;
        overflow-x: auto;
        white-space: pre;
        text-align: left;
        padding: 0 0.1em;
    }
    @media (max-width: 900px) {
        .block-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        .output-cols {
            flex-direction: column;
            gap: 0.5em;
        }
        .output-single {
            min-width: 100px;
            max-width: 100vw;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👋 Welcome to Rock, Paper, Scissors!</h1>", unsafe_allow_html=True)

# Top controls and score area
cols_top = st.columns([2,1,1])
with cols_top[0]:
    st.markdown(
        f"<div class='score-area'>"
        f"<b>Wins:</b> {st.session_state.setdefault('score', {'Wins': 0, 'Losses': 0, 'Draws': 0})['Wins']} "
        f"| <b>Losses:</b> {st.session_state['score']['Losses']}<br>"
        f"<b>Draws:</b> {st.session_state['score']['Draws']}<br>"
        f"<b>Highest Wins:</b> {st.session_state.setdefault('highest_win', 0)}"
        f"</div>", unsafe_allow_html=True)
with cols_top[1]:
    if st.button("Play Again"):
        st.session_state["last_result"] = None
        st.session_state["last_user_choice"] = None
        st.session_state["last_computer_choice"] = None
        st.rerun()
with cols_top[2]:
    if st.button("Reset Score"):
        st.session_state["score"] = {"Wins": 0, "Losses": 0, "Draws": 0}
        st.session_state["highest_win"] = 0
        st.session_state["last_result"] = None
        st.session_state["last_user_choice"] = None
        st.session_state["last_computer_choice"] = None
        st.rerun()

st.markdown("#### What will you play? Pick your move below:")

# Choice buttons in a row, highlighting selection
cols_choices = st.columns(3)
user_choice = None
last_user_choice = st.session_state.get("last_user_choice", None)
for i, name in enumerate(CHOICES):
    with cols_choices[i]:
        if st.button(name, key=name):
            user_choice = i
            break

if user_choice is not None:
    computer_choice = random.randint(0, 2)
    st.session_state["last_user_choice"] = user_choice
    st.session_state["last_computer_choice"] = computer_choice

    # Game logic
    score = st.session_state["score"]
    if user_choice == computer_choice:
        result = "It's a Draw! Nobody wins, but that's okay. Try again!"
        score["Draws"] += 1
    elif (user_choice == 0 and computer_choice == 2) or \
         (user_choice == 1 and computer_choice == 0) or \
         (user_choice == 2 and computer_choice == 1):
        result = "You Win! Nicely played!"
        score["Wins"] += 1
        if score["Wins"] > st.session_state["highest_win"]:
            st.session_state["highest_win"] = score["Wins"]
    else:
        result = "You Lose! Better luck next time!"
        score["Losses"] += 1

    st.session_state["score"] = score
    st.session_state["last_result"] = result
    st.rerun()

# Show output above, compact and side by side
last_user_choice = st.session_state.get("last_user_choice", None)
last_computer_choice = st.session_state.get("last_computer_choice", None)
last_result = st.session_state.get("last_result", None)
if last_user_choice is not None and last_computer_choice is not None:
    # Output appears immediately after the buttons
    st.markdown(f"""
    <div class="output-cols">
      <div class="output-single">
        <b>You chose</b><br>
        {CHOICES[last_user_choice]}<br>
        <div class='ascii-art-block'>{ASCII_IMAGES[last_user_choice]}</div>
      </div>
      <div class="output-single">
        <b>Computer chose</b><br>
        {CHOICES[last_computer_choice]}<br>
        <div class='ascii-art-block'>{ASCII_IMAGES[last_computer_choice]}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div class='result-msg'>{last_result}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div class='footer'>Made with ❤️ <br/>Feeling lucky? Play again!</div>", unsafe_allow_html=True)