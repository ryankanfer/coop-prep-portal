import streamlit as st
import base64
import openai
import datetime
from fpdf import FPDF
from io import BytesIO

# --- SETUP ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- GLOBAL STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Playfair Display', serif;
        }

        .glass-card {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            color: white;
            text-align: center;
            margin: 3rem auto;
            width: 400px;
        }

        .glass-button {
            background-color: #6B7EFF;
            color: white;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 1rem;
            transition: background-color 0.3s ease;
        }

        .glass-button:hover {
            background-color: #505edb;
        }

        .glass-input input {
            background-color: #1e1e1e;
            color: white;
            border-radius: 8px;
            padding: 0.75rem;
            border: none;
        }

        .glass-input input::placeholder {
            color: #aaa;
        }

        .stTextInput > div > div > input {
            background-color: #1e1e1e;
            color: white;
        }

        .stTextInput label,
        .stSelectbox label,
        .stRadio label,
        .stTextArea label {
            font-size: 1rem !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- BACKGROUND IMAGE ---
def get_base64_image(img_path):
    with open(img_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def set_background(image_path):
    b64_img = get_base64_image(image_path)
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{b64_img}");
            background-size: cover;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INIT ---
if "stage" not in st.session_state:
    st.session_state.stage = "login"

if "buyer" not in st.session_state:
    st.session_state.buyer = {}

if "responses" not in st.session_state:
    st.session_state.responses = {}

# --- PAGE: LOGIN ---
if st.session_state.stage == "login":
    set_background("background.jpg")
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h2>NYC Co-op Interview Prep Assistant</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top: -10px;'>The Board is Ready for You</p>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", key="login", help="Login", use_container_width=True):
            if username == "client" and password == "interviewready25":
                st.session_state.stage = "intro"
                st.experimental_rerun()
            else:
                st.error("Invalid login. Try again or text Ryan directly for access.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE: INTRO ---
elif st.session_state.stage == "intro":
    set_background("background.jpg")
    st.markdown("""
        <div class='glass-card'>
            <h2>Welcome to the simulation.</h2>
            <p style='text-align: left;'>
                Buying into a co-op in NYC? You’re not just buying a home — you’re buying shares in a corporation. And that corporation has a board that acts less like management… and more like a tight-knit neighborhood deciding if they want you at their block party.
            </p>
            <p style='text-align: left;'>
                They’ve seen your application. They’ve reviewed your financials.<br>
                But now? They want to see if you fit in.
            </p>
            <p style='text-align: left;'>
                This app is your prep concierge.
                You’ll enter a simulation modeled on actual co-op board interviews.
                Expect questions about your money, lifestyle, pets, and how you plan to use the apartment. How you answer shapes how the board reacts.
            </p>
            <p style='text-align: left;'>
                No paperwork. No pressure. <br>
                Just you, the board, and a little friendly judgment.
            </p>
            <form action="" method="post">
                <button class="glass-button" type="submit" name="enter_lobby">Enter Lobby</button>
            </form>
        </div>
    """, unsafe_allow_html=True)

    if "enter_lobby" in st.query_params:
        st.session_state.stage = "lobby"
        st.experimental_rerun()

# NOTE: Remaining pages (lobby, interview, etc.) not yet included in this snippet.
# Continue integration from here to cover lobby form, boardroom Q&A, and PDF generation steps.
