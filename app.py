
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

# --- PAGE SETTINGS ---
st.set_page_config(page_title="NYC Co-op Interview Prep", layout="centered")

# --- ASSET LOAD ---
logo_data = get_base64_image("assets/tkt_logo.png")
background_data = get_base64_image("assets/background.jpg")

# --- CSS STYLING ---
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

.login-title {{
    font-size: 2.5rem;
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    text-align: center;
    margin-top: 6vh;
    margin-bottom: 0.3em;
}}

.login-subtitle {{
    font-size: 1.1rem;
    text-align: center;
    margin-bottom: 2rem;
    color: #f0f0f0;
}}

.login-card {{
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 2rem;
    max-width: 400px;
    margin: 0 auto;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}}

.login-card .stTextInput > div > input,
.login-card .stTextArea > div > textarea {{
    background-color: rgba(0, 0, 0, 0.3);
    color: #ffffff;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.2);
}}

.login-card .stButton > button {{
    background-color: #6366f1;
    color: #ffffff;
    font-weight: 600;
    font-size: 1rem;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    margin-top: 1rem;
    transition: all 0.3s ease;
}}

.login-card .stButton > button:hover {{
    transform: scale(1.04);
    box-shadow: 0 0 14px #a5b4fc;
}}
</style>
""", unsafe_allow_html=True)

# Header + Subheader
st.markdown(f"""
<h1 class="login-title">NYC Co-op Interview<br>Prep Assistant</h1>
<p class="login-subtitle">The Board is Ready for You</p>
""", unsafe_allow_html=True)

# Glassy input card
st.markdown('<div class="login-card">', unsafe_allow_html=True)

# --- AUTHENTICATION ---
USERS = {"client": "interviewready25"}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if USERS.get(username.strip()) == password:
            st.session_state.authenticated = True
        else:
            st.error("Invalid username or password. Try again or text Ryan directly for access.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- FORM ---
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

# --- HELPER FUNCTIONS ---
def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()

def generate_prep_guide(profile):
    try:
        model = "gpt-4o"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a high-end NYC real estate agent helping a buyer prep for a co-op board interview."},
                {"role": "user", "content": f"""
Name: {profile['name']}
Occupation: {profile['occupation']}
Income: {profile['income']}
Assets: {profile['assets']}
Personality: {profile['personality']}
Residence: {profile['residence']}
Building: {profile['building']}

Please generate:
1. Common board interview questions
2. Tips for answering financial/personal Qs with grace
3. What to avoid
4. Final reminders before walking in
"""}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except:
        return "We're using a backup model — still great, just fewer bells & whistles."

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

# --- HANDLE SUBMISSION ---
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

    with st.spinner("Generating your co-op prep guide..."):
        guide = generate_prep_guide(profile)

    guide_edit = st.text_area("Review or edit your guide before finalizing:", value=guide, height=400)

    if st.button("Finalize PDF"):
        filepath = generate_pdf(name, guide_edit, listing)
        link = upload_to_drive(filepath, name)
        log_to_sheet(name, building, listing)
        with open(filepath, "rb") as f:
            st.success("✨ Done! Here’s your download:")
            st.download_button("📥 Download PDF", f, file_name=filepath, mime="application/pdf", use_container_width=True)
        st.info(f"A copy was saved to Google Drive here: {link}")
        st.balloons()
        st.markdown("""
        <div style="margin-top: 2rem; text-align: center; font-size: 1.2rem; font-family: 'Playfair Display', serif; color: #ffffff;">
            <em>The board will be <strong>very</strong> impressed.</em><br>
            You're prepped. You're polished. You're approved.
        </div>
        """, unsafe_allow_html=True)
