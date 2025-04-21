import streamlit as st
import base64
import openai
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
        }}
        .login-container {{
            background: rgba(0, 0, 0, 0.55);
            padding: 2rem;
            border-radius: 20px;
            max-width: 400px;
            margin: 6rem auto;
            text-align: center;
            box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.3);
        }}
        .login-container input {{
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem;
            margin-bottom: 1rem;
            width: 100%;
        }}
        .login-container input::placeholder {{
            color: #ccc;
        }}
        .login-container button {{
            background-color: #5a65ea;
            color: white;
            border: none;
            padding: 0.75rem;
            width: 100%;
            border-radius: 10px;
            font-weight: bold;
            margin-top: 1rem;
            transition: 0.3s;
        }}
        .login-container button:hover {{
            background-color: #434fda;
            cursor: pointer;
        }}
        .login-header {{
            font-size: 1.6rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.5rem;
        }}
        .login-subheader {{
            font-size: 1rem;
            color: #eee;
            margin-bottom: 2rem;
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
    
    st.markdown("""
    <div class="login-container">
        <div class="login-header">NYC Co-op Interview Prep Assistant</div>
        <div class="login-subheader">The Board is Ready for You</div>
        <form>
            <input type="text" name="username" placeholder="Username" id="username-field">
            <input type="password" name="password" placeholder="Password" id="password-field">
        </form>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", label_visibility="collapsed")
    password = st.text_input("Password", type="password", label_visibility="collapsed")

    login_btn = st.button("Login")
    if login_btn:
        if username.strip() == "client" and password == "interviewready25":
            st.session_state.stage = "intro"
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.markdown("</div>", unsafe_allow_html=True)

# --- NEXT STAGES FOLLOW ---
