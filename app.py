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
        <div style='text-align: center; padding: 2rem; background: rgba(0, 0, 0, 0.6); border-radius: 20px; max-width: 400px; margin: auto;'>
            <h2 style='margin-bottom: 0.5rem; font-size: 2rem;'>NYC Co-op Interview Prep Assistant</h2>
            <p style='color: #ccc; font-size: 0.9rem;'>The Board is Ready for You</p>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username.strip() == "client" and password == "interviewready25":
                st.session_state.stage = "onboarding"
                st.rerun()
            else:
                st.error("Invalid credentials")

# --- PAGE 2: ONBOARDING COPY ---
elif st.session_state.stage == "onboarding":
    set_background("background.jpg")
    st.markdown("""
        <div style='text-align: center; padding: 2rem; background: rgba(0, 0, 0, 0.6); border-radius: 20px; max-width: 600px; margin: auto;'>
            <h2 style='margin-bottom: 1rem;'>Welcome to the simulation.</h2>
            <p style='text-align: left;'>
            Buying into a co-op in NYC? You’re not just buying a home — you’re buying shares in a corporation.
            And that corporation has a board that acts less like management… and more like a tight-knit neighborhood deciding if they want you at their block party.
            <br><br>
            They’ve seen your application. They’ve reviewed your financials.<br>
            But now? They want to see if you fit in.
            <br><br>
            This app is your prep concierge.
            You’ll enter a simulation modeled on actual co-op board interviews.
            Expect questions about your money, lifestyle, pets, and how you plan to use the apartment.
            How you answer shapes how the board reacts.
            <br><br>
            No paperwork. No pressure.<br>
            Just you, the board, and a little friendly judgment.
            </p>
            <br>
            <button onclick="window.location.href='/';" style='padding: 0.75rem 1.5rem; border: none; background-color: #6C63FF; color: white; border-radius: 10px; font-weight: bold;'>Enter Lobby</button>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Enter Lobby"):
        st.session_state.stage = "lobby"
        st.rerun()

# --- PAGE 3: LOBBY ---
elif st.session_state.stage == "lobby":
    set_background("lobby.jpg")
    st.markdown("""
        <h1 style='text-align: center;'>Welcome to the Lobby</h1>
        <p style='text-align: center;'>The doorman will see you in now.</p>
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
        st.rerun()
