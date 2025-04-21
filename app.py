# app.py

import streamlit as st
import openai
import os
import datetime
from fpdf import FPDF
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import random
import base64

# --- UTILS ---
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

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

# --- VISUALS ---
st.set_page_config(page_title="NYC Co-op Interview Prep", layout="centered")
logo_data = get_base64_image("assets/tkt_logo.png")
background_data = get_base64_image("assets/lobby_background.jpg")  # Doorman/lobby door scene

# --- QUOTES ---
tips = [
    "\U0001f4aa Confidence matters more than credentials.",
    "\U0001f4b3 Know your debt-to-income ratio.",
    "\U0001f4ca Practice answering financial questions clearly.",
    "\U0001f465 Dress for the boardroom, not the brunch."
]

# --- CSS ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@300;400;600&display=swap');
html, body, .stApp {{
    background: url("data:image/jpg;base64,{background_data}") no-repeat center center fixed;
    background-size: cover;
    font-family: 'Lato', sans-serif;
    color: #ffffff;
}}
.login-box {{
    background: rgba(0,0,0,0.45);
    padding: 2rem;
    border-radius: 16px;
    width: 360px;
    margin: 10vh auto 2vh auto;
    text-align: center;
}}
.login-heading {{
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #fff;
}}
.login-subhead {{
    font-size: 1rem;
    margin-bottom: 1.5rem;
    color: #f0f0f0;
}}
.stTextInput > div > input {{
    background-color: rgba(255,255,255,0.15);
    border-radius: 6px;
    border: none;
    padding: 10px;
    color: #fff;
    font-size: 0.95rem;
}}
.login-cta img {{
    width: 80px;
    margin-top: 1rem;
}}
#prep-tip {{
    text-align: center;
    margin-top: 3rem;
    font-size: 1.1rem;
    font-style: italic;
    color: #f8f8f8;
}}
</style>
""", unsafe_allow_html=True)

# --- LOGIN ---
st.markdown(f"""
<div class="login-box">
    <h1 class="login-heading">NYC Co-op Interview<br>Prep Assistant</h1>
    <p class="login-subhead">The Board is Ready for You</p>
""", unsafe_allow_html=True)

USERS = {"client": "interviewready25"}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        with st.spinner("Opening the boardroom doors..."):
            if USERS.get(username.strip()) == password:
                st.session_state.authenticated = True
                st.session_state.username = username.strip().capitalize()
                st.success("Simulated Boardroom")
            else:
                st.error("Invalid credentials")
    st.markdown(f"<div id='prep-tip'>{random.choice(tips)}</div>", unsafe_allow_html=True)
    st.stop()

# --- LOBBY PAGE (Step 2) ---
st.markdown("""
## Welcome to the Lobby
You've entered the building. The board is reviewing your file.

Fill out the details below so we can prep your custom guide.
""")

with st.form("prep_form"):
    name = st.text_input("Your Full Name", value=st.session_state.username)
    occupation = st.text_input("Occupation")
    income = st.text_input("Income")
    assets = st.text_input("Assets")
    personality = st.text_input("3 Personality Traits")
    residence = st.text_input("Current Residence")
    building = st.text_input("Target Building")
    listing = st.text_input("(optional) StreetEasy Link")
    file = st.file_uploader("Optional: Upload resume or intro letter")
    submitted = st.form_submit_button("Submit")

# --- HELPER FUNCTIONS ---
def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()

def generate_prep_guide(profile):
    model = "gpt-4o"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a luxury NYC broker helping prep a buyer for a co-op interview."},
            {"role": "user", "content": f"""
Name: {profile['name']}
Occupation: {profile['occupation']}
Income: {profile['income']}
Assets: {profile['assets']}
Personality: {profile['personality']}
Residence: {profile['residence']}
Building: {profile['building']}

Create:
1. 5 potential questions
2. Advice for financial transparency
3. What to avoid
4. A pep talk in 2 sentences
"""}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

def generate_pdf(name, content, listing):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.image("assets/logo.png", 10, 8, 33)
    pdf.ln(20)
    pdf.multi_cell(0, 10, f"Co-op Board Interview Prep for {name}\n\n" + content)
    if listing:
        pdf.ln(5)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 10, f"Listing: {listing}", ln=True, link=listing)
    pdf.set_text_color(100, 100, 100)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    pdf.set_y(-20)
    pdf.cell(0, 10, f"Prepared by Ryan Kanfer | @ryanxkanfer | {timestamp}", align='C')
    filename = sanitize_filename(f"{name}_Coop_Prep.pdf")
    pdf.output(filename)
    return filename

def upload_to_drive(filepath, buyer_name):
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    file_drive = drive.CreateFile({"title": f"{now}_{sanitize_filename(buyer_name)}.pdf", "parents": [{"id": FOLDER_ID}]})
    file_drive.SetContentFile(filepath)
    file_drive.Upload()
    return file_drive['alternateLink']

def log_to_sheet(name, building, listing):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([name, building, now, listing])

# --- SUBMIT HANDLER ---
if submitted:
    profile = {
        "name": name,
        "occupation": occupation,
        "income": income,
        "assets": assets,
        "personality": personality,
        "residence": residence,
        "building": building
    }

    with st.spinner("Creating your interview playbook..."):
        guide = generate_prep_guide(profile)

    guide_edit = st.text_area("Edit your guide if needed:", value=guide, height=400)

    if st.button("Finalize Guide"):
        filepath = generate_pdf(name, guide_edit, listing)
        link = upload_to_drive(filepath, name)
        log_to_sheet(name, building, listing)

        with open(filepath, "rb") as f:
            st.success("Ready for download")
            st.download_button("📥 Download PDF", f, file_name=filepath, mime="application/pdf")
        st.info(f"Saved to Drive: {link}")
        st.balloons()
        st.markdown("<div style='text-align:center; font-size:1.2rem; font-family: Playfair Display;'><em>The board will be <strong>very</strong> impressed.</em></div>", unsafe_allow_html=True)
