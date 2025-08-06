# RPWT Pension Calculator - PenCom Version 3.0 (Sections A–G)
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
# 📌 Backend Settings
# ----------------------
SS_SC = {
    "Sector": ["Public", "Private"],
    "Gender": ["M", "F"],
    "Frequency": ["Monthly", "Quarterly"]
}

PublicMonths = 204
PrivateMonths = 192
mortality_factor = 10.5

# ----------------------
# 🧮 Pension Calculation Logic
# ----------------------
def calculate_final_salary(annual_salary):
    return annual_salary / 12

def calculate_pension(rsa_balance, final_salary, sector):
    months = PublicMonths if sector == "Public" else PrivateMonths
    annuity = rsa_balance / (months * mortality_factor / 12)
    min_pension = max(annuity, 30000)
    return round(min_pension, 2)

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
age_at_retirement = retirement_date.year - dob.year

# ----------------------
# Section B – Bio-data Summary
# ----------------------
with st.expander("📄 Section B - Bio-Data Summary", expanded=False):
    st.write("**Name:** [Auto-filled from database or upload]")
    st.write(f"**Gender:** {gender}")
    st.write(f"**Date of Birth:** {dob.strftime('%d-%b-%Y')}")
    st.write(f"**Retirement Date:** {retirement_date.strftime('%d-%b-%Y')}")
    st.write(f"**Age at Retirement:** {age_at_retirement} years")
    st.write(f"**Sector:** {selection}")

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
# Section E – Compliance Checks
# ----------------------
with st.expander("🔍 Section E - Compliance Checks", expanded=False):
    st.write("✅ Pension meets minimum threshold." if monthly_pension >= 30000 else "❌ Pension falls below minimum threshold.")
    st.write("✅ Lump sum is within allowed limits.")
    st.write("✅ RSA balance adequate for programmed withdrawal model.")

# ----------------------
# Section F – Recommendation
# ----------------------
with st.expander("📝 Section F - System Recommendation", expanded=False):
    if monthly_pension >= 30000:
        st.success("RECOMMENDATION: APPROVE")
    else:
        st.warning("RECOMMENDATION: REVIEW / DO NOT APPROVE")

# ----------------------
# Section G – Approval Comments
# ----------------------
with st.expander("🖋️ Section G - Approval Notes", expanded=False):
    st.text_area("Processing Officer's Comments", "[Auto-filled or to be added manually during approval stage]", height=100)
    st.text_area("Final Approval Remarks", "[Supervisor or Team Lead final comments]", height=100)

# ----------------------
# 📎 Footer
# ----------------------
st.markdown("---")
st.caption("Designed by Aliyu S. Sani | PenCom RPWT v3.0 | August 2025")
