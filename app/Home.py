from pathlib import Path
import streamlit as st
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MONTHLY_RETURNS_PATH = PROJECT_ROOT / "data" / "processed" / "monthly_returns.csv"
MONTHLY_PRICES_PATH = PROJECT_ROOT / "data" / "processed" / "monthly_prices.csv"

st.set_page_config(
    page_title="AI Enhanced TPM",
    page_icon="📊",
    layout="wide"
)

st.title("AI Enhanced Total Portfolio Management")

st.markdown("""
This dashboard supports a Python based total portfolio management framework.

The first version focuses on market data, asset returns, and ETF proxy validation.
Later pages will add portfolio construction, dynamic rebalancing, credit regime signals,
stress testing, and AI generated CIO style commentary.
""")

st.subheader("Current Data Status")

if MONTHLY_RETURNS_PATH.exists() and MONTHLY_PRICES_PATH.exists():
    monthly_returns = pd.read_csv(MONTHLY_RETURNS_PATH, parse_dates=["Date"])
    monthly_prices = pd.read_csv(MONTHLY_PRICES_PATH, parse_dates=["Date"])

    start_date = monthly_returns["Date"].min().date()
    end_date = monthly_returns["Date"].max().date()
    asset_count = len(monthly_returns.columns) - 1
    month_count = len(monthly_returns)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Start Date", str(start_date))
    col2.metric("End Date", str(end_date))
    col3.metric("Assets", asset_count)
    col4.metric("Monthly Observations", month_count)

    st.success("Market data files are available and ready for analysis.")
else:
    st.error("Market data files are missing. Run: python scripts/run_data_pipeline.py")

st.subheader("Project Roadmap")

st.markdown("""
1. Market data pipeline
2. Asset level risk and return analysis
3. Static benchmark portfolio
4. Dynamic TPM strategy with credit and trend signals
5. AI infrastructure sleeve analysis
6. Stress testing
7. AI generated CIO memo
""")