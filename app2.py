# Force rebuild on Streamlit Cloud - 5th Aug
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("🧮 Revised Programmed Withdrawal Template (RPWT) v3.0")
st.markdown("**Only Section A & Section D are editable. All computations are automated.**")

uploaded_file = st.file_uploader("📤 Upload the RPWT Excel Template (Unprotected)", type=["xlsm", "xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name=None)

    if 'Variables' in df:
        variables_df = df['Variables']

        # Identify editable sections (A and D)
        section_a_rows = variables_df[variables_df.iloc[:, 0].astype(str).str.startswith('A')].copy()
        section_d_rows = variables_df[variables_df.iloc[:, 0].astype(str).str.startswith('D')].copy()

        # Display full Variables sheet
        st.markdown("### Full RPWT Variables Sheet")
        st.dataframe(variables_df, use_container_width=True, height=400)

        st.markdown("### 🟢 Section A – Editable Inputs")
        edited_section_a = st.data_editor(section_a_rows, num_rows="dynamic", use_container_width=True)

        st.markdown("### 🟢 Section D – Negotiated Arrears (Optional Input)")
        edited_section_d = st.data_editor(section_d_rows, num_rows="dynamic", use_container_width=True)

        st.success("✅ Sections A & D are editable. Other data are visible but locked.")
    else:
        st.error("❌ 'Variables' sheet not found in uploaded file.")
else:
    st.warning("📂 Please upload the RPWT Excel file to begin.")
