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
# 📌 Backend Settings
# ----------------------
SS_SC = {
    "Sector": ["Public", "Private"],
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
    min_pension = max(annuity, 30000)  # Replace with official logic if available
    return round(min_pension, 2)

# ----------------------
# 📋 Collapsible Sections A–G
# ----------------------
st.markdown("### 📋 RPWT Version 3.0 Form (Sections A – G)")

# SECTION A
with st.expander("✍️ Section A - Retiree Information", expanded=True):
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
        frequency = st.selectbox("Payment Frequency", SS_SC["Frequency"])

# SECTION B
with st.expander("📄 Section B - System Summary", expanded=False):
    st.info("This section will auto-display processed data from Section A (e.g., age at retirement, length of service, eligibility flags).")

# SECTION C
with st.expander("📐 Section C - Pension Test Results", expanded=False):
    st.info("This section will show system-calculated tests such as regulatory minimum pension, 25% withdrawal limits, and applicable thresholds.")

# SECTION D
with st.expander("📊 Section D - Computation Summary", expanded=True):
    final_salary = annual_salary / 12
    monthly_pension = calculate_pension(rsa_balance, final_salary, selection)
    st.write(f"**Final Monthly Salary:** ₦{final_salary:,.2f}")
    st.write(f"**Projected Monthly Pension:** ₦{monthly_pension:,.2f}")

# SECTION E
with st.expander("🔍 Section E - Compliance Checks", expanded=False):
    st.info("This section will validate pension compliance rules such as lump sum not exceeding 50%, and monthly pension not below threshold.")

# SECTION F
with st.expander("📝 Section F - Recommendation", expanded=False):
    st.info("System recommendation based on computation outcome: Approve | Review | Adjust RSA balance or programming date.")

# SECTION G
with st.expander("🖋️ Section G - Approval Notes", expanded=False):
    st.info("Final approval comments and observations by processing officer or team lead. Read-only in live environment.")

# ----------------------
# 📎 Footer
# ----------------------
st.markdown("---")
st.caption("Designed by Aliyu S. Sani | PenCom RPWT v3.0 | August 2025")
