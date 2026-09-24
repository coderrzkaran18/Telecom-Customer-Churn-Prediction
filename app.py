# ============================================================
#  TELCO CUSTOMER CHURN PREDICTOR – STREAMLIT WEB APP
#  AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026 | BharatCares
#  Author : [Karan Kumar Chauhan]
# ============================================================
#
#  HOW TO RUN
#  ----------
#  1. (Optional) Virtual environment banao:
#         python -m venv venv
#         venv\Scripts\activate          # Windows
#         source venv/bin/activate       # macOS / Linux
#
#  2. Dependencies install karo:
#         pip install -r requirements.txt
#
#  3. Dataset location confirm karo:
#         Telco_Churn_Data.csv  -->  project root folder mein hona chahiye
#
#  4. Pehle model train karo (sirf ek baar):
#         python EDA.py
#         python model_training.py
#         (ye dono models/ folder mein .pkl files banate hain)
#
#  5. App chalao:
#         streamlit run app.py
#
#  6. Browser mein khulega:
#         http://localhost:8501
# ============================================================

import os
import joblib
import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG  (Streamlit ka sabse pehla call hona chahiye)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Telco Churn Predictor",
    page_icon="📡",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────
# MODEL & METADATA LOAD
# @st.cache_resource = ek baar load ho, bar-bar nahi
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    """
    Saved scikit-learn pipeline aur feature metadata load karta hai.
    model_training.py run karne ke baad ye files banti hain:
      - models/best_churn_model.pkl  (full Pipeline: preprocessor + classifier)
      - models/feature_meta.pkl      (column names, cat/num split, model name)
    """
    pipeline = joblib.load(os.path.join("models", "best_churn_model.pkl"))
    meta     = joblib.load(os.path.join("models", "feature_meta.pkl"))
    return pipeline, meta

pipeline, meta   = load_artifacts()
FEATURE_COLS     = meta["feature_columns"]   # exact column order used at training time
MODEL_NAME       = meta["best_model_name"]

# ─────────────────────────────────────────────────────────────
# PREDICTION FUNCTION
# ─────────────────────────────────────────────────────────────
def predict_churn(user_input_dict: dict) -> tuple[str, float]:
    """
    Customer input dictionary se churn prediction karta hai.

    Parameters
    ----------
    user_input_dict : dict
        Keys = feature names (same as training), Values = user input

    Returns
    -------
    prediction  : str   – "Yes" (churn) ya "No" (loyal)
    probability : float – churn hone ki probability (0.0 – 1.0)
    """
    # Training wali exact column order mein DataFrame banao
    input_df   = pd.DataFrame([user_input_dict])[FEATURE_COLS]

    # Probability of class 1 (Churn = Yes)
    prob       = pipeline.predict_proba(input_df)[0][1]
    prediction = "Yes" if prob >= 0.5 else "No"
    return prediction, round(float(prob), 4)

# ─────────────────────────────────────────────────────────────
# SAMPLE INPUTS  (Quick-fill buttons ke liye)
# ─────────────────────────────────────────────────────────────
SAMPLE_CHURN = {                        # High-risk churner profile
    "gender"         : "Male",
    "SeniorCitizen"  : 1,
    "Partner"        : "No",
    "Dependents"     : "No",
    "tenure"         : 3,
    "PhoneService"   : "Yes",
    "MultipleLines"  : "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity" : "No",
}
SAMPLE_LOYAL = {                        # Loyal customer profile
    "gender"         : "Female",
    "SeniorCitizen"  : 0,
    "Partner"        : "Yes",
    "Dependents"     : "Yes",
    "tenure"         : 48,
    "PhoneService"   : "Yes",
    "MultipleLines"  : "Yes",
    "InternetService": "DSL",
    "OnlineSecurity" : "Yes",
}

