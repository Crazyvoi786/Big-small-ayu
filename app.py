import streamlit as st
from collections import deque, Counter
import random

st.set_page_config(page_title="Shadow Point AI", layout="centered")
st.title("🔮 Shadow Point – God-Level Big/Small Predictor")

st.markdown("""
<style>
.big-button button, .small-button button {
    width: 100%; height: 50px; font-size: 20px; font-weight: bold;
}
.pred-box {
    background: #111; color: #0f0; padding: 20px;
    border-radius: 12px; margin-top: 20px;
    font-size: 22px; font-weight: bold; text-align: center;
    box-shadow: 0 0 10px #0f0;
}
</style>
""", unsafe_allow_html=True)

# --- Session states ---
if "history" not in st.session_state:
    st.session_state.history = []
if "predictions" not in st.session_state:
    st.session_state.predictions = []
if "conf_level" not in st.session_state:
    st.session_state.conf_level = 0

# --- Add Outcome ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔵 BIG", use_container_width=True):
        st.session_state.history.append("B")
with col2:
    if st.button("🔴 SMALL", use_container_width=True):
        st.session_state.history.append("S")

# --- Show History ---
st.markdown("### 📜 Outcome History")
st.write(" ".join(st.session_state.history))

# --- Core Prediction Logic ---
def predict_next(history):
    if len(history) < 5:
        return ("WAIT", 0)

    recent = history[-10:]  # Last 10 for analysis
    patterns = {
        "BB": "S", "SS": "B",
        "BBB": "S", "SSS": "B",
        "BBBB": "S", "SSSS": "B",
        "BSBS": "B", "SBSB": "S",
        "BBS": "S", "SSB": "B",
        "BBBBB": "S", "SSSSS": "B",
        "BBBBBB": "S", "SSSSSS": "B",
    }

    for length in range(6, 1, -1):
        seq = "".join(recent[-length:])
        if seq in patterns:
            conf = int((length/6)*100)
            return patterns[seq], conf

    # Loss Recovery System (2-loss recovery)
    if len(history) >= 4:
        if history[-1] != history[-2] and history[-2] != history[-3]:
            return history[-1], 75

    return ("SKIP", 0)

# --- Predict Button ---
if st.button("⚡ Predict", type="primary"):
    result, conf = predict_next(st.session_state.history)
    st.session_state.predictions.append(result)
    st.session_state.conf_level = conf

# --- Show Prediction ---
if st.session_state.predictions:
    pred = st.session_state.predictions[-1]
    conf = st.session_state.conf_level
    if pred == "SKIP" or pred == "WAIT":
        st.markdown(f"<div class='pred-box'>⏳ {pred} – Not Enough Pattern</div>", unsafe_allow_html=True)
    else:
        emoji = "🔵" if pred == "B" else "🔴"
        label = "BIG" if pred == "B" else "SMALL"
        st.markdown(f"<div class='pred-box'>{emoji} Predict: {label}  – Confidence: {conf}%</div>", unsafe_allow_html=True)

# --- Reset ---
if st.button("🔁 Reset All"):
    st.session_state.history = []
    st.session_state.predictions = []
    st.session_state.conf_level = 0
