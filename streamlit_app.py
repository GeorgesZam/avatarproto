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

def apply_background():
    logo_path = Path(__file__).parent / "logo.jpg"
    base64_logo = get_base64_image(logo_path)
    
    if base64_logo:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{base64_logo}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def celebrate_animation():
    st.balloons()
    time.sleep(0.5)

def get_personality_type(score):
    if score >= 16:
        return "The Visionary Leader", "You are a natural born leader with big ideas!"
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

apply_background()

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: white;'>🎯 PERSONALITY QUEST</h1>", unsafe_allow_html=True)
        
        name = st.text_input("Enter your name:", key="name_input")
        uploaded_photo = st.camera_input("Take a photo")
        
        if uploaded_photo:
            st.session_state.user_photo = Image.open(uploaded_photo)
        
        if st.button("🚀 Start", use_container_width=True):
            if name and name.strip():
                st.session_state.name = name.strip()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter your name to continue!")

else:
    questions_df = load_questions()
    
    if not st.session_state.quiz_started and not st.session_state.quiz_completed:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"<h2 style='text-align: center; color: white;'>Welcome, {st.session_state.name}! 🌟</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: white;'>Ready to discover your personality?</p>", unsafe_allow_html=True)
            
            if st.button("🎯 Start Quiz", use_container_width=True):
                st.session_state.quiz_started = True
                st.rerun()
    
    elif st.session_state.quiz_started and not st.session_state.quiz_completed:
        if len(questions_df) > 0:
            current_q = st.session_state.current_question
            
            if current_q < len(questions_df):
                question_row = questions_df.iloc[current_q]
                question_text = question_row.iloc[0]
                options = question_row.iloc[1:5].tolist()
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    # Afficher d'abord les boutons
                    for i, option in enumerate(options):
                        if st.button(option, key=f"option_{current_q}_{i}", use_container_width=True):
                            st.session_state.current_question += 1
                            st.session_state.score += random.randint(1, 5)
                            st.rerun()
                    
                    # Ensuite afficher la question avec animation
                    st.markdown(f"<h2 style='text-align: center; color: white;'>Question {current_q + 1}</h2>", unsafe_allow_html=True)
                    
                    # Animation typewriter pour la question
                    placeholder = st.empty()
                    displayed_text = ""
                    for char in question_text:
                        displayed_text += char
                        placeholder.markdown(f"<div style='color: white; font-size: 1.2em; text-align: center;'>{displayed_text}</div>", unsafe_allow_html=True)
                        time.sleep(0.03)
            else:
                st.session_state.quiz_completed = True
                st.rerun()
    
    elif st.session_state.quiz_completed:
        celebrate_animation()
        final_score = min(20, st.session_state.score)
        personality_type, personality_desc = get_personality_type(final_score)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center; color: white;'>🎉 Quiz Completed!</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: white;'>Your Personality Results</h2>", unsafe_allow_html=True)
            
            if st.session_state.user_photo:
                st.image(st.session_state.user_photo, width=200)
            
            st.markdown(f"<h1 style='text-align: center; color: gold;'>{final_score}/20</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: lightblue;'>{personality_type}</h2>", unsafe_allow_html=True)
            
            # Animation pour la description
            desc_placeholder = st.empty()
            displayed_desc = ""
            for char in personality_desc:
                displayed_desc += char
                desc_placeholder.markdown(f"<p style='text-align: center; color: white;'>{displayed_desc}</p>", unsafe_allow_html=True)
                time.sleep(0.03)
            
            st.markdown(f"""
            <div style='background: rgba(100,100,255,0.3); padding: 20px; border-radius: 10px; margin: 20px 0;'>
                <h4 style='color: white; text-align: center;'>Your Journey Summary</h4>
                <p style='color: white; text-align: center;'>Completed {len(questions_df)} questions • Score: {final_score} • {personality_type}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Restart Quiz", use_container_width=True):
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.quiz_completed = False
                st.session_state.quiz_started = False
                st.rerun()
