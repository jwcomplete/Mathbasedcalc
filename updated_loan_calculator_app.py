
import streamlit as st

# Loan formula setup and max limits
loan_formulas = {
    "C.3.0": {"down_payment": 3, "seller_concession": 0, "max_ltv": 97},
    "C.3.3": {"down_payment": 3, "seller_concession": 3, "max_ltv": 97},
    "C.5.3": {"down_payment": 5, "seller_concession": 3, "max_ltv": 95},
    # Add more formulas here
}

max_loan_limit = 806500.0

# Function to calculate loan details
def calculate_loan(purchase_price, loan_term, interest_rate, down_payment_pct, seller_concession_pct, property_tax, home_insurance, flood_insurance):
    total_sale_price = purchase_price / (1 - seller_concession_pct)
    loan_amount = total_sale_price * (1 - down_payment_pct)
    cash_to_close = total_sale_price * down_payment_pct

    # Monthly mortgage calculation (PMT formula)
    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12
    monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** -num_payments)

    # Escrow calculations (tax, insurance, flood insurance)
    monthly_property_tax = property_tax / 12
    monthly_home_insurance = home_insurance / 12
    monthly_flood_insurance = flood_insurance / 12

    # Total monthly payment
    total_monthly_payment = monthly_payment + monthly_property_tax + monthly_home_insurance + monthly_flood_insurance

    return total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment

# Streamlit UI setup
st.title("🏡 Home Affordability Calculator")

# User inputs for purchase price, loan terms, and other details
purchase_price = float(st.number_input("💰 Price ($)", min_value=50000.0, max_value=999999999.0, step=5000.0, value=807000.0))
loan_term = float(st.number_input("📆 Term (Years)", min_value=5.0, max_value=30.0, step=5.0, value=30.0))
interest_rate = float(st.number_input("📊 Interest (%)", min_value=1.0, max_value=10.0, step=0.001, value=5.625))

property_tax = float(st.number_input("🏡 Tax ($)", min_value=0.0, max_value=50000.0, step=100.0, value=0.0))
home_insurance = float(st.number_input("🔒 Insurance ($)", min_value=0.0, max_value=20000.0, step=100.0, value=0.0))
flood_insurance = float(st.number_input("🌊 Flood Ins. ($)", min_value=0.0, max_value=20000.0, step=100.0, value=0.0))

# Loan formula selection
loan_options = [key for key, values in loan_formulas.items()]
selected_formula = st.selectbox("📜 Loan Formula", loan_options)

# Check eligibility and calculate
if st.button("📊 Calculate Loan & Monthly Payment"):
    down_payment_pct = loan_formulas[selected_formula]["down_payment"] / 100
    seller_concession_pct = loan_formulas[selected_formula]["seller_concession"] / 100

    total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
        purchase_price, loan_term, interest_rate, down_payment_pct, seller_concession_pct, property_tax, home_insurance, flood_insurance
    )

    # Display results
    st.write(f"Total Sale Price: ${total_sale_price:,.2f}")
    st.write(f"Loan Amount: ${loan_amount:,.2f}")
    st.write(f"Cash to Close: ${cash_to_close:,.2f}")
    st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
    st.write(f"Total Monthly Payment (Including Taxes & Insurance): ${total_monthly_payment:,.2f}")

    # Ineligible loan handling
    if loan_amount > max_loan_limit:
        st.markdown(f'<div style="background-color:red; color:white; padding:10px; font-size:16px;">'
                    f'<strong>{selected_formula} is ineligible because the loan amount (${loan_amount:,.2f}) exceeds the max loan limit (${max_loan_limit:,.2f}).</strong></div>',
                    unsafe_allow_html=True)

        # Calculate adjusted down payment to meet max loan limit
        adjusted_down_payment = ((loan_amount - max_loan_limit) / total_sale_price * 100) + loan_formulas[selected_formula]["down_payment"]
        new_cash_to_close = total_sale_price * (adjusted_down_payment / 100)

        # Button for recalculating with adjusted down payment
        st.button(f"✅ Apply {adjusted_down_payment:.2f}% Down Payment & Recalculate\nTotal Cash to Close: ${new_cash_to_close:,.2f}")

        # Switching to next eligible formula
        next_formula = None
        for key, values in loan_formulas.items():
            if key != selected_formula and (purchase_price * (1 - values["down_payment"] / 100)) <= max_loan_limit:
                next_formula = key
                break

        if next_formula:
            new_cash_to_close_next = total_sale_price * (loan_formulas[next_formula]["down_payment"] / 100)
            st.button(f"🔄 Switch to `{next_formula}` (Eligible Formula)\nTotal Cash to Close: ${new_cash_to_close_next:,.2f}")
