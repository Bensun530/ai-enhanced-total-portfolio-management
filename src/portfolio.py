import pandas as pd
import numpy as np

from src.metrics import (
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_sharpe_ratio,
    calculate_max_drawdown,
    calculate_cumulative_returns,
    calculate_drawdowns,
)


STATIC_PORTFOLIOS = {
    "Static_TPM": {
        "SPY": 0.40,
        "LQD": 0.20,
        "HYG": 0.10,
        "TLT": 0.15,
        "GLD": 0.05,
        "SMH": 0.05,
        "BIL": 0.05,
    },
    "AI_Tilt": {
        "SPY": 0.35,
        "LQD": 0.18,
        "HYG": 0.10,
        "TLT": 0.12,
        "GLD": 0.05,
        "SMH": 0.15,
        "BIL": 0.05,
    },
    "Defensive": {
        "SPY": 0.25,
        "LQD": 0.25,
        "HYG": 0.05,
        "TLT": 0.25,
        "GLD": 0.05,
        "SMH": 0.05,
        "BIL": 0.10,
    },
}


def create_equal_weight_portfolio(asset_columns):
    """
    Create equal weight portfolio based on available assets.
    """

    weight = 1 / len(asset_columns)

    return {asset: weight for asset in asset_columns}


def validate_weights(weights, available_assets, tolerance=1e-6):
    """
    Validate that portfolio weights are usable.
    """

    missing_assets = [asset for asset in weights if asset not in available_assets]

    if missing_assets:
        raise ValueError(f"Portfolio contains assets not in return data: {missing_assets}")

    total_weight = sum(weights.values())

    if abs(total_weight - 1.0) > tolerance:
        raise ValueError(f"Weights must sum to 1. Current sum: {total_weight}")

    return True


def weights_to_dataframe(portfolio_weights):
    """
    Convert portfolio weight dictionary to a clean dataframe.
    """

    rows = []

    for portfolio_name, weights in portfolio_weights.items():
        for asset, weight in weights.items():
            rows.append({
                "Portfolio": portfolio_name,
                "Asset": asset,
                "Weight": weight,
            })

    return pd.DataFrame(rows)


def calculate_portfolio_returns(monthly_returns, weights):
    """
    Calculate monthly portfolio returns using constant monthly rebalanced weights.

    This assumes the portfolio is rebalanced back to target weights at each month end.
    """

    available_assets = list(monthly_returns.columns)
    validate_weights(weights, available_assets)

    ordered_assets = list(weights.keys())
    weight_vector = pd.Series(weights)

    portfolio_returns = monthly_returns[ordered_assets].dot(weight_vector)

    return portfolio_returns


def calculate_multiple_portfolio_returns(monthly_returns, portfolio_weights):
    """
    Calculate returns for multiple static portfolios.
    """

    portfolio_return_df = pd.DataFrame(index=monthly_returns.index)

    for portfolio_name, weights in portfolio_weights.items():
        portfolio_return_df[portfolio_name] = calculate_portfolio_returns(
            monthly_returns=monthly_returns,
            weights=weights,
        )

    return portfolio_return_df


def calculate_portfolio_summary(
    portfolio_returns,
    risk_free_returns=None,
    periods_per_year=12
):
    """
    Calculate portfolio level performance summary.
    """

    summary_rows = []

    for portfolio_name in portfolio_returns.columns:
        returns = portfolio_returns[portfolio_name].dropna()

        annualized_return = calculate_annualized_return(
            returns,
            periods_per_year=periods_per_year,
        )

        annualized_volatility = calculate_annualized_volatility(
            returns,
            periods_per_year=periods_per_year,
        )

        sharpe_ratio = calculate_sharpe_ratio(
            returns,
            risk_free_returns=risk_free_returns,
            periods_per_year=periods_per_year,
        )

        max_drawdown = calculate_max_drawdown(returns)

        summary_rows.append({
            "Portfolio": portfolio_name,
            "Annualized Return": annualized_return,
            "Annualized Volatility": annualized_volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown": max_drawdown,
            "Best Month": returns.max(),
            "Worst Month": returns.min(),
            "Positive Month Rate": (returns > 0).mean(),
        })

    return pd.DataFrame(summary_rows)


def build_static_portfolios(monthly_returns):
    """
    Build the first set of static portfolios.

    Static_TPM: base total portfolio
    AI_Tilt: higher AI infrastructure exposure
    Defensive: lower risky asset exposure
    Equal_Weight: naive benchmark
    """

    asset_columns = list(monthly_returns.columns)

    portfolio_weights = STATIC_PORTFOLIOS.copy()
    portfolio_weights["Equal_Weight"] = create_equal_weight_portfolio(asset_columns)

    for portfolio_name, weights in portfolio_weights.items():
        validate_weights(weights, asset_columns)

    portfolio_returns = calculate_multiple_portfolio_returns(
        monthly_returns=monthly_returns,
        portfolio_weights=portfolio_weights,
    )

    risk_free_returns = monthly_returns["BIL"] if "BIL" in monthly_returns.columns else None

    portfolio_summary = calculate_portfolio_summary(
        portfolio_returns=portfolio_returns,
        risk_free_returns=risk_free_returns,
    )

    cumulative_returns = calculate_cumulative_returns(portfolio_returns)
    drawdowns = calculate_drawdowns(portfolio_returns)
    weights_df = weights_to_dataframe(portfolio_weights)

    return {
        "portfolio_weights": weights_df,
        "portfolio_returns": portfolio_returns,
        "portfolio_summary": portfolio_summary,
        "cumulative_returns": cumulative_returns,
        "drawdowns": drawdowns,
    }