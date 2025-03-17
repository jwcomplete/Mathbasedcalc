
import streamlit as st
import pandas as pd
import numpy as np

# Define Loan Limits
conforming_loan_limit = 806500
high_balance_loan_limit = 1000000

# Define available C & HB Formulas with Down Payment & Seller Concessions
loan_formulas = {
    "C.3.0": {"down_payment": 3, "seller_concession": 0},
    "C.3.3": {"down_payment": 3, "seller_concession": 3},
    "C.3.6": {"down_payment": 3, "seller_concession": 6},
    "C.3.9": {"down_payment": 3, "seller_concession": 9},
    "C.5.0": {"down_payment": 5, "seller_concession": 0},
    "C.5.3": {"down_payment": 5, "seller_concession": 3},
    "C.10.6": {"down_payment": 10, "seller_concession": 6},
    "C.15.2": {"down_payment": 15, "seller_concession": 2},
    "C.20.2": {"down_payment": 20, "seller_concession": 2},
    "C.25.2": {"down_payment": 25, "seller_concession": 2},
    "HB.3.0": {"down_payment": 3, "seller_concession": 0},
    "HB.3.3": {"down_payment": 3, "seller_concession": 3},
    "HB.3.6": {"down_payment": 3, "seller_concession": 6},
    "HB.10.6": {"down_payment": 10, "seller_concession": 6},
    "HB.15.2": {"down_payment": 15, "seller_concession": 2},
    "HB.20.2": {"down_payment": 20, "seller_concession": 2},
    "HB.25.2": {"down_payment": 25, "seller_concession": 2},
}

# Function to calculate loan values
def calculate_loan(purchase_price, interest_rate, loan_term, formula):
    down_payment_pct = loan_formulas[formula]["down_payment"] / 100
    seller_concession_pct = loan_formulas[formula]["seller_concession"] / 100

    total_sale_price = purchase_price / (1 - seller_concession_pct)
    loan_amount = total_sale_price * (1 - down_payment_pct)
    cash_to_close = total_sale_price * down_payment_pct

    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12
    monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** -num_payments)

    return total_sale_price, loan_amount, cash_to_close, monthly_payment

st.title("C/HB Loan Calculator")

occupancy_type = st.selectbox("Select Occupancy Type", ["Primary Residence", "Second Home", "Investment Property"])
num_units = st.selectbox("Select Number of Units", [1, 2, 3, 4])
purchase_price = st.number_input("Enter Purchase Price ($)", min_value=50000, max_value=2000000, step=5000)
loan_term = st.number_input("Enter Loan Term (Years)", min_value=5, max_value=30, step=5, value=30)
interest_rate = st.number_input("Enter Interest Rate (%)", min_value=1.0, max_value=10.0, step=0.125, value=5.625)

eligible_formulas = []
for formula, values in loan_formulas.items():
    max_price = (conforming_loan_limit / (1 - values["down_payment"] / 100)) * (1 - values["seller_concession"] / 100)
    if purchase_price <= max_price:
        eligible_formulas.append(formula)

selected_formula = st.selectbox("Select Loan Formula", eligible_formulas)

if st.button("Calculate Loan Details"):
    total_sale_price, loan_amount, cash_to_close, monthly_payment = calculate_loan(
        purchase_price, interest_rate, loan_term, selected_formula
    )

    st.write("### Loan Calculation Results")
    st.write(f"**Total Sale Price (Including Seller Concession):** ${total_sale_price:,.2f}")
    st.write(f"**Loan Amount (LTV-Based):** ${loan_amount:,.2f}")
    st.write(f"**Cash to Close (Down Payment + Costs):** ${cash_to_close:,.2f}")
    st.write(f"**Monthly Mortgage Payment:** ${monthly_payment:,.2f}")
