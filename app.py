# Backend constants and helper logic for RPWT v3.0
from dataclasses import dataclass
from datetime import date

SS_SC = {
    "Sector": ["Public", "Private"],
    "Gender": ["M", "F"],
    "Frequency": ["Monthly", "Quarterly"]
}

# As provided in your template notes
PUBLIC_MONTHS = 500
PRIVATE_MONTHS = 6

# Projected rate of return (%). In RPWT v3.0 this is 10.5%.
PROJECTED_RATE_PCT = 10.5

@dataclass
class RPWTInputs:
    sector: str
    gender: str
    frequency: str
    dob: date
    retirement_date: date
    programming_date: date
    annual_salary: float
    rsa_balance: float
    desired_lump_sum: float = 0.0
    method: str = "Factor-based"  # or "Finance-PMT"

def months_between(d1: date, d2: date) -> int:
    """Approximate whole months between two dates, non-negative."""
    if d2 < d1:
        d1, d2 = d2, d1
    years = d2.year - d1.year
    months = years * 12 + (d2.month - d1.month)
    if d2.day < d1.day:
        months -= 1
    return max(0, months)

def age_years(on_date: date, dob: date) -> float:
    if on_date < dob:
        return 0.0
    days = (on_date - dob).days
    return round(days / 365.25, 2)

def final_salary_monthly(annual_salary: float) -> float:
    return max(0.0, float(annual_salary) / 12.0)

def sector_months(sector: str) -> int:
    return PUBLIC_MONTHS if sector.lower() == "public" else PRIVATE_MONTHS

def arrears_months(sector: str, retirement_date: date, programming_date: date) -> int:
    cap = sector_months(sector)
    raw = months_between(retirement_date, programming_date)
    return min(cap, raw)

def annuity_factor_based(balance: float, sector: str) -> float:
    """
    Compatibility with the earlier pseudo-formula:
    annuity = balance / (months * mortality_factor / 12)
    Here we treat 'mortality_factor' as PROJECTED_RATE_PCT for parity with prior snippets.
    """
    months = sector_months(sector)
    mortality_factor = PROJECTED_RATE_PCT
    denom = (months * mortality_factor / 12.0)
    if denom <= 0:
        return 0.0
    return balance / denom

def annuity_pmt(balance: float, annual_rate_pct: float, months: int) -> float:
    """Standard finance PMT: PMT = P * r / (1 - (1+r)^-n), r is monthly rate."""
    if balance <= 0 or months <= 0:
        return 0.0
    r = (annual_rate_pct / 100.0) / 12.0
    if r == 0:
        return balance / months
    denom = 1 - (1 + r) ** (-months)
    if denom <= 0:
        return 0.0
    return balance * r / denom

def currency_fmt(x: float) -> str:
    return f"₦{x:,.2f}"
import streamlit as st
from datetime import date
from backend import (
    SS_SC, RPWTInputs, months_between, age_years, final_salary_monthly,
    sector_months, arrears_months, annuity_factor_based, annuity_pmt,
    PROJECTED_RATE_PCT, currency_fmt
)

st.set_page_config(page_title="RPWT v3.0 Pension Calculator", page_icon="📈", layout="centered")

st.title("RPWT v3.0 Pension Calculator • PenCom")
st.caption("Real-time calculator for Programmed Withdrawal (Version 3.0) — for testing & demonstration.")

with st.expander("About this tool", expanded=False):
    st.markdown(
        """
        - **Projected Rate of Return**: 10.5% (as per RPWT v3.0 notes).
        - **Sector-based months cap**: Public → 500 months; Private → 6 months.
        - **Arrears months** = min(cap by sector, months between **Retirement Date** and **Date of Programming**).
        - **Two methods** for monthly pension:
            1. **Factor-based** (compatibility with earlier pseudo-formula), and
            2. **Finance PMT** using 10.5% annual rate.
        - Results update as you type. Currency shows **₦** with 2 decimals.
        """
    )

st.subheader("Section A — Input Details")

col1, col2 = st.columns(2)
with col1:
    sector = st.selectbox("Sector", SS_SC["Sector"])
    gender = st.selectbox("Gender", SS_SC["Gender"])
    frequency = st.selectbox("Payment Frequency", SS_SC["Frequency"])

with col2:
    dob = st.date_input("Date of Birth", value=date(1970, 1, 1))
    retirement_date = st.date_input("Retirement Date", value=date(2025, 1, 1))
    programming_date = st.date_input("Date of Programming", value=date.today())

