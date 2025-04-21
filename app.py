import streamlit as st
import base64
import datetime
from fpdf import FPDF
from io import BytesIO

# --- CONFIG ---
st.set_page_config(page_title="NYC Co-op Interview Prep", layout="centered")

# --- BACKGROUND SETUP ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def set_background(image_path):
    b64_img = get_base64_image(image_path)
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_img}");
            background-size: cover;
            background-position: center;
            font-family: 'Lato', sans-serif;
        }}
        .glass-box {{
            background: rgba(0, 0, 0, 0.5);
            padding: 2rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }}
        .headline {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            text-align: center;
            font-weight: bold;
            color: white;
        }}
        .subtext {{
            color: white;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE SETUP ---
if "stage" not in st.session_state:
    st.session_state.stage = "login"
if "buyer" not in st.session_state:
    st.session_state.buyer = {}
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --- PAGE 1: LOGIN ---
if st.session_state.stage == "login":
    set_background("background.jpg")
    st.markdown("<div class='glass-box' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<div class='headline'>NYC Co-op Interview Prep Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtext'>The Board is Ready for You</div>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username.strip() == "client" and password == "interviewready25":
            st.session_state.stage = "intro"
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2: INTRO LANDING PAGE ---
elif st.session_state.stage == "intro":
    set_background("background.jpg")
    st.markdown("""
        <div class='glass-box' style='max-width: 600px; margin: 0 auto;'>
        <div class='headline'>Welcome to the simulation.</div>
        <div class='subtext' style='text-align: left;'>
            Buying into a co-op in NYC? You’re not just buying a home — you’re buying shares in a corporation.
            And that corporation has a board that acts less like management… and more like a tight-knit neighborhood
            deciding if they want you at their block party.<br><br>
            They’ve seen your application. They’ve reviewed your financials.<br>
            But now? They want to see if you fit in.<br><br>
            This app is your prep concierge. You’ll enter a simulation modeled on actual co-op board interviews.
            Expect questions about your money, lifestyle, pets, and how you plan to use the apartment.
            How you answer shapes how the board reacts.<br><br>
            No paperwork. No pressure.<br>
            Just you, the board, and a little friendly judgment.
        </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Enter Lobby"):
        st.session_state.stage = "lobby"
        st.rerun()

# --- PAGE 3: LOBBY FORM ---
elif st.session_state.stage == "lobby":
    set_background("lobby.jpg")
    st.markdown("""
        <div class='glass-box' style='max-width: 850px; margin: 0 auto;'>
        <div class='headline'>Fill in Your Details</div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.buyer["name"] = st.text_input("Your Name")
        st.session_state.buyer["occupation"] = st.text_input("Occupation")
        st.session_state.buyer["income"] = st.text_input("Income")
    with col2:
        st.session_state.buyer["assets"] = st.text_input("Assets (Cash in Bank)")
        st.session_state.buyer["building"] = st.text_input("Target Building")
        st.session_state.buyer["reason"] = st.selectbox("Reason for Purchase", ["Primary Residence", "Pied E Terre", "Gift"])
    col3, col4 = st.columns(2)
    with col3:
        st.session_state.buyer["work_type"] = st.radio("Type of Work", ["W2", "Self Employed"])
    with col4:
        st.session_state.buyer["intensity"] = st.radio("Board Intensity", ["Liberal", "Conservative"])
    st.session_state.buyer["pets"] = st.radio("Pets", ["Yes", "No"])
    if st.button("Enter Boardroom"):
        st.session_state.stage = "interview"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
