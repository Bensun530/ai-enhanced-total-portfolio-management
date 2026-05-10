from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.portfolio import build_static_portfolios


def main():
    processed_dir = PROJECT_ROOT / "data" / "processed"
    output_table_dir = PROJECT_ROOT / "outputs" / "tables"

    output_table_dir.mkdir(parents=True, exist_ok=True)

    monthly_returns_path = processed_dir / "monthly_returns.csv"

    if not monthly_returns_path.exists():
        raise FileNotFoundError(
            "monthly_returns.csv not found. Run python scripts/run_data_pipeline.py first."
        )

    monthly_returns = pd.read_csv(
        monthly_returns_path,
        parse_dates=["Date"],
        index_col="Date",
    )

    results = build_static_portfolios(monthly_returns)

    results["portfolio_weights"].to_csv(
        output_table_dir / "static_portfolio_weights.csv",
        index=False,
    )

    results["portfolio_returns"].to_csv(
        output_table_dir / "static_portfolio_returns.csv",
    )

    results["portfolio_summary"].to_csv(
        output_table_dir / "static_portfolio_summary.csv",
        index=False,
    )

    results["cumulative_returns"].to_csv(
        output_table_dir / "static_portfolio_cumulative_returns.csv",
    )

    results["drawdowns"].to_csv(
        output_table_dir / "static_portfolio_drawdowns.csv",
    )

    print("Static portfolio construction completed.")
    print("Saved:")
    print(output_table_dir / "static_portfolio_weights.csv")
    print(output_table_dir / "static_portfolio_returns.csv")
    print(output_table_dir / "static_portfolio_summary.csv")
    print(output_table_dir / "static_portfolio_cumulative_returns.csv")
    print(output_table_dir / "static_portfolio_drawdowns.csv")

    print("")
    print("Portfolio summary:")
    print(results["portfolio_summary"])


if __name__ == "__main__":
    main()