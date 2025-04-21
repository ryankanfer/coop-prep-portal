import streamlit as st
import base64
import openai
import datetime
from fpdf import FPDF
from io import BytesIO

# --- SETUP ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- IMAGES ---
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
            font-family: 'Playfair Display', serif;
        }}
        .input-container {{
            background-color: rgba(0, 0, 0, 0.3);
            padding: 2rem;
            border-radius: 12px;
            width: 450px;
            margin: 0 auto;
        }}
        .title-card h1 {{
            text-align: center;
            font-size: 2rem;
            color: white;
            font-weight: bold;
            line-height: 1.2;
        }}
        .title-card p {{
            text-align: center;
            color: #ddd;
        }}
        .stTextInput > div > div > input {{
            background-color: #1e1e1e;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }}
        .stPassword > div > div > input {{
            background-color: #1e1e1e;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }}
        .stButton button {{
            background-color: #5b68ff;
            color: white;
            width: 100%;
            padding: 10px;
            border-radius: 8px;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- SESSION ---
if "stage" not in st.session_state:
    st.session_state.stage = "login"
if "buyer" not in st.session_state:
    st.session_state.buyer = {}
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --- PAGE 1: LOGIN ---
if st.session_state.stage == "login":
    set_background("background.jpg")
    with st.container():
        st.markdown("""
        <div class='title-card'>
            <h1>NYC Co-op Interview Prep Assistant</h1>
            <p>The Board is Ready for You</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='input-container'>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_clicked = st.button("Login")
        st.markdown("</div>", unsafe_allow_html=True)

    if login_clicked:
        if username.strip() == "client" and password == "interviewready25":
            st.session_state.stage = "intro"
            st.rerun()
        else:
            st.error("Invalid credentials")

# --- PAGE 2: INTRO ---
elif st.session_state.stage == "intro":
    set_background("background.jpg")
    st.markdown("""
        <style>
        .intro-container {
            background-color: rgba(0, 0, 0, 0.4);
            padding: 2rem;
            border-radius: 12px;
            max-width: 700px;
            margin: 0 auto;
            color: white;
            font-family: 'Playfair Display', serif;
        }
        .intro-container h1 {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
        }
        .intro-container p {
            font-size: 1rem;
            line-height: 1.6;
        }
        .center-button {
            display: flex;
            justify-content: center;
            margin-top: 1.5rem;
        }
        .center-button button {
            background-color: #5b68ff;
            color: white;
            border-radius: 8px;
            padding: 10px 30px;
        }
        </style>
        <div class='intro-container'>
            <h1>Welcome to the simulation.</h1>
            <p>Buying into a co-op in NYC? You’re not just buying a home — you’re buying shares in a corporation. And that corporation has a board that acts less like management… and more like a tight-knit neighborhood deciding if they want you at their block party.</p>
            <p>They’ve seen your application. They’ve reviewed your financials. But now? They want to see if you fit in.</p>
            <p>This app is your prep concierge.</p>
            <p>You’ll enter a simulation modeled on actual co-op board interviews. Expect questions about your money, lifestyle, pets, and how you plan to use the apartment. How you answer shapes how the board reacts.</p>
            <p>No paperwork. No pressure. Just you, the board, and a little friendly judgment.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        if st.button("Enter Lobby", key="intro_next"):
            st.session_state.stage = "lobby"
            st.rerun()

# The remaining stages ('lobby', 'interview', etc.) continue below...
