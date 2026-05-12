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
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: midnightblue;
    color: white;
}

/* Headings */
h1, h2, h3 {
    color: deepskyblue;
    text-align: center;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: black;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Labels */
label, .stSelectbox label, .stNumberInput label, .stSlider label {
    color: white !important;
    font-weight: bold;
}

/* Button */
.stButton>button {
    background-color: royalblue;
    color: darkblue;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: dodgerblue;
    color: white;
}

/* Metric Value */
[data-testid="stMetricValue"] {
    color: white;
    font-size: 28px;
    font-weight: bold;
}

/* Metric Label */
[data-testid="stMetricLabel"] {
    color: deepskyblue;
    font-weight: bold;
}

/* Success Message */
.stSuccess {
    background-color: royalblue;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("⚡ Real-Time Energy Consumption Prediction")

st.markdown(
    "<h3>AI-Powered Energy Forecasting Dashboard</h3>",
    unsafe_allow_html=True
)

st.write("")

# =========================
# SIDEBAR INPUTS
# =========================

st.sidebar.header("🔧 Enter Building Details")

sq_ft = st.sidebar.number_input(
    "Square Footage",
    min_value=500,
    max_value=10000,
    value=2000
)

occupants = st.sidebar.number_input(
    "Number of Occupants",
    min_value=1,
    max_value=50,
    value=5
)

appliances = st.sidebar.number_input(
    "Appliances Used",
    min_value=1,
    max_value=100,
    value=10
)

temp = st.sidebar.slider(
    "Average Temperature",
    0, 50, 25
)

building_type = st.sidebar.selectbox(
    "Building Type",
    ["Residential", "Industrial"]
)

weekend = st.sidebar.selectbox(
    "Weekend?",
    ["No", "Yes"]
)

# =========================
# ENCODING INPUTS
# =========================

industrial = 1 if building_type == "Industrial" else 0
residential = 1 if building_type == "Residential" else 0
weekend_val = 1 if weekend == "Yes" else 0

# =========================
# INPUT ARRAY
# =========================

input_data = np.array([[
    sq_ft,
    occupants,
    appliances,
    temp,
    industrial,
    residential,
    weekend_val
]])

# =========================
# PREDICTION BUTTON
# =========================

if st.button("⚡ Predict Energy Consumption"):

    prediction = model.predict(input_data)

    st.success(
        f"Predicted Energy Consumption: {prediction[0]:.2f} kWh"
    )

    st.metric(
        label="⚡ Estimated Energy Usage",
        value=f"{prediction[0]:.2f} kWh"
    )

# =========================
# FOOTER
# =========================

st.write("")
st.markdown("---")

st.markdown(
    "<center style='color:white;'>Created by Atharvi 💙</center>",
    unsafe_allow_html=True
)
