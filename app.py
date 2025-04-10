import streamlit as st
from collections import deque
import random

st.set_page_config(page_title="Shadow Point Predictor", layout="centered")
st.title("🔮 Shadow Point AI - Big/Small Prediction")
st.caption("Powered by Dodo | Focus: Big/Small Only | Advanced Trend Logic")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "loss_streak" not in st.session_state:
    st.session_state.loss_streak = 0

# Advanced pattern memory
pattern_memory = {
    ("B", "B"): "S",
    ("S", "S"): "B",
    ("B", "S"): "B",
    ("S", "B"): "S",
    ("B", "B", "B"): "S",
    ("S", "S", "S"): "B",
    ("B", "B", "S"): "B",
    ("S", "S", "B"): "S",
    ("B", "S", "B"): "S",
    ("S", "B", "S"): "B",
    ("B", "B", "B", "B"): "S",
    ("S", "S", "S", "S"): "B",
    ("B", "B", "B", "B", "B"): "S",
    ("S", "S", "S", "S", "S"): "B",
}

# Function to predict next outcome
def predict_next(history):
    for length in reversed(range(2, 6)):
        if len(history) >= length:
            recent = tuple(history[-length:])
            if recent in pattern_memory:
                return pattern_memory[recent], f"Pattern: {' → '.join(recent)} → {pattern_memory[recent]}"
    return "SKIP", "No strong pattern detected"

# Add outcome buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🟢 BIG"):
        st.session_state.history.append("B")
        prediction, reason = predict_next(st.session_state.history)
        if prediction == "B":
            st.session_state.loss_streak = 0
        elif prediction == "S":
            st.session_state.loss_streak += 1
with col2:
    if st.button("🔴 SMALL"):
        st.session_state.history.append("S")
        prediction, reason = predict_next(st.session_state.history)
        if prediction == "S":
            st.session_state.loss_streak = 0
        elif prediction == "B":
            st.session_state.loss_streak += 1

# Show prediction
if st.session_state.history:
    prediction, reason = predict_next(st.session_state.history)
    st.markdown(f"### 📌 Next Prediction: `{prediction}`")
    st.markdown(f"🧠 **Reason:** {reason}")
    st.markdown(f"🔥 **Loss Streak:** `{st.session_state.loss_streak}`")

# Show history
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 📜 Outcome History:")
    st.write(" → ".join(st.session_state.history))

# Reset button
if st.button("🔄 Reset History"):
    st.session_state.history = []
    st.session_state.loss_streak = 0
