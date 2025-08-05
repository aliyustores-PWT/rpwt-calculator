
import streamlit as st

st.set_page_config(page_title="RPWT v3.0 Pension Calculator", layout="centered")

st.title("✅ RPWT Version 3.0 Pension Calculator")
st.markdown("This tool helps retirees estimate their monthly pension and lump sum using RPWT v3.0.")

# Placeholder inputs (to be replaced with real inputs based on template)
sector = st.selectbox("Select Sector", ["Public", "Private"])
annual_salary = st.number_input("Enter Annual Salary", min_value=0.0, step=10000.0)
age_at_retirement = st.slider("Select Age at Retirement", min_value=50, max_value=70, value=60)

# Placeholder output
if annual_salary > 0:
    estimated_pension = 0.5 * (annual_salary / 12)
    st.success(f"Estimated Monthly Pension: ₦{estimated_pension:,.2f}")
    st.info("Note: Final pension depends on RSA balance and longevity projections.")

st.caption("For demonstration purposes only. Based on RPWT version 3.0 parameters.")
