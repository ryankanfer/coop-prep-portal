import streamlit as st
import base64
import openai
import time
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="NYC Co-op Interview Prep", layout="centered")
st.session_state.setdefault("stage", "login")

# --- BACKGROUND SETUP ---
def get_base64_image(img_path):
    with open(img_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def set_background(image_path):
    b64_img = get_base64_image(image_path)
    st.markdown(f"""
    <style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&display=swap');
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
}

    .stApp {{
        background-image: url("data:image/jpg;base64,{b64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- TIPS ---
TIPS = [
    "\ud83e\udde0 Know your debt-to-income ratio.",
    "\ud83d\udcc8 Be prepared to explain any large financial gifts.",
    "\ud83d\udcbc Dress like you're already on the board.",
    "\ud83c\udfe0 Know the building rules and pet policies."
]

# --- OPENAI SETUP ---
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_board_questions(name, building):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're an elite NYC broker simulating a co-op board interview."},
            {"role": "user", "content": f"Prepare 5 tailored co-op board questions for a buyer named {name} applying to {building}. Make them feel real, specific, and intimidating-but-fair."}
        ]
    )
    return response.choices[0].message.content

# --- PAGE: LOGIN ---
if st.session_state.stage == "login":
    set_background("/mnt/data/background.jpg")
    st.markdown("""
        <h1 style='text-align: center; color: white;'>NYC Co-op Interview<br>Prep Assistant</h1>
        <p style='text-align: center; color: white;'>The Board is Ready for You</p>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    st.markdown(f"""
    <div style='text-align: center; font-size: 1.1rem; color: #eee; margin-top: 1rem;'>
        {TIPS[datetime.now().second % len(TIPS)]}
    </div>
    """, unsafe_allow_html=True)

    if login_btn and username.strip() == "client" and password == "interviewready25":
        with st.spinner("Opening simulated boardroom..."):
            time.sleep(2.5)
            st.session_state.stage = "lobby"
            st.rerun()
    elif login_btn:
        st.error("Invalid credentials.")

# --- PAGE: LOBBY INPUT ---
elif st.session_state.stage == "lobby":
    set_background("/mnt/data/lobby.jpg")
    st.markdown("""
        <h2 style='text-align: center; color: white;'>Welcome to the Lobby</h2>
        <p style='text-align: center; color: white;'>The doorman will see you in now.</p>
    """, unsafe_allow_html=True)

    with st.form("info_form"):
        name = st.text_input("Your Name")
        building = st.text_input("Target Building")
        go_btn = st.form_submit_button("Enter Boardroom")

    if go_btn and name and building:
        with st.spinner("Doors opening..."):
            st.session_state.name = name
            st.session_state.building = building
            st.session_state.stage = "interview"
            time.sleep(1.5)
            st.rerun()

# --- PAGE: INTERVIEW ---
elif st.session_state.stage == "interview":
    set_background("/mnt/data/board_interview.jpg")
    st.markdown("""
        <h2 style='text-align: center; color: white;'>The Interview Begins</h2>
        <p style='text-align: center; color: white;'>Your responses will determine your fate.</p>
    """, unsafe_allow_html=True)

    if "questions" not in st.session_state:
        with st.spinner("The board is reviewing your file..."):
            st.session_state.questions = generate_board_questions(
                st.session_state.name, st.session_state.building
            )

    st.markdown(f"""
    <div style='background: rgba(0,0,0,0.55); padding: 1.5rem; border-radius: 12px; color: white;'>
    <h4>Questions for {st.session_state.name} at {st.session_state.building}:</h4>
    <pre style='white-space: pre-wrap;'>{st.session_state.questions}</pre>
    </div>
    """, unsafe_allow_html=True)
