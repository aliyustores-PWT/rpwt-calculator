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
