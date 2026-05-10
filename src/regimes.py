import pandas as pd
import numpy as np


def calculate_rolling_return(returns: pd.Series, window: int) -> pd.Series:
    """
    Calculate rolling compound return.
    """

    rolling_return = (1 + returns).rolling(window).apply(np.prod, raw=True) - 1

    return rolling_return


def calculate_credit_momentum(
    monthly_returns: pd.DataFrame,
    high_yield_col: str = "HYG",
    investment_grade_col: str = "LQD",
    window: int = 3
) -> pd.Series:
    """
    Calculate high yield versus investment grade credit momentum.

    Positive value means HYG is outperforming LQD.
    Negative value means credit risk appetite is weakening.
    """

    hyg_rolling_return = calculate_rolling_return(
        monthly_returns[high_yield_col],
        window=window
    )

    lqd_rolling_return = calculate_rolling_return(
        monthly_returns[investment_grade_col],
        window=window
    )

    credit_momentum = hyg_rolling_return - lqd_rolling_return

    return credit_momentum


def calculate_hyg_lqd_ratio(
    monthly_prices: pd.DataFrame,
    high_yield_col: str = "HYG",
    investment_grade_col: str = "LQD"
) -> pd.Series:
    """
    Calculate HYG/LQD price ratio.
    """

    ratio = monthly_prices[high_yield_col] / monthly_prices[investment_grade_col]

    return ratio


def calculate_equity_trend(
    monthly_prices: pd.DataFrame,
    equity_col: str = "SPY",
    moving_average_window: int = 10
) -> pd.Series:
    """
    Calculate equity trend using price versus moving average.
    """

    moving_average = monthly_prices[equity_col].rolling(moving_average_window).mean()

    equity_trend = monthly_prices[equity_col] / moving_average - 1

    return equity_trend


def calculate_rolling_volatility(
    monthly_returns: pd.DataFrame,
    asset_col: str = "SPY",
    window: int = 12,
    periods_per_year: int = 12
) -> pd.Series:
    """
    Calculate rolling annualized volatility.
    """

    rolling_volatility = (
        monthly_returns[asset_col]
        .rolling(window)
        .std()
        * np.sqrt(periods_per_year)
    )

    return rolling_volatility


def classify_regime(row) -> str:
    """
    Classify market regime based on credit signal and equity trend.
    """

    credit_signal = row["Credit Signal"]
    equity_signal = row["Equity Trend Signal"]

    if credit_signal == "Positive" and equity_signal == "Positive":
        return "Risk On"

    if credit_signal == "Negative" and equity_signal == "Positive":
        return "Credit Warning"

    if credit_signal == "Negative" and equity_signal == "Negative":
        return "Risk Off"

    if credit_signal == "Positive" and equity_signal == "Negative":
        return "Recovery"

    return "Unknown"


def build_credit_regime_signals(
    monthly_prices: pd.DataFrame,
    monthly_returns: pd.DataFrame
) -> pd.DataFrame:
    """
    Build credit and equity regime signal table.
    """

    signals = pd.DataFrame(index=monthly_returns.index)

    signals["HYG_LQD_Ratio"] = calculate_hyg_lqd_ratio(monthly_prices)
    signals["Credit_Momentum_3M"] = calculate_credit_momentum(monthly_returns, window=3)
    signals["SPY_Trend_10M"] = calculate_equity_trend(monthly_prices, moving_average_window=10)
    signals["SPY_Rolling_Vol_12M"] = calculate_rolling_volatility(monthly_returns, window=12)

    signals["Credit Signal"] = np.where(
        signals["Credit_Momentum_3M"] > 0,
        "Positive",
        "Negative"
    )

    signals["Equity Trend Signal"] = np.where(
        signals["SPY_Trend_10M"] > 0,
        "Positive",
        "Negative"
    )

    signals["Regime"] = signals.apply(classify_regime, axis=1)

    signals = signals.dropna()

    return signals