from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


def load_and_process_file(csv_path: Path) -> pd.DataFrame:
    """Load a CSV and return a DataFrame with columns Sales, Date, Region for Pink Morsels only.

    The input CSVs are expected to have columns: product, price, quantity, date, region.
    """
    data_frame = pd.read_csv(csv_path)

    # Filter for Pink Morsels (case-insensitive to be safe)
    is_pink_morsel = data_frame["product"].astype(str).str.lower() == "pink morsel"
    pink_only = data_frame.loc[is_pink_morsel].copy()

    if pink_only.empty:
        return pd.DataFrame(columns=["Sales", "Date", "Region"])  # consistent schema

    # Clean price like "$3.00" -> 3.00 and ensure numeric types
    pink_only["price"] = (
        pink_only["price"].astype(str).str.replace("$", "", regex=False).astype(float)
    )
    pink_only["quantity"] = pink_only["quantity"].astype(int)

    # Compute Sales = price * quantity
    pink_only["Sales"] = pink_only["price"] * pink_only["quantity"]

    # Select and rename columns to required output schema and casing
    result = pink_only.loc[:, ["Sales", "date", "region"]].rename(
        columns={"date": "Date", "region": "Region"}
    )

    return result


def process_all_inputs(data_directory: Path) -> pd.DataFrame:
    """Process all daily_sales_data_*.csv files within the provided data directory."""
    input_files = sorted(data_directory.glob("daily_sales_data_*.csv"))

    if not input_files:
        raise FileNotFoundError(
            f"No input files found in {data_directory} matching 'daily_sales_data_*.csv'"
        )

    processed_frames = [load_and_process_file(csv_path) for csv_path in input_files]
    combined = pd.concat(processed_frames, ignore_index=True)

    # Optional: sort for deterministic output
    if not combined.empty:
        combined = combined.sort_values(by=["Date", "Region"]).reset_index(drop=True)

    return combined


def main() -> int:
    repo_root = Path(__file__).parent
    data_dir = repo_root / "data"
    output_path = data_dir / "pink_morsel_sales.csv"

    data_dir.mkdir(parents=True, exist_ok=True)

    combined = process_all_inputs(data_dir)
    combined.to_csv(output_path, index=False)

    print(f"Wrote processed output -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


