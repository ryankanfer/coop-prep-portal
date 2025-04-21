import streamlit as st
import base64

# --- IMAGE HELPERS ---
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

# --- LOGIN PAGE LAYOUT ---
def login_page():
    set_background("background.jpg")

    st.markdown("""
        <style>
        .login-container {
            background: rgba(0, 0, 0, 0.6);
            padding: 2rem;
            border-radius: 1rem;
            width: 400px;
            margin: 6rem auto;
            text-align: center;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(8px);
        }
        .login-container h1 {
            font-size: 1.8rem;
            color: white;
            margin-bottom: 0.5rem;
        }
        .login-container p {
            color: #ccc;
            margin-bottom: 2rem;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 0.5rem;
            border: none;
            font-size: 1rem;
        }
        .login-button {
            background-color: #5f6fd7;
            color: white;
            padding: 0.75rem;
            border: none;
            border-radius: 0.5rem;
            font-size: 1rem;
            width: 100%;
            margin-top: 1rem;
            cursor: pointer;
        }
        </style>
    
        <div class="login-container">
            <h1>NYC Co-op Interview Prep Assistant</h1>
            <p>The Board is Ready for You</p>
            <form action="" method="post">
                <input name="username" type="text" placeholder="Username"/>
                <input name="password" type="password" placeholder="Password"/>
                <input type="submit" class="login-button" value="Login"/>
            </form>
        </div>
    """, unsafe_allow_html=True)

    # --- Actual login logic ---
    if st.session_state.get("_submitted") is None:
        st.session_state._submitted = False

    submitted = st.experimental_get_query_params().get("submit", [None])[0]
    if submitted or st.session_state._submitted:
        st.session_state._submitted = True
        username = st.experimental_get_query_params().get("username", [""])[0]
        password = st.experimental_get_query_params().get("password", [""])[0]
        if username == "client" and password == "interviewready25":
            st.session_state.stage = "lobby"
            st.experimental_rerun()
        else:
            st.error("Invalid credentials. Try again or text Ryan directly for access.")

# --- INIT STATE ---
if "stage" not in st.session_state:
    st.session_state.stage = "login"

# --- ROUTING ---
if st.session_state.stage == "login":
    login_page()

# Note: Other stages like "intro", "lobby", "interview" will continue in the full app.py
