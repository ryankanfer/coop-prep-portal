# app.py

import streamlit as st
import base64
from fpdf import FPDF
from io import BytesIO

# --- SETUP ---
openai_api_key = st.secrets.get("OPENAI_API_KEY")

# --- UTILS ---
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
            background-attachment: fixed;
        }}
        .glass-box {{
            background: rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            max-width: 500px;
            margin: 3rem auto;
            color: #fff;
        }}
        .glass-box h1, .glass-box h2, .glass-box p {{
            text-align: center;
        }}
        .stTextInput label, .stSelectbox label, .stRadio label {{
            font-weight: 600;
            font-size: 1.1rem;
            color: white;
        }}
        .stButton button {{
            width: 100%;
            background-color: #4169E1;
            color: white;
            border: none;
            padding: 0.6rem;
            border-radius: 8px;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- SESSION INIT ---
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
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("""
            <h1>NYC Co-op Interview Prep Assistant</h1>
            <p>The Board is Ready for You</p>
        """, unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username.strip() == "client" and password == "interviewready25":
                st.session_state.stage = "intro"
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2: SIMULATION INTRO ---
elif st.session_state.stage == "intro":
    set_background("background.jpg")
    with st.container():
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("""
            <h1>Welcome to the simulation.</h1>
            <p>Buying into a co-op in NYC? You’re not just buying a home — you’re buying shares in a corporation. And that corporation has a board that acts less like management… and more like a tight-knit neighborhood deciding if they want you at their block party.</p>
            <p>They’ve seen your application. They’ve reviewed your financials.<br>But now? They want to see if you fit in.</p>
            <p>This app is your prep concierge.</p>
            <p>You’ll enter a simulation modeled on actual co-op board interviews.<br>Expect questions about your money, lifestyle, pets, and how you plan to use the apartment. How you answer shapes how the board reacts.</p>
            <p>No paperwork. No pressure.<br>Just you, the board, and a little friendly judgment.</p>
        """, unsafe_allow_html=True)
        if st.button("Enter Lobby"):
            st.session_state.stage = "lobby"
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3: LOBBY FORM ---
elif st.session_state.stage == "lobby":
    set_background("lobby.jpg")
    with st.container():
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("""
            <h1>Welcome to the Lobby</h1>
            <p>The doorman will see you in now.</p>
        """, unsafe_allow_html=True)
        with st.form("lobby_form"):
            st.session_state.buyer["name"] = st.text_input("Your Name")
            st.session_state.buyer["occupation"] = st.text_input("Occupation")
            st.session_state.buyer["income"] = st.text_input("Income")
            st.session_state.buyer["assets"] = st.text_input("Assets (Cash in Bank)")
            st.session_state.buyer["building"] = st.text_input("Target Building")
            st.session_state.buyer["reason"] = st.selectbox("Reason for Purchase", ["Primary Residence", "Pied E Terre", "Gift"])
            st.session_state.buyer["intensity"] = st.radio("Board Intensity", ["Liberal", "Conservative"])
            st.session_state.buyer["work_type"] = st.radio("Type of Work", ["W2", "Self Employed"])
            st.session_state.buyer["pets"] = st.radio("Pets", ["Yes", "No"])
            submitted = st.form_submit_button("Enter Boardroom")
        if submitted:
            st.session_state.stage = "interview"
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Remaining interview simulation code and feedback PDF logic should follow as before.
