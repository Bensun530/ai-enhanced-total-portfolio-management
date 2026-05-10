from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ASSET_SUMMARY_PATH = PROJECT_ROOT / "outputs" / "tables" / "asset_summary.csv"
CORRELATION_PATH = PROJECT_ROOT / "outputs" / "tables" / "correlation_matrix.csv"
CUMULATIVE_RETURNS_PATH = PROJECT_ROOT / "outputs" / "tables" / "cumulative_returns.csv"
DRAWDOWNS_PATH = PROJECT_ROOT / "outputs" / "tables" / "drawdowns.csv"


st.set_page_config(
    page_title="Asset Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("Asset Analytics")

st.markdown("""
This page evaluates the standalone risk and return profile of each asset in the total portfolio universe.
The purpose is to understand each asset's role before building portfolio allocation rules.
""")

required_files = [
    ASSET_SUMMARY_PATH,
    CORRELATION_PATH,
    CUMULATIVE_RETURNS_PATH,
    DRAWDOWNS_PATH
]

missing_files = [path for path in required_files if not path.exists()]

if missing_files:
    st.error("Asset analytics outputs are missing. Run: python scripts/run_asset_analysis.py")
    for path in missing_files:
        st.write(path)
    st.stop()


asset_summary = pd.read_csv(ASSET_SUMMARY_PATH)
correlation_matrix = pd.read_csv(CORRELATION_PATH, index_col=0)
cumulative_returns = pd.read_csv(CUMULATIVE_RETURNS_PATH, parse_dates=["Date"])
drawdowns = pd.read_csv(DRAWDOWNS_PATH, parse_dates=["Date"])


st.subheader("Asset Summary")

formatted_summary = asset_summary.copy()

st.dataframe(
    formatted_summary.style.format({
        "Annualized Return": "{:.2%}",
        "Annualized Volatility": "{:.2%}",
        "Sharpe Ratio": "{:.2f}",
        "Max Drawdown": "{:.2%}",
        "Best Month": "{:.2%}",
        "Worst Month": "{:.2%}",
        "Positive Month Rate": "{:.2%}"
    }),
    use_container_width=True
)


st.subheader("Key Metrics")

best_return_asset = asset_summary.loc[
    asset_summary["Annualized Return"].idxmax()
]

lowest_vol_asset = asset_summary.loc[
    asset_summary["Annualized Volatility"].idxmin()
]

worst_drawdown_asset = asset_summary.loc[
    asset_summary["Max Drawdown"].idxmin()
]

best_sharpe_asset = asset_summary.loc[
    asset_summary["Sharpe Ratio"].idxmax()
]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Highest Return",
    best_return_asset["Ticker"],
    f"{best_return_asset['Annualized Return']:.2%}"
)

col2.metric(
    "Lowest Volatility",
    lowest_vol_asset["Ticker"],
    f"{lowest_vol_asset['Annualized Volatility']:.2%}"
)

col3.metric(
    "Worst Drawdown",
    worst_drawdown_asset["Ticker"],
    f"{worst_drawdown_asset['Max Drawdown']:.2%}"
)

col4.metric(
    "Best Sharpe",
    best_sharpe_asset["Ticker"],
    f"{best_sharpe_asset['Sharpe Ratio']:.2f}"
)


st.subheader("Growth of $1")

cumulative_long = cumulative_returns.melt(
    id_vars="Date",
    var_name="Ticker",
    value_name="Growth of $1"
)

growth_fig = px.line(
    cumulative_long,
    x="Date",
    y="Growth of $1",
    color="Ticker",
    title="Cumulative Return by Asset"
)

st.plotly_chart(growth_fig, use_container_width=True)


st.subheader("Drawdown")

drawdown_long = drawdowns.melt(
    id_vars="Date",
    var_name="Ticker",
    value_name="Drawdown"
)

drawdown_fig = px.line(
    drawdown_long,
    x="Date",
    y="Drawdown",
    color="Ticker",
    title="Asset Drawdowns"
)

drawdown_fig.update_yaxes(tickformat=".0%")

st.plotly_chart(drawdown_fig, use_container_width=True)


st.subheader("Correlation Matrix")

corr_fig = px.imshow(
    correlation_matrix,
    text_auto=".2f",
    aspect="auto",
    title="Monthly Return Correlation Matrix"
)

st.plotly_chart(corr_fig, use_container_width=True)


st.subheader("Interpretation Guide")

st.markdown("""
| Metric | How to read it |
|---|---|
| Annualized Return | Long term compound return estimate based on monthly returns |
| Annualized Volatility | Realized return volatility scaled to one year |
| Sharpe Ratio | Return per unit of volatility, using BIL as cash proxy |
| Max Drawdown | Worst peak to trough loss |
| Positive Month Rate | Percentage of months with positive return |
| Correlation | Whether assets move together or diversify each other |
""")