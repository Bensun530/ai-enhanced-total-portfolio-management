from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.metrics import (
    calculate_asset_summary,
    calculate_correlation_matrix,
    calculate_cumulative_returns,
    calculate_drawdowns,
)


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
        index_col="Date"
    )

    asset_summary = calculate_asset_summary(monthly_returns)
    correlation_matrix = calculate_correlation_matrix(monthly_returns)
    cumulative_returns = calculate_cumulative_returns(monthly_returns)
    drawdowns = calculate_drawdowns(monthly_returns)

    asset_summary.to_csv(output_table_dir / "asset_summary.csv", index=False)
    correlation_matrix.to_csv(output_table_dir / "correlation_matrix.csv")
    cumulative_returns.to_csv(output_table_dir / "cumulative_returns.csv")
    drawdowns.to_csv(output_table_dir / "drawdowns.csv")

    print("Asset analysis completed.")
    print("Saved:")
    print(output_table_dir / "asset_summary.csv")
    print(output_table_dir / "correlation_matrix.csv")
    print(output_table_dir / "cumulative_returns.csv")
    print(output_table_dir / "drawdowns.csv")

    print("")
    print("Asset summary preview:")
    print(asset_summary)


if __name__ == "__main__":
    main()