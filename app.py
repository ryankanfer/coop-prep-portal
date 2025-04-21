# Revised streamlit app.py with interactive landing UX upgrades

import streamlit as st
import time
import random
import base64

# --- CONFIG ---
st.set_page_config(page_title="NYC Co-op Interview Prep", layout="centered")

# --- ASSETS ---
background_image = "background.jpg"
logo_image = "tkt_logo.png"

# --- UTIL ---
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_encoded = get_base64_image(f"assets/{background_image}")
logo_encoded = get_base64_image(f"assets/{logo_image}")

# --- STYLES ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@300;400;600&display=swap');

html, body, .stApp {{
    background: url("data:image/jpg;base64,{bg_encoded}") no-repeat center center fixed;
    background-size: cover;
    font-family: 'Lato', sans-serif;
    color: #ffffff;
}}

.overlay-container {{
    background: rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 2rem;
    max-width: 380px;
    margin: 3rem auto;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    text-align: center;
}}

.overlay-container img {{
    width: 80px;
    opacity: 0.6;
    position: absolute;
    bottom: 18px;
    right: 24px;
}}

h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    text-align: center;
    margin-top: 5vh;
}}

h3 {{
    font-weight: 400;
    font-size: 1rem;
    text-align: center;
    color: #eee;
    margin-bottom: 2rem;
}}

input[type="text"], input[type="password"] {{
    width: 100%;
    padding: 0.6rem;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 6px;
    color: white;
    margin-bottom: 1rem;
}}

.stButton > button {{
    width: 100%;
    background: #6366f1;
    color: white;
    font-weight: 600;
    padding: 0.6rem;
    border-radius: 8px;
    border: none;
    transition: 0.3s;
}}

.stButton > button:hover {{
    transform: scale(1.02);
    box-shadow: 0 0 12px #a5b4fc;
}}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<h1>NYC Co-op Interview<br>Prep Assistant</h1>
<h3>The Board is Ready for You</h3>
""", unsafe_allow_html=True)

# --- LOGIN CARD ---
st.markdown(f"""
<div class="overlay-container">
    <form>
        <input type="text" name="username" placeholder="Username" id="username"/>
        <input type="password" name="password" placeholder="Password" id="password"/>
    </form>
    <img src="data:image/png;base64,{logo_encoded}" />
""", unsafe_allow_html=True)

# --- LOGIN FUNCTION ---
USERS = {"client": "interviewready25"}

username = st.session_state.get("username", "")
password = st.session_state.get("password", "")

username = st.text_input("", key="username", label_visibility="collapsed")
password = st.text_input("", type="password", key="password", label_visibility="collapsed")

if st.button("Login"):
    with st.spinner("Loading your boardroom..."):
        time.sleep(1.5)
        if USERS.get(username) == password:
            st.success("Simulated Boardroom Unlocked ✅")
            st.markdown("""
            <div style="text-align:center; font-size: 1.3rem; margin-top: 1rem;">
                🚪 <em>You enter through double doors as the board awaits...</em>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("Incorrect login. Text Ryan directly for access.")

st.markdown("</div>", unsafe_allow_html=True)

# --- DAILY PREP TIPS ---
TIPS = [
    "💡 Keep financial answers factual, not defensive.",
    "🧠 Know your debt-to-income ratio.",
    "👔 Dress like you're already approved.",
    "📝 Bring a printed copy of your reference letters just in case.",
    "🤝 Make eye contact with everyone in the room."
]

st.markdown(f"""
<div style="margin-top: 2rem; text-align: center; font-size: 0.9rem; font-style: italic; opacity: 0.8;">
    {random.choice(TIPS)}
</div>
""", unsafe_allow_html=True)
