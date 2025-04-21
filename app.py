import streamlit as st
import base64
from PIL import Image
import time

# --- FUNCTIONS ---
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(image_path):
    bg = get_base64_image(image_path)
    st.markdown(f"""
    <style>
    .stApp {{
        background: url("data:image/jpg;base64,{bg}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- PAGE SETUP ---
st.set_page_config(page_title="NYC Co-op Prep", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Lato:wght@400;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Lato', sans-serif;
        color: white;
    }}

    .login-box {{
        background-color: rgba(0,0,0,0.4);
        padding: 2rem;
        border-radius: 20px;
        width: 350px;
        margin: 0 auto;
        text-align: center;
    }}

    .login-box input {{
        margin-top: 0.75rem;
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
        border: none;
        border-radius: 8px;
        background-color: rgba(255,255,255,0.1);
        color: white;
    }}

    .login-logo {{
        width: 70px;
        margin: 1.5rem auto 0;
        display: block;
    }}

    .quote {{
        text-align: center;
        font-size: 1.1rem;
        font-style: italic;
        margin-top: 2rem;
        opacity: 0.8;
    }}
    </style>
""", unsafe_allow_html=True)

# --- GLOBALS ---
USERS = {"client": "interviewready25"}
PREP_QUOTES = [
    "Know your debt-to-income ratio.",
    "Smile — but don’t overshare.",
    "Be concise, confident, and calm.",
    "This isn’t a test. It’s a vibe check.",
    "They want to like you. Help them."
]

# --- LOGIN LOGIC ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "login_stage" not in st.session_state:
    st.session_state.login_stage = "login"

# --- LOGIN PAGE ---
if not st.session_state.authenticated:
    if st.session_state.login_stage == "login":
        set_background("/mnt/data/background.jpg")
        st.markdown("<h1 style='text-align: center; font-family: Playfair Display; font-size: 2.5rem;'>NYC Co-op Interview<br>Prep Assistant</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>The Board is Ready for You</p>", unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='login-box'>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                with st.spinner("Verifying credentials..."):
                    time.sleep(1.2)
                    if USERS.get(username.strip()) == password:
                        st.session_state.authenticated = True
                        st.session_state.login_stage = "lobby"
                        st.experimental_rerun()
                    else:
                        st.error("Invalid username or password. Try again or text Ryan directly for access.")
            st.image("/mnt/data/tkt_logo.png", width=40, output_format='PNG')
            st.markdown("</div>", unsafe_allow_html=True)

        quote = PREP_QUOTES[hash(time.time()) % len(PREP_QUOTES)]
        st.markdown(f"<p class='quote'>🧠 {quote}</p>", unsafe_allow_html=True)
        st.stop()

# --- LOBBY PAGE ---
if st.session_state.authenticated and st.session_state.login_stage == "lobby":
    set_background("/mnt/data/lobby_background.jpg")
    st.markdown("""
        <style>
        .overlay-text {
            position: absolute;
            top: 45%;
            width: 100%;
            text-align: center;
            font-size: 2.5rem;
            font-family: 'Playfair Display', serif;
            color: white;
            animation: fadein 2s;
        }
        @keyframes fadein {
            from {{ opacity: 0; }}
            to   {{ opacity: 1; }}
        }
        </style>
        <div class='overlay-text'>Simulated Boardroom</div>
    """, unsafe_allow_html=True)
    time.sleep(2.5)
    st.session_state.login_stage = "board"
    st.experimental_rerun()

# --- BOARD INTERVIEW PAGE ---
if st.session_state.authenticated and st.session_state.login_stage == "board":
    set_background("/mnt/data/board_interview.jpg")
    st.markdown("""
        <h1 style="text-align: center; margin-top: 2rem; font-size: 2.5rem; font-family: Playfair Display;">
            Welcome to the Interview
        </h1>
        <p style="text-align: center; margin-bottom: 3rem;">The Board will see you now.</p>
    """, unsafe_allow_html=True)

    with st.form("prep_form"):
        name = st.text_input("Your Name")
        occupation = st.text_input("Occupation")
        building = st.text_input("Target Building")
        traits = st.text_area("What three words describe you?")
        submit = st.form_submit_button("Submit")

    if submit:
        st.success("You're prepped, polished, and ready.")
        st.balloons()
