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

def apply_dark_theme():
    logo_path = Path(__file__).parent / "logo.jpg"
    base64_logo = get_base64_image(logo_path)
    
    background_style = f"""
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_logo}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    """ if base64_logo else """
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%) !important;
    }
    """
    
    st.markdown(
        f"""
        <style>
        /* Reset Streamlit defaults */
        .stApp {{
            background-color: transparent !important;
        }}
        
        .main .block-container {{
            background-color: transparent !important;
        }}
        
        {background_style}
        
        /* Global text color */
        .stApp, .stMarkdown, .stText {{
            color: #ffffff !important;
        }}
        
        /* Container styling */
        .dark-container {{
            background: rgba(0, 0, 0, 0.85) !important;
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            margin: 1rem 0;
        }}
        
        /* Button styling */
        .stButton > button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.8rem 1.5rem !important;
            font-weight: 600 !important;
            width: 100% !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
        }}
        
        /* Input styling */
        .stTextInput > div > div > input {{
            background: rgba(255,255,255,0.1) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }}
        
        /* Camera input */
        .stCameraInput > div {{
            background: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 10px !important;
        }}
        
        /* Text elements */
        .dark-title {{
            color: #ffffff !important;
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }}
        
        .dark-subtitle {{
            color: #cccccc !important;
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }}
        
        .dark-question {{
            color: #ffffff !important;
            font-size: 1.3rem;
            text-align: center;
            margin: 1rem 0;
            line-height: 1.5;
        }}
        
        .dark-score {{
            color: #ffd700 !important;
            font-size: 3rem;
            text-align: center;
            font-weight: bold;
        }}
        
        .dark-personality {{
            color: #66ccff !important;
            font-size: 1.8rem;
            text-align: center;
            font-weight: bold;
            margin: 1rem 0;
        }}
        
        /* Summary box */
        .dark-summary {{
            background: rgba(100,100,255,0.2) !important;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid rgba(100,100,255,0.3);
            margin: 1rem 0;
        }}
        
        /* Force dark background for all containers */
        div[data-testid="stVerticalBlock"] > div {{
            background-color: transparent !important;
        }}
        
        /* Remove any white backgrounds */
        .element-container, .stMarkdown, .stButton {{
            background-color: transparent !important;
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
        return "The Visionary Leader", "You are a natural born leader with big ideas and the drive to make them happen!"
    elif score >= 12:
        return "The Creative Innovator", "Your imagination knows no bounds and you see possibilities everywhere!"
    elif score >= 8:
        return "The Analytical Thinker", "You approach life with logic and careful consideration."
    else:
        return "The Supportive Collaborator", "You thrive in teams and bring people together with your empathy!"

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

apply_dark_theme()

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="dark-container">', unsafe_allow_html=True)
        st.markdown('<div class="dark-title">🎯 PERSONALITY QUEST</div>', unsafe_allow_html=True)
        st.markdown('<div class="dark-subtitle">Discover Your True Self</div>', unsafe_allow_html=True)
        
        name = st.text_input("**Enter your name:**", key="name_input")
        uploaded_photo = st.camera_input("**Take a photo for your profile**")
        
        if uploaded_photo:
            st.session_state.user_photo = Image.open(uploaded_photo)
        
        if st.button("🚀 Start Your Journey", use_container_width=True):
            if name and name.strip():
                st.session_state.name = name.strip()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter your name to continue!")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    questions_df = load_questions()
    
    if not st.session_state.quiz_started and not st.session_state.quiz_completed:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="dark-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="dark-title">Welcome, {st.session_state.name}! 🌟</div>', unsafe_allow_html=True)
            st.markdown('<div class="dark-subtitle">Ready to uncover your unique personality traits?</div>', unsafe_allow_html=True)
            
            if st.button("🎯 Begin Personality Test", use_container_width=True):
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
                    st.markdown('<div class="dark-container">', unsafe_allow_html=True)
                    
                    # Afficher d'abord les boutons
                    for i, option in enumerate(options):
                        if st.button(option, key=f"option_{current_q}_{i}", use_container_width=True):
                            st.session_state.current_question += 1
                            st.session_state.score += random.randint(1, 5)
                            st.rerun()
                    
                    # Ensuite afficher la question avec animation
                    st.markdown(f'<div class="dark-title">Question {current_q + 1}</div>', unsafe_allow_html=True)
                    
                    # Animation typewriter pour la question
                    placeholder = st.empty()
                    displayed_text = ""
                    for char in question_text:
                        displayed_text += char
                        placeholder.markdown(f'<div class="dark-question">{displayed_text}</div>', unsafe_allow_html=True)
                        time.sleep(0.03)
                    
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
            st.markdown('<div class="dark-container">', unsafe_allow_html=True)
            st.markdown('<div class="dark-title">🎉 Quiz Completed!</div>', unsafe_allow_html=True)
            st.markdown('<div class="dark-subtitle">Your Personality Results</div>', unsafe_allow_html=True)
            
            if st.session_state.user_photo:
                st.image(st.session_state.user_photo, width=200)
            
            st.markdown(f'<div class="dark-score">{final_score}/20</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="dark-personality">{personality_type}</div>', unsafe_allow_html=True)
            
            # Animation pour la description
            desc_placeholder = st.empty()
            displayed_desc = ""
            for char in personality_desc:
                displayed_desc += char
                desc_placeholder.markdown(f'<div class="dark-question">{displayed_desc}</div>', unsafe_allow_html=True)
                time.sleep(0.03)
            
            st.markdown(f'''
            <div class="dark-summary">
                <h4 style="color: white !important; text-align: center; margin-bottom: 1rem;">Your Journey Summary</h4>
                <p style="color: #cccccc !important; text-align: center; margin: 0;">
                    Completed {len(questions_df)} questions • Score: {final_score} • {personality_type}
                </p>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("🔄 Take Test Again", use_container_width=True):
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.quiz_completed = False
                st.session_state.quiz_started = False
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
