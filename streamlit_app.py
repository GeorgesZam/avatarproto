import streamlit as st
import pandas as pd
import time
import random
import subprocess
import sys
import os
import tempfile
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

        /* Main panel to improve contrast against the blue/white building background */
        .main-container {{
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem;
            box-shadow: 0 6px 18px rgba(11, 37, 69, 0.15);
        }}

        /* Panel text: dark color for good contrast */
        .panel-text {{
            color: #07213a;
            text-align: center;
            margin: 0.4rem 0;
        }}
        
        .stButton > button {{
            background: #0b67b2;
            color: white;
            border: none;
            padding: 0.7rem 1rem;
            border-radius: 8px;
            width: 100%;
            margin: 0.4rem 0;
        }}

        .stButton > button:hover {{
            background: #095fa0;
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
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="panel-text">🎯 PERSONALITY QUEST</h1>', unsafe_allow_html=True)

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
            st.markdown('<div class="main-container">', unsafe_allow_html=True)
            st.markdown(f'<h2 class="panel-text">Welcome {st.session_state.name}!</h2>', unsafe_allow_html=True)

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
                    st.markdown(f'<h3 class="panel-text">Question {current_q + 1}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<p class="panel-text">{question_text}</p>', unsafe_allow_html=True)

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
            st.markdown('<div class="main-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="panel-text">🎉 QUIZ COMPLETED!</h2>', unsafe_allow_html=True)

            if st.session_state.user_photo:
                st.image(st.session_state.user_photo, width=150)

            st.markdown(f'<h1 class="panel-text">{final_score}/20</h1>', unsafe_allow_html=True)
            st.markdown(f'<h3 class="panel-text">{personality_type}</h3>', unsafe_allow_html=True)
            st.markdown(f'<p class="panel-text">{personality_desc}</p>', unsafe_allow_html=True)

            # Restart and Play buttons
            if st.button("RESTART QUIZ"):
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.quiz_completed = False
                st.session_state.quiz_started = False
                st.rerun()

            if st.button("PLAY A GAME"):
                try:
                    # Write a minimal Panda3D script to disk
                    game_code = r"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LVector3
import sys

class MyApp(ShowBase):
    def __init__(self):
        super().__init__()
        # Simple scene: a rotating model if available; otherwise empty scene
        try:
            model = self.loader.loadModel('models/panda')
            model.reparentTo(self.render)
            model.setScale(0.5)
            model.setPos(0, 10, -1)
            self.taskMgr.add(self.spin, 'spinTask')
        except Exception:
            pass

    def spin(self, task):
        if self.render:
            self.render.setHpr(task.time * 30, 0, 0)
        return task.cont

if __name__ == '__main__':
    app = MyApp()
    app.run()
"""

                    game_path = Path(__file__).parent / 'panda_game.py'
                    with open(game_path, 'w', encoding='utf-8') as f:
                        f.write(game_code)

                    # Try launching the Panda3D script in background
                    subprocess.Popen([sys.executable, str(game_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    st.success('Le jeu a été lancé dans une fenêtre séparée (si Panda3D est installé).')
                    st.info('Remarque: Panda3D ouvrira une fenêtre native en dehors du navigateur; cela peut ne pas fonctionner dans certains environnements distants.')
                except Exception as e:
                    st.error(f"Impossible de lancer le jeu: {e}")

            st.markdown('</div>', unsafe_allow_html=True)
