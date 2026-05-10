import pandas as pd
import yfinance as yf


DEFAULT_TICKERS = {
    "SPY": "US Equity",
    "LQD": "Investment Grade Credit",
    "HYG": "High Yield Credit",
    "TLT": "Treasury Duration",
    "GLD": "Gold",
    "SMH": "AI Infrastructure",
    "BIL": "Cash Proxy"
}


def download_adjusted_prices(
    tickers=None,
    start_date="2007-01-01",
    end_date=None
):
    """
    Download adjusted close prices from Yahoo Finance.

    Parameters
    ----------
    tickers : list or None
        List of ticker symbols. If None, use default universe.
    start_date : str
        Start date for price history.
    end_date : str or None
        End date for price history.

    Returns
    -------
    pd.DataFrame
        Daily adjusted close prices.
    """

    if tickers is None:
        tickers = list(DEFAULT_TICKERS.keys())

    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"].copy()
    else:
        prices = data[["Close"]].copy()
        prices.columns = tickers

    prices = prices.sort_index()
    prices.index.name = "Date"

    return prices


def clean_price_data(prices):
    """
    Clean price data by removing empty rows and forward filling missing values.
    """

    prices = prices.copy()
    prices = prices.dropna(how="all")
    prices = prices.ffill()
    prices = prices.dropna()

    return prices


def convert_to_monthly_prices(daily_prices, drop_incomplete_current_month=True):
    """
    Convert daily prices to completed month end prices.

    The current calendar month is excluded by default because it only contains
    month to date data and should not be treated as a completed monthly return.
    """

    monthly_prices = daily_prices.resample("ME").last()
    monthly_prices = monthly_prices.dropna()

    if drop_incomplete_current_month:
        current_month = pd.Timestamp.today().to_period("M")
        monthly_prices = monthly_prices[
            monthly_prices.index.to_period("M") < current_month
        ]

    return monthly_prices

def calculate_monthly_returns(monthly_prices):
    """
    Calculate monthly simple returns.
    """

    monthly_returns = monthly_prices.pct_change().dropna()

    return monthly_returns


def save_dataframes(
    daily_prices,
    monthly_prices,
    monthly_returns,
    raw_path="data/raw/asset_prices.csv",
    monthly_price_path="data/processed/monthly_prices.csv",
    monthly_return_path="data/processed/monthly_returns.csv"
):
    """
    Save data outputs to CSV.
    """

    daily_prices.to_csv(raw_path)
    monthly_prices.to_csv(monthly_price_path)
    monthly_returns.to_csv(monthly_return_path)