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

# --- CSS STYLING ---
logo_data = get_base64_image("assets/tkt_logo.png")
background_data = get_base64_image("assets/background.jpg")

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

/* Ambient spotlight */
.overlay-spotlight::before {{
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 40%;
    transform: translate(-50%, -50%);
    background: radial-gradient(ellipse at center, rgba(0,0,0,0.15), transparent 70%);
    z-index: 0;
}}

.login-container {{
    padding: 2rem;
    max-width: 420px;
    margin: 4vh auto 2vh;
    position: relative;
    text-align: center;
    z-index: 2;
}}

.login-logo {{
    width: 120px;
    margin-bottom: 1.2rem;
    animation: slideFade 1.2s ease-out forwards;
    opacity: 0;
    transform: translateY(-30px);
}}

@keyframes slideFade {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.login-heading {{
    font-size: 2.5rem;
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    margin-bottom: 0.3rem;
    text-shadow: 0 0 10px rgba(0,0,0,0.4);
}}

.login-subhead {{
    font-size: 1.1rem;
    color: #eeeeee;
    margin-bottom: 2rem;
    text-shadow: 0 0 6px rgba(0,0,0,0.3);
}}

.stTextInput > div > input,
.stTextArea > div > textarea {{
    background-color: rgba(255,255,255,0.15);
    color: #ffffff;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 0.5rem;
    font-family: 'Lato', sans-serif;
    width: 70% !important;
    margin: 0 auto;
    display: block;
}}

.stTextInput input:hover {{
    box-shadow: 0 0 6px rgba(255,255,255,0.2);
}}

label, .stTextInput label, .stTextArea label {{
    color: #e0e0e0;
    font-weight: 300;
    font-family: 'Lato', sans-serif;
    text-align: left;
    width: 70%;
    display: block;
    margin: 0 auto;
    padding-left: 5px;
}}

.stButton>button {{
    background-color: #6366f1;
    color: #ffffff;
    font-family: 'Lato', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    width: 70%;
    display: block;
    margin: 1rem auto;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 0 0 rgba(0,0,0,0);
}}

.stButton>button:hover {{
    transform: scale(1.03);
    box-shadow: 0 0 15px #a5b4fc;
}}

.scroll-hint {{
  position: absolute;
  bottom: 4vh;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.5rem;
  color: #ffffff88;
  animation: pulse 2s infinite;
}}
@keyframes pulse {{
  0%, 100% {{ opacity: 0.4; transform: translate(-50%, 0); }}
  50% {{ opacity: 1; transform: translate(-50%, 5px); }}
}}

.footer-signature {{
  position: absolute;
  bottom: 2vh;
  width: 100%;
  text-align: center;
  color: #cccccc;
  font-size: 0.9rem;
  font-family: 'Lato', sans-serif;
}}
</style>
""
