import pandas as pd
from typing import Optional, Literal, Dict
# ... keep your existing imports/constants/classes ...

WOOLHOUSE_11_24 = 11.0 / 24.0  # monthly conversion adjustment from annual factor

def _pick_nx_dx_col(df: pd.DataFrame) -> pd.Series:
    """
    Try to find the nx/dx column in a sheet.
    Priority by name; else fall back to the 12th column (Excel VLOOKUP col_index_num=12).
    """
    candidates = [c for c in df.columns if str(c).strip().lower() in {"nx/dx", "nx_dx", "nxdx", "nx over dx", "nx:dx"}]
    if candidates:
        return df[candidates[0]]

    # If not named, mimic your VLOOKUP(C..., ..., 12):
    # Excel is 1-based; pandas is 0-based → index 11 is the 12th column.
    if df.shape[1] >= 12:
        return df.iloc[:, 11]

    raise ValueError("Cannot locate nx/dx column (named or 12th column).")

def load_mortality_df(file) -> pd.DataFrame:
    """
    Accepts CSV or Excel. Two supported layouts:

    A) Single table with columns:
       age, nx_dx_M, nx_dx_F [, ex_months_M, ex_months_F]
       → We'll compute ax_M = nx_dx_M - 11/24; ax_F = nx_dx_F - 11/24

    B) Excel with two sheets 'Male' and 'Female', each with an 'age' column and an nx/dx column
       (either named or in the 12th column). We merge on age and build ax_M/ax_F via 11/24 rule.
    """
    name = getattr(file, "name", "").lower()
    if name.endswith((".xlsx", ".xls")):
        xls = pd.ExcelFile(file)
        sheet_names = [s.lower() for s in xls.sheet_names]

        if "male" in sheet_names and "female" in sheet_names:
            male = xls.parse(xls.sheet_names[sheet_names.index("male")])
            female = xls.parse(xls.sheet_names[sheet_names.index("female")])

            # normalize columns
            for d in (male, female):
                d.columns = [str(c).strip() for c in d.columns]
                if "age" not in d.columns:
                    raise ValueError("Each sheet must include an 'age' column.")
                d = d.sort_values("age").reset_index(drop=True)

            nx_dx_M = _pick_nx_dx_col(male).rename("nx_dx_M")
            male = pd.concat([male[["age"]], nx_dx_M], axis=1)
            nx_dx_F = _pick_nx_dx_col(female).rename("nx_dx_F")
            female = pd.concat([female[["age"]], nx_dx_F], axis=1)

            df = pd.merge(male, female, on="age", how="inner")
            # Optional terms if you include them in extra sheets/cols; we won't assume here.

        else:
            # Single-sheet Excel: treat like CSV
            df = xls.parse(xls.sheet_names[0])
            df.columns = [str(c).strip() for c in df.columns]
    else:
        df = pd.read_csv(file)
        df.columns = [str(c).strip() for c in df.columns]

    # Case A: already has nx_dx_M / nx_dx_F
    if "nx_dx_M" in df.columns and "nx_dx_F" in df.columns:
        pass
    # Case B fallback: maybe you already computed ax_M/ax_F in the file
    elif "ax_M" in df.columns and "ax_F" in df.columns:
        # If ax_* are present, we can work with them directly.
        # Still, build nx_dx_* for reference using the inverse Woolhouse approx:
        df["nx_dx_M"] = df["ax_M"] + WOOLHOUSE_11_24
        df["nx_dx_F"] = df["ax_F"] + WOOLHOUSE_11_24
    else:
        # If neither present, try to infer both from a single nx/dx column (not typical).
        raise ValueError("Mortality table must provide nx_dx_M & nx_dx_F, or ax_M & ax_F, or Male/Female sheets.")

    if "ax_M" not in df.columns:
        df["ax_M"] = df["nx_dx_M"] - WOOLHOUSE_11_24
    if "ax_F" not in df.columns:
        df["ax_F"] = df["nx_dx_F"] - WOOLHOUSE_11_24

    # Keep optional remaining months if you add them
    for c in ["ex_months_M", "ex_months_F"]:
        if c not in df.columns:
            df[c] = pd.NA

    # Final tidy
    keep = ["age", "nx_dx_M", "nx_dx_F", "ax_M", "ax_F", "ex_months_M", "ex_months_F"]
    df = df[keep].sort_values("age").reset_index(drop=True)
    return df

def nearest_row_by_age(df: pd.DataFrame, age: float) -> pd.Series:
    nearest_age = int(round(age))
    nearest_age = max(min(nearest_age, int(df["age"].max())), int(df["age"].min()))
    row = df.loc[df["age"] == nearest_age]
    if row.empty:
        idx = (df["age"] - age).abs().idxmin()
        row = df.loc[[idx]]
    return row.squeeze()

def gendered_pension_factor_based(residual: float, gender: str, age_prog: float, mort_df: Optional[pd.DataFrame]) -> float:
    """
    Factor-based monthly pension using a_x^(12) ≈ (nx/dx) - 11/24 at 10.5%.
    """
    if residual <= 0:
        return 0.0
    if mort_df is None:
        # Fallback if table not provided
        ax = 140.0 if gender == "M" else 150.0
        return residual / ax
    row = nearest_row_by_age(mort_df, age_prog)
    ax = float(row["ax_M"] if gender == "M" else row["ax_F"])
    return residual / ax

def gendered_pension_interest_based(residual: float, gender: str, age_prog: float, mort_df: Optional[pd.DataFrame]) -> float:
    """
    Interest-based (PMT) using 10.5% and a term from table:
    - Prefer ex_months_* if provided
    - Else derive a term n so that annuity factor a(i,n) ≈ a_x^(12)
    """
    if residual <= 0:
        return 0.0
    if mort_df is None:
        n = 240 if gender == "F" else 220
        return pmt_from_term(residual, PROJECTED_RATE_PCT, n)

    row = nearest_row_by_age(mort_df, age_prog)
    ex_col = "ex_months_M" if gender == "M" else "ex_months_F"
    if ex_col in row and pd.notna(row[ex_col]):
        n = int(round(float(row[ex_col])))
    else:
        ax = float(row["ax_M"] if gender == "M" else row["ax_F"])
        n = derive_term_from_factor(ax, PROJECTED_RATE_PCT, cap=720)
    return pmt_from_term(residual, PROJECTED_RATE_PCT, n)
