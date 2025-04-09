import streamlit as st

st.set_page_config(page_title="Shadow Point Predictor", layout="centered")

st.title("🔮 Shadow Point: Big/Small Predictor")
st.markdown("Focus: **Manual Outcome Input** → AI Pattern → Next Prediction")

# --- SESSION STORAGE ---
if "history" not in st.session_state:
    st.session_state.history = []

if "loss_streak" not in st.session_state:
    st.session_state.loss_streak = 0

# --- INPUT ---
outcome = st.text_input("Enter last outcome (B/S):", max_chars=1).upper()
submit = st.button("Submit")

# --- TREND RULES ---
def predict_next(history):
    if len(history) < 3:
        return "SKIP", "Not enough data"

    recent = "".join(history[-6:])

    # Common trend patterns
    if recent.endswith("BB"):
        return "S", "Pattern: BB → S"
    if recent.endswith("SS"):
        return "B", "Pattern: SS → B"
    if recent.endswith("BSBS") or recent.endswith("SBSB"):
        return "SKIP", "Zigzag detected"
    if recent.endswith("BBB"):
        return "S", "Pattern: BBB → S"
    if recent.endswith("SSS"):
        return "B", "Pattern: SSS → B"
    if recent.endswith("BBBB") or recent.endswith("SSSS"):
        return history[-1], "Long trend → Follow same"
    
    # Default fallback
    return "SKIP", "No clear pattern"

# --- SUBMIT LOGIC ---
if submit and outcome in ["B", "S"]:
    st.session_state.history.append(outcome)

    prediction, reason = predict_next(st.session_state.history)

    last = st.session_state.history[-1]
    if len(st.session_state.history) >= 2:
        prev_pred, _ = predict_next(st.session_state.history[:-1])
        if prev_pred == last:
            st.session_state.loss_streak = 0
        elif prev_pred in ["B", "S"]:
            st.session_state.loss_streak += 1

    # Show prediction
    st.markdown(f"### 📌 Next Prediction: `{prediction}`")
    st.markdown(f"🧠 **Reason:** {reason}")
    st.markdown(f"🔥 **Loss Streak:** {st.session_state.loss_streak}")

    # Recovery advice
    if st.session_state.loss_streak >= 2:
        st.warning("⚠️ Multiple losses detected. Use caution or wait for trend clarity.")

# --- DISPLAY HISTORY ---
if st.session_state.history:
    st.markdown("#### 📜 Outcome History")
    st.code(" → ".join(st.session_state.history), language="text")

# --- RESET BUTTON ---
if st.button("Reset History"):
    st.session_state.history = []
    st.session_state.loss_streak = 0
    st.success("History Cleared")