col3, col4 = st.columns(2)
with col3:
    annual_salary = st.number_input("Annual Salary (₦)", min_value=0.0, step=1000.0, format="%.2f")
with col4:
    rsa_balance = st.number_input("RSA Balance (₦)", min_value=0.0, step=1000.0, format="%.2f")

desired_lump_sum = st.number_input("Desired Lump Sum (₦) — optional", min_value=0.0, step=1000.0, format="%.2f")

method = st.radio(
    "Calculation Method",
    ["Factor-based", f"Finance-PMT @ {PROJECTED_RATE_PCT}%"],
    horizontal=True
)

# Prepare inputs
inp = RPWTInputs(
    sector=sector,
    gender=gender,
    frequency=frequency,
    dob=dob,
    retirement_date=retirement_date,
    programming_date=programming_date,
    annual_salary=annual_salary,
    rsa_balance=rsa_balance,
    desired_lump_sum=desired_lump_sum,
    method="Factor-based" if method == "Factor-based" else "Finance-PMT"
)

st.divider()
st.subheader("Derived Values & Checks")

age_ret = age_years(inp.retirement_date, inp.dob)
age_prog = age_years(inp.programming_date, inp.dob)
fsal = final_salary_monthly(inp.annual_salary)
cap_months = sector_months(inp.sector)
arr_m = arrears_months(inp.sector, inp.retirement_date, inp.programming_date)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Age at Retirement", f"{age_ret} yrs")
with c2:
    st.metric("Age at Programming", f"{age_prog} yrs")
with c3:
    st.metric("Final Salary (Monthly)", currency_fmt(fsal))

c4, c5, c6 = st.columns(3)
with c4:
    st.metric("Sector Months Cap", f"{cap_months} months")
with c5:
    st.metric("Arrears Months", f"{arr_m} months")
with c6:
    months_diff = months_between(inp.retirement_date, inp.programming_date)
    st.metric("Months Between Ret. & Prog.", f"{months_diff} months")

st.divider()
st.subheader("Pension Computation")

residual_balance = max(0.0, inp.rsa_balance - inp.desired_lump_sum)
if residual_balance < inp.rsa_balance and inp.desired_lump_sum > 0:
    st.info(f"Residual RSA after Lump Sum: {currency_fmt(residual_balance)}", icon="💡")

if inp.method == "Factor-based":
    monthly_pension = annuity_factor_based(residual_balance, inp.sector)
else:
    monthly_pension = annuity_pmt(residual_balance, PROJECTED_RATE_PCT, sector_months(inp.sector))

# Frequency adjustment
if inp.frequency == "Monthly":
    pension_per_period = monthly_pension
elif inp.frequency == "Quarterly":
    pension_per_period = monthly_pension * 3
else:
    pension_per_period = monthly_pension  # fallback

arrears_value = monthly_pension * arr_m

c7, c8, c9 = st.columns(3)
with c7:
    st.metric("Monthly Pension", currency_fmt(monthly_pension))
with c8:
    st.metric(f"Pension per {inp.frequency}", currency_fmt(pension_per_period))
with c9:
    st.metric("Arrears Value", currency_fmt(arrears_value))

st.divider()
st.subheader("Summary")

st.write(
    f"""
- **Sector**: {inp.sector}  •  **Gender**: {inp.gender}  •  **Frequency**: {inp.frequency}  
- **DOB**: {inp.dob}  •  **Retirement**: {inp.retirement_date}  •  **Programming**: {inp.programming_date}  
- **Annual Salary**: {currency_fmt(inp.annual_salary)}  •  **Final Salary (Monthly)**: {currency_fmt(fsal)}  
- **RSA Balance**: {currency_fmt(inp.rsa_balance)}  •  **Desired Lump Sum**: {currency_fmt(inp.desired_lump_sum)}  •  **Residual**: {currency_fmt(residual_balance)}  
- **Method**: {inp.method}  •  **Projected Return**: {PROJECTED_RATE_PCT}%  
- **Monthly Pension**: {currency_fmt(monthly_pension)}  •  **Arrears Months**: {arr_m}  •  **Arrears Value**: {currency_fmt(arrears_value)}
"""
)

st.caption("This tool is for guidance only. For regulatory use, validate with the official RPWT v3.0 Excel and PenCom circulars.")
