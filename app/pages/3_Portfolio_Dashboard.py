from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SUMMARY_PATH = PROJECT_ROOT / "outputs" / "tables" / "static_portfolio_summary.csv"
WEIGHTS_PATH = PROJECT_ROOT / "outputs" / "tables" / "static_portfolio_weights.csv"
RETURNS_PATH = PROJECT_ROOT / "outputs" / "tables" / "static_portfolio_returns.csv"
CUMULATIVE_PATH = PROJECT_ROOT / "outputs" / "tables" / "static_portfolio_cumulative_returns.csv"
DRAWDOWN_PATH = PROJECT_ROOT / "outputs" / "tables" / "static_portfolio_drawdowns.csv"


st.set_page_config(
    page_title="Portfolio Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Portfolio Dashboard")

st.markdown("""
This page compares the first set of static total portfolio allocations.
Each portfolio is monthly rebalanced back to its target weights.
""")

required_files = [
    SUMMARY_PATH,
    WEIGHTS_PATH,
    RETURNS_PATH,
    CUMULATIVE_PATH,
    DRAWDOWN_PATH,
]

missing_files = [path for path in required_files if not path.exists()]

if missing_files:
    st.error("Portfolio outputs are missing. Run: python scripts/run_portfolio_construction.py")
    for path in missing_files:
        st.write(path)
    st.stop()


summary = pd.read_csv(SUMMARY_PATH)
weights = pd.read_csv(WEIGHTS_PATH)
portfolio_returns = pd.read_csv(RETURNS_PATH, parse_dates=["Date"])
cumulative_returns = pd.read_csv(CUMULATIVE_PATH, parse_dates=["Date"])
drawdowns = pd.read_csv(DRAWDOWN_PATH, parse_dates=["Date"])


st.subheader("Portfolio Summary")

st.dataframe(
    summary.style.format({
        "Annualized Return": "{:.2%}",
        "Annualized Volatility": "{:.2%}",
        "Sharpe Ratio": "{:.2f}",
        "Max Drawdown": "{:.2%}",
        "Best Month": "{:.2%}",
        "Worst Month": "{:.2%}",
        "Positive Month Rate": "{:.2%}",
    }),
    use_container_width=True
)


st.subheader("Key Portfolio Metrics")

best_return = summary.loc[summary["Annualized Return"].idxmax()]
best_sharpe = summary.loc[summary["Sharpe Ratio"].idxmax()]
lowest_vol = summary.loc[summary["Annualized Volatility"].idxmin()]
lowest_drawdown = summary.loc[summary["Max Drawdown"].idxmax()]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Highest Return",
    best_return["Portfolio"],
    f"{best_return['Annualized Return']:.2%}"
)

col2.metric(
    "Best Sharpe",
    best_sharpe["Portfolio"],
    f"{best_sharpe['Sharpe Ratio']:.2f}"
)

col3.metric(
    "Lowest Volatility",
    lowest_vol["Portfolio"],
    f"{lowest_vol['Annualized Volatility']:.2%}"
)

col4.metric(
    "Smallest Drawdown",
    lowest_drawdown["Portfolio"],
    f"{lowest_drawdown['Max Drawdown']:.2%}"
)


st.subheader("Portfolio Weights")

selected_portfolio = st.selectbox(
    "Select portfolio",
    sorted(weights["Portfolio"].unique())
)

selected_weights = weights[weights["Portfolio"] == selected_portfolio].copy()
selected_weights = selected_weights.sort_values("Weight", ascending=False)

weight_fig = px.bar(
    selected_weights,
    x="Asset",
    y="Weight",
    title=f"{selected_portfolio} Target Weights",
    text_auto=".1%"
)

weight_fig.update_yaxes(tickformat=".0%")

st.plotly_chart(weight_fig, use_container_width=True)

st.dataframe(
    selected_weights.style.format({"Weight": "{:.2%}"}),
    use_container_width=True
)


st.subheader("Cumulative Return")

cumulative_long = cumulative_returns.melt(
    id_vars="Date",
    var_name="Portfolio",
    value_name="Growth of $1"
)

cumulative_fig = px.line(
    cumulative_long,
    x="Date",
    y="Growth of $1",
    color="Portfolio",
    title="Static Portfolio Growth of $1"
)

st.plotly_chart(cumulative_fig, use_container_width=True)


st.subheader("Drawdown")

drawdown_long = drawdowns.melt(
    id_vars="Date",
    var_name="Portfolio",
    value_name="Drawdown"
)

drawdown_fig = px.line(
    drawdown_long,
    x="Date",
    y="Drawdown",
    color="Portfolio",
    title="Static Portfolio Drawdowns"
)

drawdown_fig.update_yaxes(tickformat=".0%")

st.plotly_chart(drawdown_fig, use_container_width=True)


st.subheader("Recent Monthly Portfolio Returns")

st.dataframe(
    portfolio_returns.tail(24).style.format({
        col: "{:.2%}" for col in portfolio_returns.columns if col != "Date"
    }),
    use_container_width=True
)


st.subheader("Interpretation")

st.markdown("""
Static_TPM is the base allocation.

AI_Tilt increases SMH exposure to test whether an AI infrastructure sleeve improves portfolio performance.

Defensive reduces risky assets and increases Treasury duration, investment grade credit, and cash.

Equal_Weight is a naive benchmark that gives every asset the same weight.

This page is still static. The next major step is dynamic rebalancing using credit signals and equity trend.
""")