
import streamlit as st

# Set Page Configuration for a Compact UI
st.set_page_config(page_title="Home Affordability Calculator", layout="wide")

# Function to calculate mortgage payments and total costs
def calculate_loan(purchase_price, loan_term, interest_rate, property_tax, home_insurance, flood_insurance):
    # Convert interest rate to monthly interest
    monthly_interest_rate = (interest_rate / 100) / 12
    loan_amount = purchase_price * 0.90  # Assuming 10% down payment (Modify as needed)
    num_payments = loan_term * 12

    # Monthly mortgage payment formula (PMT formula)
    if monthly_interest_rate > 0:
        monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    else:
        monthly_payment = loan_amount / num_payments  # If interest rate is 0

    # Calculate escrow (taxes and insurance)
    monthly_property_tax = property_tax / 12
    monthly_home_insurance = home_insurance / 12
    monthly_flood_insurance = flood_insurance / 12

    # Total monthly cost
    total_monthly_payment = monthly_payment + monthly_property_tax + monthly_home_insurance + monthly_flood_insurance

    return loan_amount, monthly_payment, total_monthly_payment, monthly_property_tax, monthly_home_insurance, monthly_flood_insurance

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

st.markdown("---")

# Calculate Button
if st.button("📊 Calculate Loan & Monthly Payment"):
    loan_amount, monthly_payment, total_monthly_payment, monthly_property_tax, monthly_home_insurance, monthly_flood_insurance = calculate_loan(
        purchase_price, loan_term, interest_rate, property_tax, home_insurance, flood_insurance
    )

    # Display Results
    st.success("📌 Loan Calculation Results:")
    st.write(f"🏦 **Loan Amount:** ${loan_amount:,.2f}")
    st.write(f"💰 **Monthly Mortgage Payment:** ${monthly_payment:,.2f}")
    st.write(f"🏡 **Monthly Property Tax:** ${monthly_property_tax:,.2f}")
    st.write(f"🔒 **Monthly Home Insurance:** ${monthly_home_insurance:,.2f}")
    st.write(f"🌊 **Monthly Flood Insurance:** ${monthly_flood_insurance:,.2f}")
    st.write(f"💸 **Total Monthly Payment:** ${total_monthly_payment:,.2f}")
