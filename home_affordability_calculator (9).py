import streamlit as st
import pandas as pd
import numpy as np

# Set Page Configuration for a Compact UI
st.set_page_config(page_title="Home Affordability Calculator", layout="wide")

# Define Loan Limits
conforming_loan_limit = 806500.00
high_balance_loan_limit = 1000000.00

# Define available C & HB Formulas with Down Payment, Seller Concessions, and LTV Restrictions
loan_formulas = {
    "C.3.0": {"down_payment": 3, "seller_concession": 0, "max_ltv": 97},
    "C.3.3": {"down_payment": 3, "seller_concession": 3, "max_ltv": 97},
    "C.3.6": {"down_payment": 3, "seller_concession": 6, "max_ltv": 97},
    "C.5.3": {"down_payment": 5, "seller_concession": 3, "max_ltv": 95},
    "C.10.6": {"down_payment": 10, "seller_concession": 6, "max_ltv": 90},
    "C.15.2": {"down_payment": 15, "seller_concession": 2, "max_ltv": 85},
    "C.20.2": {"down_payment": 20, "seller_concession": 2, "max_ltv": 80},
    "C.25.2": {"down_payment": 25, "seller_concession": 2, "max_ltv": 75},
    "HB.3.3": {"down_payment": 3, "seller_concession": 3, "max_ltv": 95},
    "HB.3.6": {"down_payment": 3, "seller_concession": 6, "max_ltv": 95},
    "HB.10.6": {"down_payment": 10, "seller_concession": 6, "max_ltv": 90},
    "HB.15.2": {"down_payment": 15, "seller_concession": 2, "max_ltv": 85},
    "HB.20.2": {"down_payment": 20, "seller_concession": 2, "max_ltv": 80},
    "HB.25.2": {"down_payment": 25, "seller_concession": 2, "max_ltv": 75},
}

# Define LTV Restrictions by Occupancy Type and Units
ltv_limits = {
    "Primary Residence": {1: 97, 2: 85, 3: 75, 4: 75},
    "Second Home": {1: 90},
    "Investment Property": {1: 85, 2: 85, 3: 75, 4: 75},
    "High-Balance": {1: 95, 2: 85, 3: 75, 4: 75}
}

# Compact UI Layout
st.title("\U0001F3E1 Home Affordability Calculator")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    occupancy_type = st.selectbox("🏠 Occupancy", ["Primary Residence", "Second Home", "Investment Property"])
    num_units = st.selectbox("🏢 Units", [1, 2, 3, 4])
    purchase_price = st.number_input("💰 Price ($)", min_value=50000.0, max_value=2000000.0, step=5000.0, value=50000.0, format="%.2f")

with col2:
    loan_term = st.number_input("📆 Term (Years)", min_value=5.0, max_value=30.0, step=5.0, value=30.0, format="%.2f")
    interest_rate = st.number_input("📊 Interest (%)", min_value=1.0, max_value=10.0, step=0.001, value=5.625, format="%.3f")

with col3:
    property_tax = st.number_input("🏡 Tax ($)", min_value=0.0, max_value=50000.0, step=100.0, value=0.0, format="%.2f")
    home_insurance = st.number_input("🔒 Insurance ($)", min_value=0.0, max_value=20000.0, step=100.0, value=0.0, format="%.2f")
    flood_insurance = st.number_input("🌊 Flood Ins. ($)", min_value=0.0, max_value=20000.0, step=100.0, value=0.0, format="%.2f")

st.markdown("---")

# Determine eligible loan formulas
eligible_formulas = []
for formula, values in loan_formulas.items():
    max_price = (conforming_loan_limit / (1 - values["down_payment"] / 100)) * (1 - values["seller_concession"] / 100)

    if purchase_price and purchase_price <= max_price and values["max_ltv"] <= ltv_limits.get(occupancy_type, {}).get(num_units, 0):
        eligible_formulas.append(formula)

selected_formula = st.selectbox("📜 Loan Formula", eligible_formulas)

if st.button("🧮 Calculate"):
    st.write("Calculation logic goes here")



if st.button("🧮 Calculate"):
    total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment, monthly_property_tax, monthly_home_insurance, monthly_flood_insurance = calculate_loan(
        purchase_price, interest_rate, loan_term, selected_formula, property_tax, home_insurance, flood_insurance
    )

    # Compact Results Display
    colA, colB, colC = st.columns([1, 1, 1])

    with colA:
        st.info(f"💰 **Total Sale Price:** ${total_sale_price:,.2f}")
        st.success(f"🏦 **Loan Amount:** ${loan_amount:,.2f}")

    with colB:
        st.write(f"💵 **Cash to Close:** ${cash_to_close:,.2f}")
        st.write(f"📊 **Interest Payment:** ${monthly_payment:,.2f}")

    with colC:
        st.write(f"🏡 **Property Tax:** ${monthly_property_tax:,.2f}")
        st.write(f"🔒 **Home Insurance:** ${monthly_home_insurance:,.2f}")
        st.write(f"🌊 **Flood Insurance:** ${monthly_flood_insurance:,.2f}")
        st.write(f"💸 **Total Monthly Payment:** ${total_monthly_payment:,.2f}")

