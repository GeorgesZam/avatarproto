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

else:
    questions_df = load_questions()
    
    if not st.session_state.quiz_started and not st.session_state.quiz_completed:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'<h2 class="panel-text">Welcome {st.session_state.name}!</h2>', unsafe_allow_html=True)

            if st.button("BEGIN QUIZ"):
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
                    st.markdown(f'<h3 class="panel-text">Question {current_q + 1}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<p class="panel-text">{question_text}</p>', unsafe_allow_html=True)

                    for i, option in enumerate(options):
                        if st.button(option, key=f"option_{i}"):
                            st.session_state.current_question += 1
                            st.session_state.score += random.randint(1, 5)
                            st.rerun()
            else:
                st.session_state.quiz_completed = True
                st.rerun()
    
    elif st.session_state.quiz_completed:
        celebrate_animation()
        final_score = min(20, st.session_state.score)
        personality_type, personality_desc = get_personality_type(final_score)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
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
                st.session_state.game_active = True
                st.rerun()

            if 'game_active' in st.session_state and st.session_state.game_active:
                # Appliquer un fond classique pour le jeu
                st.markdown(
                    """
                    <style>
                    .stApp {
                        background-image: none !important;
                        background-color: #f0f2f6 !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown("---")
                st.markdown('<h3 class="panel-text">🎮 3D Game</h3>', unsafe_allow_html=True)
                
                game_html = r"""
<canvas id="gameCanvas" style="display: block; margin: 0 auto; border: 2px solid #07213a; border-radius: 8px; width: 100%; max-width: 600px; height: 400px;"></canvas>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babylon.js/5.0.0/babylon.min.js"></script>
<script>
    const canvas = document.getElementById('gameCanvas');
    const engine = new BABYLON.Engine(canvas, true);
    const scene = new BABYLON.Scene(engine);
    
    // Camera
    const camera = new BABYLON.UniversalCamera('camera1', new BABYLON.Vector3(0, 5, -15));
    camera.attachControl(canvas, true);
    camera.speed = 0.15;
    
    // Light
    const light = new BABYLON.HemisphericLight('light1', new BABYLON.Vector3(1, 1, 1), scene);
    light.intensity = 0.8;
    
    // Sky
    scene.clearColor = new BABYLON.Color3(0.5, 0.7, 1);
    
    // Ground
    const ground = BABYLON.MeshBuilder.CreateGround('ground', {width: 50, height: 50}, scene);
    const groundMat = new BABYLON.StandardMaterial('groundMat', scene);
    groundMat.diffuse = new BABYLON.Color3(0.2, 0.8, 0.2);
    ground.material = groundMat;
    
    // Player (sphere)
    const player = BABYLON.MeshBuilder.CreateSphere('player', {diameter: 1}, scene);
    player.position.y = 1;
    const playerMat = new BABYLON.StandardMaterial('playerMat', scene);
    playerMat.diffuse = new BABYLON.Color3(1, 0.5, 0);
    player.material = playerMat;
    
    // Collectibles (small boxes)
    const collectibles = [];
    for (let i = 0; i < 5; i++) {
        const box = BABYLON.MeshBuilder.CreateBox('box' + i, {size: 0.5}, scene);
        box.position = new BABYLON.Vector3(Math.random() * 20 - 10, 1, Math.random() * 20 - 10);
        const boxMat = new BABYLON.StandardMaterial('boxMat' + i, scene);
        boxMat.diffuse = new BABYLON.Color3(Math.random(), Math.random(), Math.random());
        box.material = boxMat;
        collectibles.push(box);
    }
    
    // Keyboard input
    const keys = {};
    window.addEventListener('keydown', (e) => keys[e.key] = true);
    window.addEventListener('keyup', (e) => keys[e.key] = false);
    
    // Game loop
    engine.runRenderLoop(() => {
        if (keys['ArrowUp'] || keys['w']) player.position.z += 0.2;
        if (keys['ArrowDown'] || keys['s']) player.position.z -= 0.2;
        if (keys['ArrowLeft'] || keys['a']) player.position.x -= 0.2;
        if (keys['ArrowRight'] || keys['d']) player.position.x += 0.2;
        
        collectibles.forEach((box, idx) => {
            box.rotation.y += 0.01;
            if (BABYLON.Vector3.Distance(player.position, box.position) < 1.5) {
                box.dispose();
                collectibles.splice(idx, 1);
            }
        });
        
        scene.render();
    });
    
    window.addEventListener('resize', () => engine.resize());
</script>
                """
                st.components.v1.html(game_html, height=600)
                
                if st.button("Quitter le jeu"):
                    st.session_state.game_active = False
                    st.rerun()
