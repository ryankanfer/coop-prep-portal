import streamlit as st
import base64
import openai
from fpdf import FPDF
from io import BytesIO

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
            font-family: 'Lato', sans-serif;
        }}
        
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Lato&display=swap');

        .login-card {{
            background: rgba(0, 0, 0, 0.65);
            border-radius: 1rem;
            padding: 2rem;
            max-width: 400px;
            margin: 5rem auto;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            color: white;
            animation: fadeIn 0.8s ease-in-out;
        }}

        .login-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.75rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 0.5rem;
        }}

        .login-subtitle {{
            text-align: center;
            font-size: 0.9rem;
            margin-bottom: 2rem;
            color: #ccc;
        }}

        .stTextInput>div>div>input {{
            background-color: rgba(255,255,255,0.1);
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem;
        }}

        .stButton>button {{
            width: 100%;
            background-color: #4A63DD;
            color: white;
            font-weight: bold;
            border-radius: 0.5rem;
            padding: 0.75rem;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>
    """, unsafe_allow_html=True)

# --- SESSION INIT ---
if "stage" not in st.session_state:
    st.session_state.stage = "login"

# --- LOGIN PAGE ---
if st.session_state.stage == "login":
    set_background("background.jpg")

    st.markdown("""
    <div class="login-card">
        <div class="login-title">NYC Co-op Interview Prep Assistant</div>
        <div class="login-subtitle">The Board is Ready for You</div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_clicked = st.button("Login")

    st.markdown("""</div>""", unsafe_allow_html=True)

    if login_clicked:
        if username.strip() == "client" and password == "interviewready25":
            st.session_state.stage = "intro"
            st.rerun()
        else:
            st.error("Invalid credentials")
