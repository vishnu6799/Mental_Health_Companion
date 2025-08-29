import streamlit as st
import pandas as pd
from transformers import pipeline
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Mental Health Companion", page_icon="🧠", layout="wide")

# Patch for transformers expecting typeDict (fix numpy issue)
if not hasattr(np, "typeDict"):
    np.typeDict = np.sctypeDict

# -----------------------------
# Load Hugging Face Emotion Model
# -----------------------------
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=True
    )

emotion_model = load_model()

# -----------------------------
# Analyze Emotions
# -----------------------------
def analyze_emotions(text):
    results = emotion_model(text)[0]
    emotions = {r["label"]: r["score"] for r in results}
    return emotions

# -----------------------------
# Personalized Coping Strategies
# -----------------------------
def get_personalized_strategies(emotions):
    top_emotion = max(emotions, key=emotions.get)
    strategies = {
        "joy": [
            "✨ Write down what made you happy today.",
            "🎶 Celebrate with your favorite song.",
            "📸 Capture this moment in a photo or note."
        ],
        "sadness": [
            "✍️ Try journaling your thoughts.",
            "📞 Call a close friend or family member.",
            "🌳 Step outside for fresh air or a short walk."
        ],
        "anger": [
            "🌬️ Do a quick 4-7-8 breathing cycle.",
            "🚶 Take a short walk to release tension.",
            "🙏 Write down 3 things you are grateful for."
        ],
        "fear": [
            "👀 Try grounding: name 3 things you see around you.",
            "🧘 Practice a 2-min meditation.",
            "💡 Read an uplifting quote or mantra."
        ],
        "surprise": [
            "🎨 Channel your energy into something creative.",
            "📔 Write about what surprised you.",
            "😊 Share the surprise with someone close."
        ],
        "disgust": [
            "🎶 Listen to music you enjoy.",
            "🏋️‍♂️ Try light exercise to shift focus.",
            "📝 Reframe the situation with a positive angle."
        ],
        "neutral": [
            "🙏 Write a short gratitude journal.",
            "📚 Read a book or article you like.",
            "🌿 Enjoy a mindful tea/coffee break."
        ]
    }
    return strategies.get(top_emotion, ["💤 Take a short break, drink water, and relax."])

# -----------------------------
# Toolkit Features
# -----------------------------
def breathing_exercise():
    st.subheader("🌬️ Breathing Exercise (4-7-8)")
    st.write("Follow the guided cycle below ⬇️")

    if st.button("Start Breathing Cycle"):
        phases = [("Inhale", 4, "🔵"), ("Hold", 7, "🟡"), ("Exhale", 8, "🟢")]
        progress = st.progress(0)
        text_placeholder = st.empty()

        total_time = sum([p[1] for p in phases])
        elapsed = 0

        for phase, duration, symbol in phases:
            for t in range(duration, 0, -1):
                text_placeholder.markdown(f"### {symbol} {phase}... {t}s")
                elapsed += 1
                progress.progress(elapsed / total_time)
                time.sleep(1)

        text_placeholder.success("✅ Cycle Complete! Feel free to repeat.")

def journaling_prompt():
    prompts = [
        "What are 3 things you are grateful for today?",
        "Write about a small victory you had recently.",
        "What’s one worry you can let go of right now?",
        "Write a letter to your future self."
    ]
    st.subheader("✍️ Journaling Prompt")
    prompt = random.choice(prompts)
    st.info(prompt)

    journal_entry = st.text_area("Your Journal Entry:", placeholder="Start writing here...")

    if st.button("Save Journal Entry"):
        if "journal" not in st.session_state:
            st.session_state.journal = []
        st.session_state.journal.append({"prompt": prompt, "entry": journal_entry})
        st.success("✅ Entry saved!")

        # Show past entries
        st.write("### 📔 Your Journal Entries")
        for idx, j in enumerate(st.session_state.journal[::-1], 1):
            st.markdown(f"**{idx}. Prompt:** {j['prompt']}")
            st.write(f"✍️ {j['entry']}")
            st.markdown("---")

def crisis_support(emotions):
    if emotions.get("sadness", 0) > 0.8:
        st.error("⚠️ It seems you’re feeling very low. Please consider reaching out to a helpline or trusted person.")

# -----------------------------
# UI Layout
# -----------------------------
st.title("🧘 Mental Health Companion")
st.write("Type how you feel and get instant insights + well-being tools.")

user_input = st.text_area("How are you feeling today?", placeholder="e.g. I feel nervous and can't sleep well.")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Analyze"):
    if user_input.strip():
        emotions = analyze_emotions(user_input)
        strategies = get_personalized_strategies(emotions)

        # Save history
        st.session_state.history.append({"text": user_input, **emotions})

        # Results
        st.subheader("📊 Emotion Analysis")
        df = pd.DataFrame(list(emotions.items()), columns=["Emotion", "Score"])
        st.bar_chart(df.set_index("Emotion"))

        st.subheader("💡 Personalized Coping Strategies")
        for s in strategies:
            st.success(s)

        crisis_support(emotions)

# -----------------------------
# History & Trends
# -----------------------------
if st.session_state.history:
    st.subheader("📝 Your Emotion History")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)

    st.subheader("📈 Trends Over Time")
    st.line_chart(history_df.drop(columns=["text"]))
   
    st.subheader("🥧 Overall Emotion Distribution")
    emotion_means = history_df.drop(columns=["text"]).mean()

    fig, ax = plt.subplots(figsize=(2, 2))
    ax.pie(
        emotion_means,
        labels=emotion_means.index,
        autopct='%1.1f%%',
        textprops={'fontsize': 6},
        radius=1.6 
    )
    st.pyplot(fig, use_container_width=False) 
    

   

# -----------------------------
# Mental Health Toolkit
# -----------------------------
st.markdown("---")
st.header("🧰 Mental Health Toolkit")

col1, col2 = st.columns(2)
with col1:
    breathing_exercise()
with col2:
    journaling_prompt()

# -----------------------------
# Future Scope
# -----------------------------
with st.expander("🚀 Future Scope"):
    st.write("""
    - **Multilingual Emotion Detection** 🌍 for inclusivity.  
    - **Gamification** 🎮 (reward streaks, badges).  
    - **Community Support** 🤝 (anonymous peer-to-peer sharing).  
    """)
