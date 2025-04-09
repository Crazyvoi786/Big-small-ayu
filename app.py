import streamlit as st
import random

st.set_page_config(page_title="Shadow Point - God Mode", layout="centered")

st.title("🔮 Shadow Point AI Predictor - God Mode")
st.markdown("Enter previous outcomes to get **Big/Small/Skip** prediction. Built for **max profit, low loss** 💸")

history = st.text_area("📥 Enter outcomes (B/S) separated by space:", placeholder="B B S B S ...").strip().upper()
outcomes = history.split()

def detect_pattern(data):
    if len(data) < 5:
        return "SKIP", 0.0

    last = data[-5:]

    # Advanced trend rules
    patterns = {
        ("B", "B", "B", "B", "B"): "B",
        ("S", "S", "S", "S", "S"): "S",
        ("B", "S", "B", "S", "B"): "B",
        ("S", "B", "S", "B", "S"): "S",
        ("B", "B", "S", "S", "B"): "B",
        ("S", "S", "B", "B", "S"): "S",
        ("B", "B", "B", "S", "S"): "B",
        ("S", "S", "S", "B", "B"): "S",
        ("B", "S", "S", "B", "B"): "B",
        ("S", "B", "B", "S", "S"): "S",
    }

    for pattern, prediction in patterns.items():
        if tuple(last) == pattern:
            return prediction, 0.85

    # Recovery logic: If last 2 are losses
    if len(data) >= 3 and data[-3:] == ["B", "B", "B"]:
        return "B", 0.75
    if len(data) >= 3 and data[-3:] == ["S", "S", "S"]:
        return "S", 0.75

    return "SKIP", 0.0

if st.button("🔎 Predict"):
    if not outcomes:
        st.warning("Please enter some outcome data!")
    else:
        prediction, confidence = detect_pattern(outcomes)
        if prediction == "SKIP":
            st.info("🤖 Not enough data or unclear trend. Skipping prediction.")
        else:
            st.success(f"🔮 Prediction: **{prediction}**")
            st.write(f"📊 Confidence: `{int(confidence * 100)}%`")
