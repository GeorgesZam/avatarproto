import streamlit as st
import pandas as pd
import time
import random
from pathlib import Path
import base64
from PIL import Image

st.set_page_config(page_title="Personality Quest", layout="centered")

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def load_questions():
    try:
        csv_path = Path(__file__).parent / "quizz.csv"
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return pd.DataFrame()

def apply_clean_theme():
    logo_path = Path(__file__).parent / "logo.jpg"
    base64_logo = get_base64_image(logo_path)
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{base64_logo}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        .main-container {{
            background: rgba(0, 0, 0, 0.8);
            padding: 2rem;
            border-radius: 10px;
            margin: 1rem;
        }}
        
        .white-text {{
            color: white;
            text-align: center;
        }}
        
        .stButton > button {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 0.7rem 1rem;
            border-radius: 5px;
            width: 100%;
            margin: 0.2rem 0;
        }}
        
        .stButton > button:hover {{
            background: #45a049;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def celebrate_animation():
    st.balloons()

def get_personality_type(score):
    if score >= 16:
        return "The Visionary Leader", "You are a natural born leader!"
    elif score >= 12:
        return "The Creative Innovator", "Your imagination knows no bounds!"
    elif score >= 8:
        return "The Analytical Thinker", "You approach life with logic."
    else:
        return "The Supportive Collaborator", "You bring people together!"

if 'name' not in st.session_state:
    st.session_state.name = ""
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'user_photo' not in st.session_state:
    st.session_state.user_photo = None

apply_clean_theme()

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        
        
        name = st.text_input("Enter your name:")
        uploaded_photo = st.camera_input("Take a photo")
        
        if uploaded_photo:
            st.session_state.user_photo = Image.open(uploaded_photo)
        
        if st.button("START"):
            if name and name.strip():
                st.session_state.name = name.strip()
                st.session_state.logged_in = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    questions_df = load_questions()
    
    if not st.session_state.quiz_started and not st.session_state.quiz_completed:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'<h2 class="white-text">Welcome {st.session_state.name}!</h2>', unsafe_allow_html=True)
            
            if st.button("BEGIN QUIZ"):
                st.session_state.quiz_started = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.quiz_started and not st.session_state.quiz_completed:
        if len(questions_df) > 0:
            current_q = st.session_state.current_question
            
            if current_q < len(questions_df):
                question_row = questions_df.iloc[current_q]
                question_text = question_row.iloc[0]
                options = question_row.iloc[1:5].tolist()
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown('<div class="main-container">', unsafe_allow_html=True)
                    st.markdown(f'<h3 class="white-text">Question {current_q + 1}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<p class="white-text">{question_text}</p>', unsafe_allow_html=True)
                    
                    for i, option in enumerate(options):
                        if st.button(option, key=f"option_{i}"):
                            st.session_state.current_question += 1
                            st.session_state.score += random.randint(1, 5)
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.session_state.quiz_completed = True
                st.rerun()
    
    elif st.session_state.quiz_completed:
        celebrate_animation()
        final_score = min(20, st.session_state.score)
        personality_type, personality_desc = get_personality_type(final_score)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            
            st.markdown('<h2 class="white-text">🎉 QUIZ COMPLETED!</h2>', unsafe_allow_html=True)
            
            if st.session_state.user_photo:
                st.image(st.session_state.user_photo, width=150)
            
            st.markdown(f'<h1 class="white-text">{final_score}/20</h1>', unsafe_allow_html=True)
            st.markdown(f'<h3 class="white-text">{personality_type}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="white-text">{personality_desc}</p>', unsafe_allow_html=True)
            
            if st.button("RESTART QUIZ"):
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.quiz_completed = False
                st.session_state.quiz_started = False
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
