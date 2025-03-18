
import streamlit as st

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

# Max Loan Limit (for primary residence 1-unit standard loan)
max_loan_limit = 806500.0

# Function to calculate mortgage payments and eligibility
def calculate_loan(purchase_price, loan_term, interest_rate, formula, property_tax, home_insurance, flood_insurance):
    down_payment_pct = loan_formulas[formula]["down_payment"] / 100
    seller_concession_pct = loan_formulas[formula]["seller_concession"] / 100

    total_sale_price = purchase_price / (1 - seller_concession_pct)
    loan_amount = total_sale_price * (1 - down_payment_pct)
    cash_to_close = total_sale_price * down_payment_pct

    # Convert interest rate to monthly interest
    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12

    # Monthly mortgage payment formula (PMT formula)
    if monthly_interest_rate > 0:
        monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    else:
        monthly_payment = loan_amount / num_payments

    # Calculate escrow (taxes and insurance)
    monthly_property_tax = property_tax / 12
    monthly_home_insurance = home_insurance / 12
    monthly_flood_insurance = flood_insurance / 12

    # Total monthly cost
    total_monthly_payment = monthly_payment + monthly_property_tax + monthly_home_insurance + monthly_flood_insurance

    return total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment

# UI Layout
st.title("🏡 Home Affordability Calculator")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    occupancy_type = st.selectbox("🏠 Occupancy", ["Primary Residence", "Second Home", "Investment Property"])
    num_units = st.selectbox("🏢 Units", [1, 2, 3, 4])
    purchase_price = float(st.number_input("💰 Price ($)", min_value=50000.0, max_value=999999999.0, step=5000.0, value=807000.0, format="%.2f"))

with col2:
    loan_term = float(st.number_input("📆 Term (Years)", min_value=5.0, max_value=30.0, step=5.0, value=30.0, format="%.0f"))
    interest_rate = float(st.number_input("📊 Interest (%)", min_value=1.0, max_value=10.0, step=0.001, value=5.625, format="%.3f"))

with col3:
    property_tax = float(st.number_input("🏡 Tax ($)", min_value=0.0, max_value=50000.0, step=100.0, value=0.0, format="%.2f"))
    home_insurance = float(st.number_input("🔒 Insurance ($)", min_value=0.0, max_value=20000.0, step=100.0, value=0.0, format="%.2f"))
    flood_insurance = float(st.number_input("🌊 Flood Ins. ($)", min_value=0.0, max_value=20000.0, step=100.0, value=0.0, format="%.2f"))

st.markdown("---")

# Loan Formula Selection
loan_options = []
for key, values in loan_formulas.items():
    estimated_loan_amount = purchase_price * (1 - values["down_payment"] / 100)
    if estimated_loan_amount > max_loan_limit:
        loan_options.append(f"{key} 🚫")
    else:
        loan_options.append(key)

selected_formula = st.selectbox("📜 Loan Formula", loan_options)

# Check if the selected formula is eligible
is_ineligible = "🚫" in selected_formula

# Calculate Button
if st.button("📊 Calculate Loan & Monthly Payment"):
    formula_key = selected_formula.replace(" 🚫", "")

    total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
        purchase_price, loan_term, interest_rate, formula_key, property_tax, home_insurance, flood_insurance
    )

    if loan_amount > max_loan_limit:
        st.markdown(
            f'<div style="background-color:red; color:white; padding:10px; font-size:16px;">'
            f'<strong>{formula_key} is ineligible because the loan amount (${loan_amount:,.2f}) exceeds the max loan limit (${max_loan_limit:,.2f}).</strong></div>',
            unsafe_allow_html=True)

        # Suggest increasing down payment
        adjusted_down_payment = ((loan_amount - max_loan_limit) / total_sale_price * 100) + loan_formulas[formula_key]["down_payment"]
        new_cash_to_close = total_sale_price * (adjusted_down_payment / 100)

        st.markdown(
            f"💡 **Your Options:**"
        )

        # Button for increasing down payment and recalculating
        st.button(
            f"✅ Apply {adjusted_down_payment:.2f}% Down Payment & Recalculate - Total Cash to Close: ${new_cash_to_close:,.2f}"
        )

        # Button to switch to the next eligible formula
        next_formula = None
        for key, values in loan_formulas.items():
            if key != formula_key and (purchase_price * (1 - values["down_payment"] / 100)) <= max_loan_limit:
                next_formula = key
                break

        if next_formula:
            # Recalculate total cash to close for the next eligible formula
            new_cash_to_close_next = total_sale_price * (loan_formulas[next_formula]["down_payment"] / 100)
            
            st.button(
                f"🔄 Switch to `{next_formula}` (Eligible Formula)
"
                f" - Total Cash to Close: ${new_cash_to_close_next:,.2f}"
            )
