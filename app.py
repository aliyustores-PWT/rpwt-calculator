# RPWT Pension Calculator - PenCom Version 3.0 (Sections A–D)
# By Aliyu S. Sani | Deployment Ready for Streamlit Cloud

import streamlit as st
import datetime as dt

# ----------------------
# 📌 Backend Settings
# ----------------------
SS_SC = {
    "Sector": ["Public", "Private"],
    "Gender": ["M", "F"],
    "Frequency": ["Monthly", "Quarterly"]
}

PublicMonths = 500
PrivateMonths = 6
mortality_factor = 10.5
arrears_months = =ROUND(IF(OR($C$6 = "PUBLIC", $C$6 = "STATE"),IF(YEARFRAC($C$13, $C$14, 1) * 12 > 500, 500, YEARFRAC($C$13, $C$14, 1) * 12),IF(YEARFRAC($C$13, $C$14, 1) * 12 > 6, 6, YEARFRAC($C$13, $C$14, 1) * 12)),0)  # Example default value for max allowable arrears

# ----------------------
# 🧮 Pension Calculation Logic
# ----------------------
def calculate_final_salary(annual_salary):
    return annual_salary / 12

def calculate_pension(rsa_balance, final_salary, sector):
    months = PublicMonths if sector == "Public" else PrivateMonths
    annuity = rsa_balance / (months * mortality_factor / 12)
    min_pension = max(annuity, 0)
    return round(min_pension, 2)

def calculate_age(birth_date, ref_date):
    return ref_date.year - birth_date.year - ((ref_date.month, ref_date.day) < (birth_date.month, birth_date.day))

# ----------------------
# 📋 RPWT Section A – Editable Input
# ----------------------
st.markdown("### 📋 RPWT Version 3.0 Form (Sections A – G)")

with st.expander("✍️ Section A - Retiree Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        rsa_balance = st.number_input("RSA Balance (₦)", min_value=0.0, format="%.2f", step=1000.0)
        annual_salary = st.number_input("Annual Salary (₦)", min_value=0.0, format="%.2f", step=1000.0)
        dob = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", SS_SC["Gender"])
        selection = st.selectbox("Sector", SS_SC["Sector"])
    with col2:
        retirement_date = st.date_input("Retirement Date")
        program_date = st.date_input("Date of Programming", dt.date.today())
        frequency = st.selectbox("Payment Frequency", SS_SC["Frequency"])

# Live backend-calculated values
final_salary = calculate_final_salary(annual_salary)
lump_sum = rsa_balance * 0.25
monthly_pension = calculate_pension(rsa_balance, final_salary, selection)
current_age = calculate_age(dob, dt.date.today())
age_at_retirement = calculate_age(dob, retirement_date)

# ----------------------
# Section B – Validated & Derived Data
# ----------------------
with st.expander("📄 Section B - Validated & Derived Information", expanded=False):
    st.write(f"**Validated Annual Salary:** ₦{annual_salary:,.2f}")
    st.write(f"**Maximum Allowable Months in Arrears:** {arrears_months} months")
    st.write(f"**Current Age:** {current_age} years")
    st.write(f"**Age at Retirement:** {age_at_retirement} years")

# ----------------------
# Section C – Regulatory Limits
# ----------------------
with st.expander("📐 Section C - Pension Limits & Tests", expanded=False):
    st.write(f"**Final Monthly Salary:** ₦{final_salary:,.2f}")
    st.write(f"**Proposed Lump Sum (25%):** ₦{lump_sum:,.2f}")
    st.write(f"**Proposed Monthly Pension:** ₦{monthly_pension:,.2f}")
    st.write("**Minimum Monthly Pension Threshold:** ₦30,000")
    st.write("**Result:** ✅ PASS" if monthly_pension >= 30000 else "**Result:** ❌ FAIL")

# ----------------------
# Section D – Editable Summary
# ----------------------
with st.expander("📊 Section D - Computation Summary", expanded=True):
    st.write(f"**RSA Balance:** ₦{rsa_balance:,.2f}")
    st.write(f"**Annual Salary:** ₦{annual_salary:,.2f}")
    st.write(f"**Final Monthly Salary:** ₦{final_salary:,.2f}")
    st.write(f"**Monthly Pension:** ₦{monthly_pension:,.2f}")
    st.write(f"**Lump Sum (25%):** ₦{lump_sum:,.2f}")
    st.write("**Payment Frequency:** " + frequency)

# ----------------------
# 📎 Footer
# ----------------------
st.markdown("---")
st.caption("Designed by Aliyu S. Sani | PenCom RPWT v3.0 | August 2025")
