import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="Shadow Point", layout="centered")
st.title("🌟 Shadow Point: Big/Small Predictor")

st.markdown("""
<style>
    .main {
        background-color: #0d1117;
        color: white;
        font-family: 'Courier New', monospace;
    }
    .stButton > button {
        background-color: #1f6feb;
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

outcomes = st.text_area("Enter Outcomes (B for Big, S for Small):", placeholder="Example: B S B B S S B ...")
outcome_list = outcomes.upper().strip().split()

prediction = ""
confidence = 0
skip = False

if len(outcome_list) >= 5:
    recent = outcome_list[-5:]
    counter = Counter(recent)
    most_common = counter.most_common()

    if most_common[0][1] >= 4:
        prediction = most_common[0][0]
        confidence = 90
    elif len(set(recent)) == 2 and recent[-1] != recent[-2]:
        prediction = recent[-1]
        confidence = 70
    elif recent.count("B") == 3 and recent.count("S") == 2:
        prediction = "S"
        confidence = 65
    elif recent.count("S") == 3 and recent.count("B") == 2:
        prediction = "B"
        confidence = 65
    else:
        skip = True

    # Recovery Logic: max 2 loss allowed
    if len(outcome_list) >= 7:
        last7 = outcome_list[-7:]
        win_count = sum([1 for i in range(1, len(last7)) if last7[i] == last7[i-1]])
        if win_count < 2:
            skip = False
            prediction = random.choice(["B", "S"])
            confidence = 60

if len(outcome_list) < 5:
    st.info("Enter at least 5 outcomes to get a prediction.")
elif skip:
    st.warning("No strong pattern detected. Suggest: SKIP")
else:
    st.success(f"Next Prediction: **{prediction}** | Confidence: **{confidence}%**")

st.markdown("---")
st.caption("Shadow Point v1 — Powered by Dodo AI")
