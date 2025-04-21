
# app.py

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
            background-repeat: no-repeat;
        }}
        .glass-box {{
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(14px);
            border-radius: 20px;
            padding: 2rem;
            margin: 3vh auto;
            width: 90%;
            max-width: 700px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }}
        h1, h2, h3 {{
            font-family: 'Playfair Display', serif !important;
        }}
        .stTextInput > div > input,
        .stTextArea > div > textarea {{
            background-color: rgba(255,255,255,0.12);
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.3);
            color: #ffffff;
            font-size: 16px;
        }}
        label {{
            font-weight: bold;
            font-size: 1rem;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- SESSION INIT ---
if "stage" not in st.session_state:
    st.session_state.stage = "login"
if "buyer" not in st.session_state:
    st.session_state.buyer = {}
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --- PAGE: LOGIN ---
if st.session_state.stage == "login":
    set_background("background.jpg")
    with st.container():
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>NYC Co-op Interview Prep Assistant</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>The Board is Ready for You</h3>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username.strip() == "client" and password == "interviewready25":
                st.session_state.stage = "landing"
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE: LANDING EXPLANATION ---
elif st.session_state.stage == "landing":
    set_background("background.jpg")
    with st.container():
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<h2>Welcome to the simulation.</h2>", unsafe_allow_html=True)
        st.markdown("""
        Buying into a co-op in NYC? You’re not just buying a home — you’re buying shares in a corporation. And that corporation has a board that acts less like management… and more like a tight-knit neighborhood deciding if they want you at their block party.

        They’ve seen your application. They’ve reviewed your financials.
        But now? They want to see if you fit in.

        This app is your prep concierge.

        You’ll enter a simulation modeled on actual co-op board interviews.
        Expect questions about your money, lifestyle, pets, and how you plan to use the apartment. How you answer shapes how the board reacts.

        No paperwork. No pressure.
        Just you, the board, and a little friendly judgment.

        When you're ready, the doorman will walk you into the lobby.
        """)
        if st.button("Enter Lobby"):
            st.session_state.stage = "lobby"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE: LOBBY FORM ---
elif st.session_state.stage == "lobby":
    set_background("lobby.jpg")
    with st.form("lobby_form"):
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.markdown("<h2>Fill in Your Details</h2>", unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            st.session_state.buyer["name"] = st.text_input("Your Name")
            st.session_state.buyer["occupation"] = st.text_input("Occupation")
            st.session_state.buyer["income"] = st.text_input("Income")
            st.session_state.buyer["work_type"] = st.radio("Type of Work", ["W2", "Self Employed"])
        with cols[1]:
            st.session_state.buyer["assets"] = st.text_input("Assets (Cash in Bank)")
            st.session_state.buyer["building"] = st.text_input("Target Building")
            st.session_state.buyer["reason"] = st.selectbox("Reason for Purchase", ["Primary Residence", "Pied E Terre", "Gift"])
        st.session_state.buyer["intensity"] = st.radio("Board Intensity", ["Liberal", "Conservative"])
        st.session_state.buyer["pets"] = st.radio("Pets", ["Yes", "No"])
        submitted = st.form_submit_button("Enter Boardroom")
        st.markdown("</div>", unsafe_allow_html=True)
    if submitted:
        st.session_state.stage = "interview"
        st.rerun()

# --- PAGE: BOARD INTERVIEW ---
elif st.session_state.stage == "interview":
    set_background("board_interview.jpg")
    buyer = st.session_state.buyer

    def get_questions():
        return [
            {"member": "Evelyn Sharp", "question": f"Tell us why you're interested in {buyer['building']}.", "trigger": "building"},
            {"member": "Randy Gold", "question": f"As someone who is {buyer['work_type']}, how do you ensure financial stability month to month?", "trigger": "work_type"},
            {"member": "Evelyn Sharp", "question": f"What about your income of {buyer['income']} gives you confidence?", "trigger": "income"},
            {"member": "Randy Gold", "question": f"Can you explain where your {buyer['assets']} in assets are held?", "trigger": "assets"},
            {"member": "Maya Patel", "question": f"Do you anticipate hosting often? What's your lifestyle like as a {buyer['occupation']}?", "trigger": "occupation"},
            {"member": "Evelyn Sharp", "question": f"The board has had mixed experiences with pets. You marked '{buyer['pets']}'. Can you clarify?", "trigger": "pets"}
        ]

    if "questions" not in st.session_state:
        st.session_state.questions = get_questions()

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("<h2>The Simulated Boardroom</h2>", unsafe_allow_html=True)

    for idx, q in enumerate(st.session_state.questions):
        st.markdown(f"**{q['member']}:** {q['question']}")
        reply = st.text_area("Your Response:", key=f"reply_{idx}")
        st.session_state.responses[q['member'] + '_' + q['trigger']] = reply
        if reply:
            st.markdown(f"*{q['member']} reacts:* {buyer['name']}, noted.")

    if st.button("Finish Interview & View Feedback"):
        def generate_feedback_pdf(name, responses):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            pdf.cell(0, 10, f"Board Interview Feedback for {name}", ln=True)
            pdf.ln(5)
            for idx, (key, answer) in enumerate(responses.items(), start=1):
                member, topic = key.split('_')
                question_text = next((q["question"] for q in st.session_state.questions if q["member"] == member and q["trigger"] == topic), None)
                if question_text:
                    pdf.multi_cell(0, 10, f"Q{idx}: {question_text}\nA: {answer}\n")
            pdf.ln(5)
            pdf.set_font("Helvetica", style='I', size=11)
            pdf.cell(0, 10, "Final Note: Welcome home.", ln=True)
            output = BytesIO()
            pdf.output(output, 'F')
            output.seek(0)
            return output

        pdf_file = generate_feedback_pdf(buyer['name'], st.session_state.responses)
        st.balloons()
        st.success(f"Board review complete. Welcome home, {buyer['name']}.")
        st.download_button(
            label="📥 Download Board Summary",
            data=pdf_file.getvalue(),
            file_name=f"{buyer['name'].replace(' ', '_')}_Board_Feedback.pdf",
            mime="application/pdf"
        )
    st.markdown("</div>", unsafe_allow_html=True)
