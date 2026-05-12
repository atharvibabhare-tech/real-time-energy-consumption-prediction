import streamlit as st
import pickle
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Energy Consumption Prediction",
    page_icon="⚡",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================
model = pickle.load(open("model.pkl", "rb"))

# =========================
# CUSTOM CSS — Light Blue Theme
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --blue-50:  #EFF6FF;
    --blue-100: #DBEAFE;
    --blue-200: #BFDBFE;
    --blue-300: #93C5FD;
    --blue-400: #60A5FA;
    --blue-500: #3B82F6;
    --blue-600: #2563EB;
    --blue-700: #1D4ED8;
    --text-dark: #1E3A5F;
    --text-mid:  #3B5998;
    --text-soft: #6B8DC4;
    --white:     #FFFFFF;
    --shadow:    0 4px 24px rgba(59,130,246,0.10);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Background */
.stApp {
    background: linear-gradient(160deg, #EFF6FF 0%, #DBEAFE 50%, #EFF6FF 100%) !important;
    min-height: 100vh;
}

#MainMenu, footer { visibility: hidden; }
.block-container { padding: 2rem 3rem 3rem !important; max-width: 1100px; }

/* ---- HERO ---- */
.hero {
    background: linear-gradient(135deg, #2563EB 0%, #60A5FA 100%);
    border-radius: 20px;
    padding: 2.8rem 3rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(37,99,235,0.25);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "⚡";
    position: absolute;
    font-size: 12rem;
    opacity: 0.06;
    right: -1rem; top: -2rem;
    line-height: 1;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: #fff;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 100px;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.3);
}
.hero h1 {
    color: #fff !important;
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.5rem !important;
    line-height: 1.2 !important;
}
.hero p {
    color: rgba(255,255,255,0.82);
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
}

/* ---- SIDEBAR ---- */
section[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--blue-200) !important;
}
section[data-testid="stSidebar"] .sidebar-brand {
    background: linear-gradient(135deg, #2563EB, #60A5FA);
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    text-align: center;
    color: #fff;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 1.5rem;
    letter-spacing: 0.02em;
}
section[data-testid="stSidebar"] label {
    color: var(--text-dark) !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.04em !important;
}
section[data-testid="stSidebar"] .stNumberInput input,
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--blue-50) !important;
    border: 1.5px solid var(--blue-200) !important;
    border-radius: 10px !important;
    color: var(--text-dark) !important;
    font-weight: 500 !important;
}
section[data-testid="stSidebar"] .stNumberInput input:focus,
section[data-testid="stSidebar"] .stSelectbox > div > div:focus {
    border-color: var(--blue-400) !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,0.15) !important;
}

/* ---- CARDS ---- */
.info-card {
    background: var(--white);
    border: 1.5px solid var(--blue-200);
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    box-shadow: var(--shadow);
    margin-bottom: 1.2rem;
    transition: box-shadow 0.2s, border-color 0.2s;
}
.info-card:hover {
    box-shadow: 0 8px 32px rgba(59,130,246,0.18);
    border-color: var(--blue-300);
}
.card-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
.card-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-soft);
    margin-bottom: 0.3rem;
}
.card-value {
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--text-dark);
}
.card-sub {
    font-size: 0.78rem;
    color: var(--text-soft);
    margin-top: 0.2rem;
}

/* ---- PREDICT BUTTON ---- */
.stButton > button {
    background: linear-gradient(135deg, #2563EB 0%, #60A5FA 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(37,99,235,0.4) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ---- RESULT PANEL ---- */
.result-panel {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 2px solid var(--blue-300);
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(59,130,246,0.15);
    margin-top: 1.5rem;
    animation: fadeIn 0.4s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-soft);
    margin-bottom: 0.5rem;
}
.result-value {
    font-size: 3.5rem;
    font-weight: 700;
    color: var(--blue-600);
    line-height: 1;
    margin-bottom: 0.4rem;
}
.result-unit {
    font-size: 1.1rem;
    font-weight: 400;
    color: var(--text-soft);
}
.result-note {
    font-size: 0.82rem;
    color: var(--text-soft);
    margin-top: 0.8rem;
}

/* ---- SECTION HEADER ---- */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 2rem 0 1rem;
}
.section-dot {
    width: 8px; height: 8px;
    background: var(--blue-500);
    border-radius: 50%;
}
.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-dark);
    margin: 0;
}
.section-line {
    flex: 1;
    height: 1px;
    background: var(--blue-200);
}

/* ---- DIVIDER & FOOTER ---- */
hr { border-color: var(--blue-200) !important; }
.footer {
    text-align: center;
    color: var(--text-soft);
    font-size: 0.78rem;
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--blue-200);
}
.footer span { color: var(--blue-500); }
</style>
""", unsafe_allow_html=True)

# =========================
# HERO BANNER
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered Forecasting</div>
    <h1>⚡ Energy Consumption Predictor</h1>
    <p>Enter your building details in the sidebar to get an instant AI prediction.</p>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR INPUTS
# =========================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🔧 Building Details</div>', unsafe_allow_html=True)

    sq_ft = st.number_input("📐 Square Footage", min_value=500, max_value=10000, value=2000, step=50)
    occupants = st.number_input("👥 Number of Occupants", min_value=1, max_value=50, value=5)
    appliances = st.number_input("🔌 Appliances Used", min_value=1, max_value=100, value=10)
    temp = st.slider("🌡️ Average Temperature (°C)", 0, 50, 25)
    building_type = st.selectbox("🏢 Building Type", ["Residential", "Industrial"])
    weekend = st.selectbox("📅 Day Type", ["Weekday", "Weekend"])

# =========================
# ENCODING
# =========================
industrial   = 1 if building_type == "Industrial" else 0
residential  = 1 if building_type == "Residential" else 0
weekend_val  = 1 if weekend == "Weekend" else 0

input_data = np.array([[sq_ft, occupants, appliances, temp, industrial, residential, weekend_val]])

# =========================
# SUMMARY CARDS
# =========================
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <p class="section-title">Input Summary</p>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "📐", "Square Footage",    f"{sq_ft:,} sq ft",  "building area"),
    (c2, "👥", "Occupants",         str(occupants),       "people"),
    (c3, "🔌", "Appliances",        str(appliances),      "devices"),
    (c4, "🌡️", "Temperature",       f"{temp}°C",          building_type),
]
for col, icon, label, value, sub in cards:
    with col:
        st.markdown(f"""
        <div class="info-card">
            <div class="card-icon">{icon}</div>
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            <div class="card-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# PREDICT BUTTON
# =========================
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <p class="section-title">Prediction</p>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col_btn, _ = st.columns([1, 2])
with col_btn:
    predict = st.button("⚡ Predict Energy Consumption")

if predict:
    prediction = model.predict(input_data)
    val = prediction[0]

    # Efficiency label
    if val < 100:
        efficiency = "🟢 Low Usage — Excellent efficiency"
    elif val < 250:
        efficiency = "🟡 Moderate Usage — Room to optimise"
    else:
        efficiency = "🔴 High Usage — Consider energy-saving measures"

    st.markdown(f"""
    <div class="result-panel">
        <div class="result-label">Estimated Energy Usage</div>
        <div class="result-value">{val:.2f} <span class="result-unit">kWh</span></div>
        <div class="result-note">{efficiency}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    Built with <span>♥</span> by Atharvi &nbsp;·&nbsp; AI-Powered Energy Forecasting
</div>
""", unsafe_allow_html=True)
