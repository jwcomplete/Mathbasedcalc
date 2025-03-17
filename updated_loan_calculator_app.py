
import streamlit as st
import pandas as pd
import numpy as np

# Define Loan Limits
conforming_loan_limit = 806500
high_balance_loan_limit = 1000000

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
    down_payment_pct = loan_formulas[formula]["down_payment"] / 100
    seller_concession_pct = loan_formulas[formula]["seller_concession"] / 100

    total_sale_price = purchase_price / (1 - seller_concession_pct)
    loan_amount = total_sale_price * (1 - down_payment_pct)
    cash_to_close = total_sale_price * down_payment_pct

    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12
    monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** -num_payments)

    # Calculate monthly taxes & insurance
    monthly_property_tax = property_tax / 12
    monthly_home_insurance = home_insurance / 12
    monthly_flood_insurance = flood_insurance / 12

    total_monthly_payment = monthly_payment + monthly_property_tax + monthly_home_insurance + monthly_flood_insurance

    return total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment

st.title("C/HB Loan Calculator - Updated")

# User Inputs
occupancy_type = st.selectbox("Select Occupancy Type", ["Primary Residence", "Second Home", "Investment Property"])
num_units = st.selectbox("Select Number of Units", [1, 2, 3, 4])
purchase_price = st.number_input("Enter Purchase Price ($)", min_value=50000, max_value=2000000, step=5000)
loan_term = st.number_input("Enter Loan Term (Years)", min_value=5, max_value=30, step=5, value=30)
interest_rate = st.number_input("Enter Interest Rate (%)", min_value=1.0, max_value=10.0, step=0.125, value=5.625)

# Additional Fields for Property Tax & Insurance
property_tax = st.number_input("Enter Annual Property Tax ($)", min_value=0, max_value=50000, step=100)
home_insurance = st.number_input("Enter Annual Home Insurance ($)", min_value=0, max_value=20000, step=100)
flood_insurance = st.number_input("Enter Annual Flood Insurance ($)", min_value=0, max_value=20000, step=100)

# Determine eligible loan formulas
eligible_formulas = []
for formula, values in loan_formulas.items():
    max_price = (conforming_loan_limit / (1 - values["down_payment"] / 100)) * (1 - values["seller_concession"] / 100)

    # Check if purchase price and LTV restrictions are met
    if purchase_price <= max_price and values["max_ltv"] <= ltv_limits.get(occupancy_type, {}).get(num_units, 0):
        eligible_formulas.append(formula)

# Dropdown for Eligible Formulas
selected_formula = st.selectbox("Select Loan Formula", eligible_formulas)

# Calculate Loan Details
if st.button("Calculate Loan Details"):
    total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
        purchase_price, interest_rate, loan_term, selected_formula, property_tax, home_insurance, flood_insurance
    )

    # Display Results
    st.write("### Loan Calculation Results")
    st.write(f"**Total Sale Price (Including Seller Concession):** ${total_sale_price:,.2f}")
    st.write(f"**Loan Amount (LTV-Based):** ${loan_amount:,.2f}")
    st.write(f"**Cash to Close (Down Payment + Costs):** ${cash_to_close:,.2f}")
    st.write(f"**Monthly Mortgage Payment (Principal & Interest Only):** ${monthly_payment:,.2f}")
    st.write(f"**Total Monthly Payment (Including Taxes & Insurance):** ${total_monthly_payment:,.2f}")
