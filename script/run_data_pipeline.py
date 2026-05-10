from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.data_loader import (
    DEFAULT_TICKERS,
    download_adjusted_prices,
    clean_price_data,
    convert_to_monthly_prices,
    calculate_monthly_returns,
    save_dataframes,
)


def main():
    raw_dir = PROJECT_ROOT / "data" / "raw"
    processed_dir = PROJECT_ROOT / "data" / "processed"

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    tickers = list(DEFAULT_TICKERS.keys())

    print("Starting data pipeline")
    print("Tickers:", tickers)

    daily_prices_raw = download_adjusted_prices(
        tickers=tickers,
        start_date="2007-01-01",
    )

    print("Raw daily prices shape:", daily_prices_raw.shape)

    missing_summary = pd.DataFrame({
        "missing_count": daily_prices_raw.isna().sum(),
        "missing_pct": daily_prices_raw.isna().mean().round(4),
    })

    missing_summary_path = processed_dir / "missing_summary.csv"
    missing_summary.to_csv(missing_summary_path)

    daily_prices = clean_price_data(daily_prices_raw)
    monthly_prices = convert_to_monthly_prices(daily_prices)
    monthly_returns = calculate_monthly_returns(monthly_prices)

    save_dataframes(
        daily_prices=daily_prices,
        monthly_prices=monthly_prices,
        monthly_returns=monthly_returns,
        raw_path=raw_dir / "asset_prices.csv",
        monthly_price_path=processed_dir / "monthly_prices.csv",
        monthly_return_path=processed_dir / "monthly_returns.csv",
    )

    print("Clean daily prices shape:", daily_prices.shape)
    print("Monthly prices shape:", monthly_prices.shape)
    print("Monthly returns shape:", monthly_returns.shape)

    print("Start date:", monthly_returns.index.min())
    print("End date:", monthly_returns.index.max())

    print("Saved:")
    print(raw_dir / "asset_prices.csv")
    print(processed_dir / "monthly_prices.csv")
    print(processed_dir / "monthly_returns.csv")
    print(processed_dir / "missing_summary.csv")


if __name__ == "__main__":
    main()