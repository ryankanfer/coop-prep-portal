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

# === HELPER: Image Encoding ===
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# === CONFIG ===
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

# === PAGE SETUP ===
st.set_page_config(page_title="NYC Co-op Interview Prep", layout="wide")
logo_data = get_base64_image("assets/tkt_logo.png")
background_data = get_base64_image("assets/background.jpg")

# === CSS ===
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@300;400;600&display=swap');

html, body, .stApp {{
    background: url("data:image/jpg;base64,{background_data}") no-repeat center center fixed;
    background-size: cover;
    font-family: 'Lato', sans-serif;
    color: #ffffff;
}}

html::before {{
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.35);
    z-index: 0;
}}

h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    text-shadow: 0 0 10px rgba(0,0,0,0.45);
}}

h3 {{
    font-family: 'Lato', sans-serif;
    font-weight: 400;
    text-align: center;
    color: #f1f1f1;
    margin-top: -10px;
    margin-bottom: 2rem;
    text-shadow: 0 0 6px rgba(0,0,0,0.3);
}}

.logo-img {{
    display: block;
    margin: 0 auto 1rem;
    width: 120px;
}}

.glass-box {{
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 2rem;
    max-width: 420px;
    margin: 0 auto;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}}

.stTextInput > div > input {{
    background-color: rgba(255,255,255,0.15);
    color: #ffffff;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 0.5rem;
}}

.stTextInput label, .stTextArea label {{
    color: #e0e0e0;
    font-weight: 300;
}}

.stButton>button {{
    background-color: #6366f1;
    color: #ffffff;
    font-weight: 600;
    font-size: 1rem;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    width: 100%;
    transition: all 0.3s ease-in-out;
}}

.stButton>button:hover {{
    transform: scale(1.03);
    box-shadow: 0 0 15px #a5b4fc;
}}
</style>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown(f"""
    <img src="data:image/png;base64,{logo_data}" class="logo-img" />
    <h1>NYC Co-op Interview<br>Prep Assistant</h1>
    <h3>The Board is Ready for You</h3>
""", unsafe_allow_html=True)

# === LOGIN & FORM ===
st.markdown('<div class="glass-box">', unsafe_allow_html=True)

USERS = {"client": "interviewready25"}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.text_input("Username").strip()
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state.authenticated = True
        else:
            st.error("Invalid username or password. Try again or text Ryan directly for access.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="glass-box">', unsafe_allow_html=True)

st.subheader("Fill this out — we'll handle the rest.")
with st.form("prep_form"):
    name = st.text_input("Buyer Name")
    occupation = st.text_input("Occupation")
    income = st.text_input("Income")
    assets = st.text_input("Assets")
    personality = st.text_input("Personality Traits")
    residence = st.text_input("Current Residence")
    building = st.text_input("Target Building")
    listing = st.text_input("StreetEasy Link (optional — paste it in for a pretty PDF)")
    file = st.file_uploader("Optional: Upload resume or personal letter")
    submitted = st.form_submit_button("Get me approved")

st.markdown('</div>', unsafe_allow_html=True)

# === REMAINING LOGIC OMITTED FOR BREVITY ===
