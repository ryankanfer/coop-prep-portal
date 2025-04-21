import streamlit as st
import base64
from fpdf import FPDF
from io import BytesIO

# --- SETUP ---
st.set_page_config(page_title="Co-op Interview Prep", layout="centered")

# --- IMAGES ---
def get_base64_image(img_path):
    with open(img_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def set_background(image_path):
    b64_img = get_base64_image(image_path)
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&display=swap');
        
        .stApp {{
            background-image: url("data:image/jpg;base64,{b64_img}");
            background-size: cover;
            background-position: center;
        }}

        .glass-card {{
            background: rgba(0, 0, 0, 0.5);
            border-radius: 20px;
            padding: 2rem;
            max-width: 420px;
            margin: 3rem auto;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        }}

        .glass-card h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            color: white;
            text-align: center;
            margin-bottom: 0.5rem;
        }}

        .glass-card p {{
            text-align: center;
            color: #ccc;
            margin-top: 0;
            font-size: 0.9rem;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- LOGIN PAGE ---
def login_page():
    set_background("background.jpg")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h1>NYC Co-op Interview Prep Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p>The Board is Ready for You</p>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "client" and password == "interviewready25":
            st.session_state.stage = "intro"
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.markdown('</div>', unsafe_allow_html=True)

# --- SESSION INIT ---
if "stage" not in st.session_state:
    st.session_state.stage = "login"

# --- MAIN ---
if st.session_state.stage == "login":
    login_page()
