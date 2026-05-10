from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.regimes import build_credit_regime_signals


def main():
    processed_dir = PROJECT_ROOT / "data" / "processed"
    output_table_dir = PROJECT_ROOT / "outputs" / "tables"

    output_table_dir.mkdir(parents=True, exist_ok=True)

    monthly_prices_path = processed_dir / "monthly_prices.csv"
    monthly_returns_path = processed_dir / "monthly_returns.csv"

    if not monthly_prices_path.exists():
        raise FileNotFoundError(
            "monthly_prices.csv not found. Run python scripts/run_data_pipeline.py first."
        )

    if not monthly_returns_path.exists():
        raise FileNotFoundError(
            "monthly_returns.csv not found. Run python scripts/run_data_pipeline.py first."
        )

    monthly_prices = pd.read_csv(
        monthly_prices_path,
        parse_dates=["Date"],
        index_col="Date"
    )

    monthly_returns = pd.read_csv(
        monthly_returns_path,
        parse_dates=["Date"],
        index_col="Date"
    )

    signals = build_credit_regime_signals(
        monthly_prices=monthly_prices,
        monthly_returns=monthly_returns
    )

    output_path = output_table_dir / "credit_regime_signals.csv"
    signals.to_csv(output_path)

    print("Credit regime signal engine completed.")
    print("Saved:")
    print(output_path)

    print("")
    print("Regime counts:")
    print(signals["Regime"].value_counts())

    print("")
    print("Latest signal:")
    print(signals.tail(1).T)


if __name__ == "__main__":
    main()