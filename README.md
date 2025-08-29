# 🧘 Mental Health Companion
https://mentalhealthcompanion-dkxfrogkdmgu52xceudusu.streamlit.app/

**Mental Health Companion** is an AI-powered web app that helps users understand, track, and manage their emotions in real time. It combines emotion detection, personalized coping strategies, and interactive mental wellness tools into a single platform.

---

## 🚀 Features

- **Emotion Analysis:**  
  Detects emotions from user input using a Hugging Face transformer model and visualizes them with bar charts and pie charts.

- **Personalized Coping Strategies:**  
  Suggests actionable strategies based on the top emotion detected (e.g., breathing exercises, journaling, grounding techniques).

- **Mental Health Toolkit:**  
  - **Breathing Exercise:** Guided 4-7-8 breathing with live progress bar.  
  - **Journaling Prompt:** Personalized prompts with saved entries and history tracking.

- **Emotion History & Trends:**  
  Tracks user emotion history and visualizes trends over time.

- **Future Scope:**  
  - Multilingual emotion detection  
  - Gamification (streaks, badges)  
  - Anonymous peer-to-peer community support  

---

## 🛠 Technology Stack

- **Frontend / Deployment:** Streamlit  
- **Machine Learning:** Hugging Face Transformers (`j-hartmann/emotion-english-distilroberta-base`)  
- **Data Processing & Visualization:** Pandas, Matplotlib, NumPy  
- **Backend (Model Execution):** PyTorch  

---

## ⚡ Getting Started

### Prerequisites
- Python >= 3.10

### Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/mental-health-companion.git
cd mental-health-companion

### Install dependencies
pip install -r requirements.txt


#Streamlit run
streamlit run app.py

