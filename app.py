import streamlit as st
import openai
import os
import datetime
from fpdf import FPDF
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json
import base64

# --- FUNCTIONS ---
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
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()

# --- CONFIGURATION ---
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
service_account_info = st.secrets["gcp_service_account"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(dict(service_account_info), SCOPES)
client_sheet = gspread.authorize(credentials)
drive_auth = GoogleAuth()
drive_auth.credentials = credentials
drive = GoogleDrive(drive_auth)
FOLDER_ID = "1A2BcDeFgH_IJKlmnopQRstUvWX"
SHEET_NAME = "Co-op Prep Submissions"
sheet = client_sheet.open(SHEET_NAME).sheet1

st.set_page_config(page_title="NYC Co-op Interview Prep", layout="centered")

# --- PAGE CONTROL ---
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "profile" not in st.session_state:
    st.session_state.profile = {}

# --- LANDING PAGE ---
if st.session_state.page == "landing":
    set_background("background.jpg")
    st.markdown("""
    <style>
        h1 { text-align: center; font-size: 3rem; font-family: 'Playfair Display'; }
        p { text-align: center; font-size: 1.2rem; }
        .login-box { background-color: rgba(255, 255, 255, 0.07); padding: 2rem; border-radius: 12px; max-width: 400px; margin: auto; }
        .stTextInput input { background-color: white !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="login-box">
            <h1>NYC Co-op Interview Prep Assistant</h1>
            <p>The Board is Ready for You</p>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", key="user")
    password = st.text_input("Password", type="password", key="pass")
    if st.button("Enter Lobby"):
        if username.strip() == "client" and password == "interviewready25":
            st.session_state.page = "lobby"
        else:
            st.error("Invalid credentials. Text Ryan if you're stuck.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- LOBBY PAGE ---
elif st.session_state.page == "lobby":
    set_background("lobby.jpg")
    st.markdown("""<h1 style='text-align: center;'>Welcome to the Lobby</h1>""", unsafe_allow_html=True)
    with st.form("buyer_info"):
        name = st.text_input("Full Name")
        occupation = st.text_input("Occupation")
        income = st.text_input("Annual Income")
        assets = st.text_input("Cash in Bank")
        building = st.text_input("Target Building")
        reason = st.radio("Reason for Purchase", ["Primary Residence", "Pied-à-Terre", "Gift"])
        intensity = st.radio("Board Intensity", ["Liberal", "Conservative"])
        work_type = st.radio("Type of Work", ["W2", "Self Employed"])
        pets = st.radio("Any Pets?", ["Yes", "No"])
        submit = st.form_submit_button("Enter Boardroom")

    if submit:
        st.session_state.profile = {
            "name": name,
            "occupation": occupation,
            "income": income,
            "assets": assets,
            "building": building,
            "reason": reason,
            "intensity": intensity,
            "work_type": work_type,
            "pets": pets
        }
        st.session_state.page = "board"
        st.experimental_rerun()

# --- BOARD INTERVIEW SIMULATION ---
elif st.session_state.page == "board":
    set_background("board_interview.jpg")
    profile = st.session_state.profile
    name = profile.get("name", "the applicant")

    board_members = [
        {"name": "Evelyn Sharp", "role": "Board President", "tone": "formal"},
        {"name": "Randy Gold", "role": "Finance Chair", "tone": "curious"},
        {"name": "Maya Patel", "role": "Culture Lead", "tone": "warm"}
    ]

    st.markdown(f"""
        <h1 style='text-align: center;'>The Simulated Boardroom</h1>
        <p style='text-align: center;'>You've been granted a seat. Let's see how the conversation unfolds.</p>
        <br>
    """, unsafe_allow_html=True)

    st.markdown("#### Questions from the Board")

    # Generate tailored questions
    questions = [
        f"{board_members[0]['name']}: Tell us why you're interested in {profile['building']}.",
        f"{board_members[1]['name']}: As someone who is {profile['work_type']}, how do you ensure financial stability month to month?",
        f"{board_members[0]['name']}: What about your current income of {profile['income']} gives you confidence to take this on?",
        f"{board_members[1]['name']}: Can you explain where your {profile['assets']} in assets are currently held?",
        f"{board_members[2]['name']}: Do you anticipate hosting often? What's your lifestyle like as a {profile['occupation']}?",
        f"{board_members[0]['name']}: The board has had mixed experiences with pets. You marked '{profile['pets']}'. Can you clarify?"
    ]

    responses = []
    for i, q in enumerate(questions):
        response = st.text_area(q, key=f"response_{i}")
        if response:
            if "confidence" in q.lower():
                st.markdown(f"**{board_members[0]['name']} reacts:** Thank you, {name}, that’s reassuring.")
            elif "hosting" in q.lower():
                st.markdown(f"**{board_members[2]['name']} reacts:** Appreciate the honesty, {name}.")
            elif "assets" in q.lower():
                st.markdown(f"**{board_members[1]['name']} reacts:** That adds helpful context.")
        responses.append(response)

    st.markdown("<br><br><h4 style='text-align: center;'>You're doing great.</h4>", unsafe_allow_html=True)