# ─────────────────────────────────────────────────────────────
# SESSION STATE  (sample button press yaad rahe)
# ─────────────────────────────────────────────────────────────
if "sample" not in st.session_state:
    st.session_state.sample = None

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1 style='text-align:center; color:#3b82d4;'>📡 Telco Churn Predictor</h1>
    <p style='text-align:center; color:#57606a; font-size:15px;'>
        Fill in the customer details and see — will this customer 
        <b>churn</b> or <b>remain loyal</b>?
    </p>
    <hr style='border:1px solid #e5e7eb; margin-bottom:4px;'>
    """,
    unsafe_allow_html=True,
)
st.caption(f"🤖 Active Model: **{MODEL_NAME}**  |  Features used: **{len(FEATURE_COLS)}**")

# ─────────────────────────────────────────────────────────────
# QUICK-FILL BUTTONS
# ─────────────────────────────────────────────────────────────
st.markdown("#### 💡 Quick Fill")
btn_col1, btn_col2, btn_col3 = st.columns([1.2, 1.2, 1])

with btn_col1:
    if st.button("📋 Sample: Likely Churn", use_container_width=True):
        st.session_state.sample = "churn"
        st.rerun()
with btn_col2:
    if st.button("📋 Sample: Loyal Customer", use_container_width=True):
        st.session_state.sample = "loyal"
        st.rerun()
with btn_col3:
    if st.button("🔄 Reset Form", use_container_width=True):
        st.session_state.sample = None
        st.rerun()

# Active sample resolve karo
_S = (SAMPLE_CHURN if st.session_state.sample == "churn" else
      SAMPLE_LOYAL  if st.session_state.sample == "loyal"  else None)

def _v(key, default):
    """Active sample se value lo; warna default."""
    return _S[key] if (_S and key in _S) else default

st.markdown("<hr style='border:1px solid #e5e7eb;'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# INPUT FORM
# ─────────────────────────────────────────────────────────────
st.markdown("#### 📝 Customer Details")

with st.form("churn_form"):

    # ── Account Information ─────────────────────────────────
    st.markdown("**🗓️ Account Information**")
    a1, a2 = st.columns(2)
    with a1:
        tenure = st.slider(
            "Tenure (months)",
            min_value=0, max_value=72,
            value=_v("tenure", 12),
            help="Customer kitne mahine se company ke saath hai (0 = naya, 72 = purana)",
        )
    with a2:
        senior_raw    = st.selectbox(
            "Senior Citizen",
            options=["No (0)", "Yes (1)"],
            index=1 if _v("SeniorCitizen", 0) == 1 else 0,
            help="Customer 65+ saal ka hai?",
        )
        senior_citizen = 1 if senior_raw.startswith("Yes") else 0

    # ── Demographics ────────────────────────────────────────
    st.markdown("**👤 Demographics**")
    d1, d2, d3 = st.columns(3)
    with d1:
        gender = st.selectbox(
            "Gender",
            ["Male", "Female"],
            index=["Male", "Female"].index(_v("gender", "Male")),
        )
    with d2:
        partner = st.selectbox(
            "Partner",
            ["No", "Yes"],
            index=["No", "Yes"].index(_v("Partner", "No")),
            help="Customer ke saath partner/spouse hai?",
        )
    with d3:
        dependents = st.selectbox(
            "Dependents",
            ["No", "Yes"],
            index=["No", "Yes"].index(_v("Dependents", "No")),
            help="Customer ke saath dependents (bachche / parents) hain?",
        )

    # ── Phone Services ──────────────────────────────────────
    st.markdown("**📞 Phone Services**")
    p1, p2 = st.columns(2)
    with p1:
        phone_service = st.selectbox(
            "Phone Service",
            ["No", "Yes"],
            index=["No", "Yes"].index(_v("PhoneService", "Yes")),
        )
    with p2:
        ml_opts         = ["No", "No phone service", "Yes"]
        multiple_lines  = st.selectbox(
            "Multiple Lines",
            ml_opts,
            index=ml_opts.index(_v("MultipleLines", "No")),
        )

    # ── Internet Services ───────────────────────────────────
    st.markdown("**🌐 Internet Services**")
    i1, i2 = st.columns(2)
    with i1:
        inet_opts        = ["DSL", "Fiber optic", "No"]
        internet_service = st.selectbox(
            "Internet Service",
            inet_opts,
            index=inet_opts.index(_v("InternetService", "Fiber optic")),
        )
    with i2:
        sec_opts        = ["No", "No internet service", "Yes"]
        online_security = st.selectbox(
            "Online Security",
            sec_opts,
            index=sec_opts.index(_v("OnlineSecurity", "No")),
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Submit ──────────────────────────────────────────────
    submitted = st.form_submit_button(
        "🔍  Predict Churn",
        use_container_width=True,
        type="primary",
    )

# ─────────────────────────────────────────────────────────────
# RESULT DISPLAY
# ─────────────────────────────────────────────────────────────
if submitted:
    user_input = {
        "gender"         : gender,
        "SeniorCitizen"  : senior_citizen,
        "Partner"        : partner,
        "Dependents"     : dependents,
        "tenure"         : tenure,
        "PhoneService"   : phone_service,
        "MultipleLines"  : multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity" : online_security,
    }

    prediction, probability = predict_churn(user_input)
    prob_pct = probability * 100

    st.markdown("<hr style='border:1px solid #e5e7eb;'>", unsafe_allow_html=True)
    st.markdown("### 📊 Prediction Result")

    # ── Result Card ─────────────────────────────────────────
    if prediction == "Yes":
        st.markdown(
            f"""
            <div style='background:#fff1f0; border:2px solid #e05c5c;
                        border-radius:10px; padding:22px; text-align:center;'>
                <h2 style='color:#e05c5c; margin:0;'>⚠️ Churn Prediction: YES</h2>
                <p style='font-size:18px; margin:10px 0 0 0;'>
                    Churn Probability: <b>{prob_pct:.1f}%</b>
                </p>
                <p style='color:#57606a; margin:6px 0 0 0;'>
                    This customer could churn — take immediate retention action!
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style='background:#f0fff4; border:2px solid #22c55e;
                        border-radius:10px; padding:22px; text-align:center;'>
                <h2 style='color:#16a34a; margin:0;'>✅ Churn Prediction: NO</h2>
                <p style='font-size:18px; margin:10px 0 0 0;'>
                    Churn Probability: <b>{prob_pct:.1f}%</b>
                </p>
                <p style='color:#57606a; margin:6px 0 0 0;'>
                    This customer seems loyal — keep up the great service!
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Probability Bar ─────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**Churn Probability Meter: {prob_pct:.1f}%**")
    st.progress(probability)

    # ── Risk Level ──────────────────────────────────────────
    if prob_pct >= 70:
        st.error("🔴 HIGH RISK — Immediate retention action required!")
    elif prob_pct >= 40:
        st.warning("🟡 MEDIUM RISK — Monitor this customer closely.")
    else:
        st.success("🟢 LOW RISK — Customer is likely to stay.")

    # ── Input Summary (collapsible) ─────────────────────────
    with st.expander("📋 View Input Summary"):
        summary_df = pd.DataFrame(
            list(user_input.items()), columns=["Feature", "Value"]
        )
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <hr style='border:1px solid #e5e7eb; margin-top:48px;'>
    <p style='text-align:center; color:#57606a; font-size:12px;'>
        AICTE &nbsp;|&nbsp;
        IBM SkillsBuild Data Analytics with AI Internship 2026 &nbsp;|&nbsp;
        BharatCares &nbsp;|&nbsp;
        Telco Churn Predict Project &nbsp;|&nbsp;
    </p>
    """,
    unsafe_allow_html=True,
)
