# RPWT Pension Calculator - PenCom Version 3.0
# By Aliyu S. Sani | Deployment Ready for Streamlit Cloud

import streamlit as st
import datetime as dt

# ----------------------
# 🔒 Password Protection
# ----------------------
def password_gate():
    st.markdown("<h3 style='text-align: center;'>🔐 PenCom RPWT Pension Calculator</h3>", unsafe_allow_html=True)
    pwd = st.text_input("Enter Password", type="password")
    if pwd != "PenCom2025":
        st.warning("Access denied. Enter the correct password to proceed.")
        st.stop()

password_gate()

# ----------------------
# 📌 Backend Settings (Sample values - adjust as needed)
# ----------------------
SS_SC = {
    "Sector": ["Public", "Private"],
    "Salary Structure": ["CONPSS", "CONHESS", "CONUASS", "CONTISS"],
    "Grade Level": list(range(1, 18)),
    "Step": list(range(1, 16)),
    "Gender": ["Male", "Female"],
    "Frequency": ["Monthly", "Quarterly"]
}

PublicMonths = 204
PrivateMonths = 192
mortality_factor = 10.5

# ----------------------
# 🧮 Pension Calculation Logic
# ----------------------
def calculate_pension(rsa_balance, final_salary, sector):
    months = PublicMonths if sector == "Public" else PrivateMonths
    annuity = rsa_balance / (months * mortality_factor / 12)
    min_pension = max(annuity, 30000)  # replace with real logic if needed
    return round(min_pension, 2)

# ----------------------
# 📋 User Inputs
# ----------------------
st.subheader("📝 Section A - Retiree Information")

col1, col2 = st.columns(2)

with col1:
    rsa_balance = st.number_input("RSA Balance (₦)", min_value=0.0, format="%.2f")
    annual_salary = st.number_input("Annual Salary (₦)", min_value=0.0, format="%.2f")
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", SS_SC["Gender"])
    selection = st.selectbox("Sector", SS_SC["Sector"])

with col2:
    retirement_date = st.date_input("Retirement Date")
    program_date = st.date_input("Date of Programming", dt.date.today())
    salary_structure = st.selectbox("Salary Structure", SS_SC["Salary Structure"])
    grade = st.selectbox("Grade Level", SS_SC["Grade Level"])
    step = st.selectbox("Step", SS_SC["Step"])
    frequency = st.selectbox("Payment Frequency", SS_SC["Frequency"])

# ----------------------
# 📊 Final Calculations
# ----------------------
final_salary = annual_salary / 12
monthly_pension = calculate_pension(rsa_balance, final_salary, selection)

# ----------------------
# 💡 Display Results
# ----------------------
st.subheader("📈 Pension Projection Result")
st.write(f"**Final Monthly Salary:** ₦{final_salary:,.2f}")
st.write(f"**Projected Monthly Pension:** ₦{monthly_pension:,.2f}")

# ----------------------
# 📎 Footer
# ----------------------
st.markdown("---")
st.caption("Designed by Aliyu S. Sani | PenCom RPWT v3.0 | August 2025")
