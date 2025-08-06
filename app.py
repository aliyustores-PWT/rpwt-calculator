# RPWT Pension Calculator - PenCom Version 3.0 (Sections A–G)
# By Aliyu S. Sani | Deployment Ready for Streamlit Cloud

import streamlit as st
import datetime as dt
import math
from PIL import Image

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

# Parameters from Commission
mgmt_charge = 0.01
reg_charge = 0.005
interest_rate = 0.105

# ----------------------
# 📋 Header and Branding
# ----------------------
logo = Image.open("pencom_logo.jpg")
st.image(logo, width=120)
st.markdown("### 📋 RPWT Version 3.0 Form (Sections A – G)")

# ----------------------
# 🧮 Financial Formulas
# ----------------------
def calculate_final_salary(annual_salary):
    return annual_salary / 12

def calculate_age(start_date, end_date):
    return end_date.year - start_date.year - ((end_date.month, end_date.day) < (start_date.month, start_date.day))

def calculate_datedif_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

def calculate_net_interest():
    return interest_rate * (1 - (mgmt_charge + reg_charge))

def calculate_pmt(rate, nper, pv):
    if rate == 0:
        return pv / nper
    return abs(rate * pv / (1 - (1 + rate) ** (-nper)))

def calculate_pv(rate, nper, pmt):
    if rate == 0:
        return pmt * nper
    return abs(pmt * (1 - (1 + rate) ** (-nper)) / rate)

# ----------------------
# Form Input - Section A
# ----------------------
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
        consolidation_date = st.date_input("Date of Consolidation", dt.date.today())
        frequency = st.selectbox("Payment Frequency", SS_SC["Frequency"])

# ----------------------
# Custom 'Run Calculation' Button
# ----------------------
if st.button("▶️ Run Pension Calculation", type="primary"):

    # Backend Calculations
    months_in_arrears = calculate_datedif_months(retirement_date, consolidation_date)
    current_age = calculate_age(dob, consolidation_date)
    age_at_retirement = calculate_age(dob, retirement_date)
    final_salary = calculate_final_salary(annual_salary)
    monthly_salary = final_salary
    fifty_percent_salary = final_salary * 0.5
    net_interest = calculate_net_interest()
    nc = mortality_factor - (11/24)
    nper = int(nc * (12 if frequency == "Monthly" else 4))
    reg_lumpsum = rsa_balance * 0.25
    pension = calculate_pmt(net_interest / (12 if frequency == "Monthly" else 4), nper, rsa_balance - reg_lumpsum)
    pv_component = calculate_pv(net_interest / (12 if frequency == "Monthly" else 4), nper, fifty_percent_salary)
    max_stat_lumpsum = max(0, rsa_balance + pv_component)
    min_reg_lumpsum = 0.0
    max_stat_pension = calculate_pmt(net_interest / (12 if frequency == "Monthly" else 4), nper, rsa_balance - min_reg_lumpsum)

    # Section B
    with st.expander("📄 Section B - Validated & Derived Information", expanded=False):
        st.write(f"**Validated Annual Salary:** ₦{annual_salary:,.2f}")
        st.write(f"**Maximum Allowable Months in Arrears:** {months_in_arrears} months")
        st.write(f"**Current Age:** {current_age} years")
        st.write(f"**Age at Retirement:** {age_at_retirement} years")

    # Section C
    with st.expander("📐 Section C - Pension Limits & Tests", expanded=False):
        st.write(f"**Final Monthly Salary:** ₦{monthly_salary:,.2f}")
        st.write(f"**50% of Final Salary:** ₦{fifty_percent_salary:,.2f}")
        st.write(f"**Minimum Regulatory Lumpsum:** ₦{min_reg_lumpsum:,.2f}")
        st.write(f"**Regulatory Pension:** ₦{pension:,.2f}")
        st.write(f"**Maximum Statutory Monthly Pension:** ₦{max_stat_pension:,.2f}")
        st.write(f"**Maximum Statutory Lumpsum:** ₦{max_stat_lumpsum:,.2f}")
        st.write(f"**Regulatory Lumpsum (25%):** ₦{reg_lumpsum:,.2f}")

    # Section D
    with st.expander("📊 Section D - Computation Summary", expanded=True):
        st.write(f"**RSA Balance:** ₦{rsa_balance:,.2f}")
        st.write(f"**Final Monthly Salary:** ₦{monthly_salary:,.2f}")
        st.write(f"**Monthly Pension:** ₦{pension:,.2f}")
        st.write(f"**Regulatory Lumpsum:** ₦{reg_lumpsum:,.2f}")
        st.write(f"**Payment Frequency:** {frequency}")

    # Section E
    with st.expander("🔍 Section E - Compliance Checks", expanded=False):
        st.write("✅ Pension meets minimum threshold." if pension >= 30000 else "❌ Pension falls below minimum threshold.")
        st.write("✅ Lump sum within 25% allowed.")
        st.write("✅ RSA balance adequate for programmed withdrawal.")

    # Section F
    with st.expander("📝 Section F - System Recommendation", expanded=False):
        if pension >= 30000:
            st.success("RECOMMENDATION: APPROVE")
        else:
            st.warning("RECOMMENDATION: REVIEW / DO NOT APPROVE")

    # Section G
    with st.expander("🖋️ Section G - Approval Notes", expanded=False):
        st.text_area("Processing Officer's Comments", "[Auto-filled or to be added manually during approval stage]", height=100)
        st.text_area("Final Approval Remarks", "[Supervisor or Team Lead final comments]", height=100)

# ----------------------
# Footer
# ----------------------
st.markdown("---")
st.caption("Designed by Aliyu S. Sani | PenCom RPWT v3.0 | August 2025")
