from pathlib import Path

import pandas as pd


def load_csv_data(config):
    """
    Load raw CSV data using paths and column mappings from the configuration.
    """

    project_root = Path(__file__).resolve().parent.parent.parent.parent

    raw_path = config["source"]["path"]
    file_path = Path(raw_path)

    if not file_path.absolute():
        file_path = project_root / raw_path

    if file_path.is_dir():
        csv_files = list(file_path.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(
                f"No CSV files found in directory: {file_path.absolute()}"
            )
        file_path = csv_files[0]

    if not file_path.exists():
        raise FileNotFoundError(
            f"Source CSV file not found at: {file_path.absolute()}."
        )

    print(f"Reading CSV file from: {file_path}")
    df = pd.read_csv(file_path)

    column_mapping = config["columns"]

    inverted_mapping = {v: k for k, v in column_mapping.items()}

    missing_columns = [col for col in inverted_mapping if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns in CSV: {missing_columns}.")

    df = df.rename(columns=inverted_mapping)

    print(f"Successfully loaded and normalized {len(df)} rows from CSV.")
    return df


if __name__ == "__main__":
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from config import load_config

    cfg = load_config()
    df_data = load_csv_data(cfg)
    print("\nPreview of normalized data:")
    print(df_data.head(10))
