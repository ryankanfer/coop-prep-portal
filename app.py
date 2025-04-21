# app.py

import streamlit as st
import base64
import openai
import datetime
from fpdf import FPDF

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
        <h1 style='text-align: center;'>NYC Co-op Interview Prep Assistant</h1>
        <p style='text-align: center;'>The Board is Ready for You</p>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username.strip() == "client" and password == "interviewready25":
            st.session_state.stage = "lobby"
            st.rerun()
        else:
            st.error("Invalid credentials")

# --- PAGE 2: LOBBY ---
elif st.session_state.stage == "lobby":
    set_background("lobby.jpg")
    st.markdown("""
        <h1 style='text-align: center;'>Welcome to the Lobby</h1>
        <p style='text-align: center;'>The doorman will see you in now.</p>
    """, unsafe_allow_html=True)

    with st.form("lobby_form"):
        st.session_state.buyer["name"] = st.text_input("Your Name")
        st.session_state.buyer["occupation"] = st.text_input("Occupation")
        st.session_state.buyer["income"] = st.text_input("Income")
        st.session_state.buyer["assets"] = st.text_input("Assets (Cash in Bank)")
        st.session_state.buyer["building"] = st.text_input("Target Building")
        st.session_state.buyer["reason"] = st.selectbox("Reason for Purchase", ["Primary Residence", "Pied E Terre", "Gift"])
        st.session_state.buyer["intensity"] = st.radio("Board Intensity", ["Liberal", "Conservative"])
        st.session_state.buyer["work_type"] = st.radio("Type of Work", ["W2", "Self Employed"])
        st.session_state.buyer["pets"] = st.radio("Pets", ["Yes", "No"])
        submitted = st.form_submit_button("Enter Boardroom")

    if submitted:
        st.session_state.stage = "interview"
        st.rerun()

# --- PAGE 3: BOARD INTERVIEW ---
elif st.session_state.stage == "interview":
    set_background("board_interview.jpg")
    buyer = st.session_state.buyer

    def get_questions():
        return [
            {
                "member": "Evelyn Sharp",
                "question": f"Tell us why you're interested in {buyer['building']}.",
                "trigger": "building"
            },
            {
                "member": "Randy Gold",
                "question": f"As someone who is {buyer['work_type']}, how do you ensure financial stability month to month?",
                "trigger": "work_type"
            },
            {
                "member": "Evelyn Sharp",
                "question": f"What about your current income of {buyer['income']} gives you confidence to take this on?",
                "trigger": "income"
            },
            {
                "member": "Randy Gold",
                "question": f"Can you explain where your {buyer['assets']} in assets are currently held?",
                "trigger": "assets"
            },
            {
                "member": "Maya Patel",
                "question": f"Do you anticipate hosting often? What's your lifestyle like as a {buyer['occupation']}?",
                "trigger": "occupation"
            },
            {
                "member": "Evelyn Sharp",
                "question": f"The board has had mixed experiences with pets. You marked '{buyer['pets']}'. Can you clarify?",
                "trigger": "pets"
            }
        ]

    if "questions" not in st.session_state:
        st.session_state.questions = get_questions()

    st.markdown("""
        <h2 style='text-align: center;'>The Simulated Boardroom</h2>
        <p style='text-align: center;'>You've been granted a seat. Let's see how the conversation unfolds.</p>
    """, unsafe_allow_html=True)

    for idx, q in enumerate(st.session_state.questions):
        st.markdown(f"**{q['member']}:** {q['question']}")
        reply = st.text_area("Your Response:", key=f"reply_{idx}")
        st.session_state.responses[q['member'] + '_' + q['trigger']] = reply

        # Optional reactions
        if reply:
            st.markdown(f"*{q['member']} reacts:* Thank you, {buyer['name']}, that’s helpful.")

    st.markdown("<p style='text-align:center; color:#aaa;'>You're doing great.</p>", unsafe_allow_html=True)

    # --- FINAL CTA ---
    if st.button("Finish Interview & View Feedback"):
        from io import BytesIO

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
            pdf.set_text_color(50, 50, 50)
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
