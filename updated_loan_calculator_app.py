
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

# Function to calculate loan values
def calculate_loan(purchase_price, interest_rate, loan_term, formula, property_tax, home_insurance, flood_insurance):
    interest_rate = round(float(interest_rate), 3)  # Ensure explicit float conversion
    down_payment_pct = loan_formulas[formula]["down_payment"] / 100
    seller_concession_pct = loan_formulas[formula]["seller_concession"] / 100

    total_sale_price = round(purchase_price / (1 - seller_concession_pct), 2)
    loan_amount = round(total_sale_price * (1 - down_payment_pct), 2)
    cash_to_close = round(total_sale_price * down_payment_pct, 2)

    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12
    monthly_payment = round((monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** -num_payments), 2)

    # Calculate monthly taxes & insurance
    monthly_property_tax = round(property_tax / 12, 2)
    monthly_home_insurance = round(home_insurance / 12, 2)
    monthly_flood_insurance = round(flood_insurance / 12, 2)

    total_monthly_payment = round(monthly_payment + monthly_property_tax + monthly_home_insurance + monthly_flood_insurance, 2)

    return total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment, monthly_property_tax, monthly_home_insurance, monthly_flood_insurance

# Compact UI Layout
st.title("🏡 Home Affordability Calculator")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    occupancy_type = st.selectbox("🏠 Occupancy", ["Primary Residence", "Second Home", "Investment Property"])
    num_units = st.selectbox("🏢 Units", [1, 2, 3, 4])
    purchase_price = int(st.number_input("💰 Price ($)", value=50000, min_value=50000, max_value=999999999, step=5000, format="%d"))

with col2:
    loan_term = int(st.number_input("📆 Term (Years)", value=30, min_value=5, max_value=30, step=5, format="%d"))
    interest_rate = float(st.number_input("📊 Interest (%)", value=5.625, min_value=1.0, max_value=10.0, step=0.001, format="%.3f"))

with col3:
    property_tax = int(st.number_input("🏡 Tax ($)", value=0, min_value=0, max_value=50000, step=100, format="%d"))
    home_insurance = int(st.number_input("🔒 Insurance ($)", value=0, min_value=0, max_value=20000, step=100, format="%d"))
    flood_insurance = int(st.number_input("🌊 Flood Ins. ($)", value=0, min_value=0, max_value=20000, step=100, format="%d"))

st.markdown("---")

# Determine eligible loan formulas
eligible_formulas = []
for formula, values in loan_formulas.items():
    max_price = (conforming_loan_limit / (1 - values["down_payment"] / 100)) * (1 - values["seller_concession"] / 100)

    if purchase_price <= max_price and values["max_ltv"] <= ltv_limits.get(occupancy_type, {}).get(num_units, 0):
        eligible_formulas.append(formula)

selected_formula = st.selectbox("📜 Loan Formula", eligible_formulas)

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

