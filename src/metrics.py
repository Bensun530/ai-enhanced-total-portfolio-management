import pandas as pd
import numpy as np


def calculate_cumulative_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cumulative returns from periodic simple returns.
    """

    cumulative_returns = (1 + returns).cumprod()

    return cumulative_returns


def calculate_drawdowns(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate drawdown series from periodic simple returns.
    """

    cumulative_returns = calculate_cumulative_returns(returns)
    running_max = cumulative_returns.cummax()
    drawdowns = cumulative_returns / running_max - 1

    return drawdowns


def calculate_max_drawdown(returns: pd.Series) -> float:
    """
    Calculate maximum drawdown for one return series.
    """

    cumulative_returns = (1 + returns).cumprod()
    running_max = cumulative_returns.cummax()
    drawdowns = cumulative_returns / running_max - 1

    return drawdowns.min()


def calculate_annualized_return(returns: pd.Series, periods_per_year: int = 12) -> float:
    """
    Calculate annualized compound return.
    """

    returns = returns.dropna()
    n_periods = len(returns)

    if n_periods == 0:
        return np.nan

    total_return = (1 + returns).prod()
    annualized_return = total_return ** (periods_per_year / n_periods) - 1

    return annualized_return


def calculate_annualized_volatility(returns: pd.Series, periods_per_year: int = 12) -> float:
    """
    Calculate annualized volatility.
    """

    return returns.dropna().std() * np.sqrt(periods_per_year)


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_returns: pd.Series | None = None,
    periods_per_year: int = 12
) -> float:
    """
    Calculate annualized Sharpe ratio.

    If risk free returns are provided, use excess returns.
    Otherwise, use raw returns.
    """

    returns = returns.dropna()

    if risk_free_returns is not None:
        aligned = pd.concat([returns, risk_free_returns], axis=1).dropna()
        excess_returns = aligned.iloc[:, 0] - aligned.iloc[:, 1]
    else:
        excess_returns = returns

    annualized_excess_return = calculate_annualized_return(
        excess_returns,
        periods_per_year=periods_per_year
    )

    annualized_volatility = calculate_annualized_volatility(
        excess_returns,
        periods_per_year=periods_per_year
    )

    if annualized_volatility == 0:
        return np.nan

    return annualized_excess_return / annualized_volatility


def calculate_asset_summary(
    monthly_returns: pd.DataFrame,
    risk_free_column: str = "BIL"
) -> pd.DataFrame:
    """
    Calculate asset level risk and return summary.
    """

    summary_rows = []

    if risk_free_column in monthly_returns.columns:
        risk_free_returns = monthly_returns[risk_free_column]
    else:
        risk_free_returns = None

    for ticker in monthly_returns.columns:
        returns = monthly_returns[ticker].dropna()

        annualized_return = calculate_annualized_return(returns)
        annualized_volatility = calculate_annualized_volatility(returns)
        sharpe_ratio = calculate_sharpe_ratio(
            returns,
            risk_free_returns=risk_free_returns
        )
        max_drawdown = calculate_max_drawdown(returns)

        summary_rows.append({
            "Ticker": ticker,
            "Annualized Return": annualized_return,
            "Annualized Volatility": annualized_volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown": max_drawdown,
            "Best Month": returns.max(),
            "Worst Month": returns.min(),
            "Positive Month Rate": (returns > 0).mean()
        })

    summary = pd.DataFrame(summary_rows)

    return summary


def calculate_correlation_matrix(monthly_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate asset return correlation matrix.
    """

    return monthly_returns.corr()