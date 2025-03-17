
import streamlit as st

# Set Page Configuration for a Compact UI
st.set_page_config(page_title="Home Affordability Calculator", layout="wide")

# UI Layout
st.title("🏡 Home Affordability Calculator")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    occupancy_type = st.selectbox("🏠 Occupancy", ["Primary Residence", "Second Home", "Investment Property"])
    num_units = st.selectbox("🏢 Units", [1, 2, 3, 4])
    purchase_price = float(st.number_input("💰 Price ($)", min_value=50000.0, max_value=2000000.0, step=5000.0, value=50000.0, format="%.0f"))

with col2:
    loan_term = float(st.number_input("📆 Term (Years)", min_value=5.0, max_value=30.0, step=5.0, value=30.0, format="%.0f"))
    interest_rate = float(st.number_input("📊 Interest (%)", min_value=1.0, max_value=10.0, step=0.001, value=5.625, format="%.3f"))

with col3:
    property_tax = float(st.number_input("🏡 Tax ($)", min_value=0.0, max_value=50000.0, step=100.0, value=0.0, format="%.0f"))
    home_insurance = float(st.number_input("🔒 Insurance ($)", min_value=0.0, max_value=20000.0, step=100.0, value=0.0, format="%.0f"))
    flood_insurance = float(st.number_input("🌊 Flood Ins. ($)", min_value=0.0, max_value=20000.0, step=100.0, value=0.0, format="%.0f"))
