from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MONTHLY_PRICES_PATH = PROJECT_ROOT / "data" / "processed" / "monthly_prices.csv"
MONTHLY_RETURNS_PATH = PROJECT_ROOT / "data" / "processed" / "monthly_returns.csv"
MISSING_SUMMARY_PATH = PROJECT_ROOT / "data" / "processed" / "missing_summary.csv"

st.set_page_config(
    page_title="Market Data",
    page_icon="📈",
    layout="wide"
)

st.title("Market Data")

st.markdown("""
This page checks the ETF proxy dataset used in the total portfolio framework.
The goal is to confirm that the price data, monthly returns, and missing value treatment are clean before portfolio construction.
""")

if not MONTHLY_PRICES_PATH.exists() or not MONTHLY_RETURNS_PATH.exists():
    st.error("Market data files are missing. Run: python scripts/run_data_pipeline.py")
    st.stop()

monthly_prices = pd.read_csv(MONTHLY_PRICES_PATH, parse_dates=["Date"])
monthly_returns = pd.read_csv(MONTHLY_RETURNS_PATH, parse_dates=["Date"])

asset_columns = [col for col in monthly_returns.columns if col != "Date"]

start_date = monthly_returns["Date"].min().date()
end_date = monthly_returns["Date"].max().date()
asset_count = len(asset_columns)
month_count = len(monthly_returns)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Start Date", str(start_date))
col2.metric("End Date", str(end_date))
col3.metric("Assets", asset_count)
col4.metric("Monthly Return Rows", month_count)

st.subheader("Asset Universe")

asset_role_map = {
    "SPY": "US Equity",
    "LQD": "Investment Grade Credit",
    "HYG": "High Yield Credit",
    "TLT": "Treasury Duration",
    "GLD": "Gold",
    "SMH": "AI Infrastructure",
    "BIL": "Cash Proxy"
}

asset_table = pd.DataFrame({
    "Ticker": asset_columns,
    "Role": [asset_role_map.get(ticker, "Unknown") for ticker in asset_columns]
})

st.dataframe(asset_table, use_container_width=True)

st.subheader("Normalized Monthly Prices")

normalized_prices = monthly_prices.copy()
price_cols = [col for col in normalized_prices.columns if col != "Date"]
normalized_prices[price_cols] = normalized_prices[price_cols] / normalized_prices[price_cols].iloc[0]

normalized_long = normalized_prices.melt(
    id_vars="Date",
    value_vars=price_cols,
    var_name="Ticker",
    value_name="Growth of $1"
)

fig = px.line(
    normalized_long,
    x="Date",
    y="Growth of $1",
    color="Ticker",
    title="Growth of $1 by Asset"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Monthly Return Summary")

summary_rows = []

for ticker in asset_columns:
    returns = monthly_returns[ticker]
    annual_return = (1 + returns).prod() ** (12 / len(returns)) - 1
    annual_vol = returns.std() * (12 ** 0.5)
    sharpe = annual_return / annual_vol if annual_vol != 0 else None
    best_month = returns.max()
    worst_month = returns.min()

    summary_rows.append({
        "Ticker": ticker,
        "Annualized Return": annual_return,
        "Annualized Volatility": annual_vol,
        "Sharpe Ratio": sharpe,
        "Best Month": best_month,
        "Worst Month": worst_month
    })

summary_table = pd.DataFrame(summary_rows)

st.dataframe(
    summary_table.style.format({
        "Annualized Return": "{:.2%}",
        "Annualized Volatility": "{:.2%}",
        "Sharpe Ratio": "{:.2f}",
        "Best Month": "{:.2%}",
        "Worst Month": "{:.2%}"
    }),
    use_container_width=True
)

st.subheader("Monthly Returns")

st.dataframe(monthly_returns.tail(24), use_container_width=True)

st.subheader("Monthly Prices")

st.dataframe(monthly_prices.tail(24), use_container_width=True)

st.subheader("Missing Value Summary")

if MISSING_SUMMARY_PATH.exists():
    missing_summary = pd.read_csv(MISSING_SUMMARY_PATH)
    st.dataframe(missing_summary, use_container_width=True)
else:
    st.warning("Missing summary file not found.")