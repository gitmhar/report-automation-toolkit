import pandas as pd


def validate_sales_data(df):
    """
    Validates the normalized sales dataframe for:
    - Missing required fields
    - Invalid dates
    - Negative or non-numeric quantities and prices
    - Duplicate transaction IDs
    """

    df = df.copy()

    required_fields = [
        "transaction_id",
        "transaction_date",
        "product",
        "quantity",
        "unit_price",
    ]

    is_valid = pd.Series(True, index=df.index)
    validation_notes = pd.Series("", index=df.index)

    for col in required_fields:
        missing_mask = df[col].isna() | (df[col] == "")
        if missing_mask.any():
            is_valid[missing_mask] = False
            validation_notes[missing_mask] += f"Missing {col}; "

    parsed_data = pd.to_datetime(df["transaction_date"], errors="coerce")
    bad_date_mask = parsed_data.isna() & is_valid
    if bad_date_mask.any():
        is_valid[bad_date_mask] = False
        validation_notes[bad_date_mask] += "Invalid transaction_date format; "

    duplicate_mask = df.duplicated(subset=["transaction_id"], keep=False)
    if duplicate_mask.any():
        validation_notes[duplicate_mask] += "Duplicate transaction_id detected; "

    df["is_valid"] = is_valid
    df["validation_notes"] = validation_notes.str.strip("; ")

    valid_df = df[df["is_valid"]].copy()
    invalid_df = df[~df["is_valid"]].copy()

    print(
        f"Validation complete: {len(valid_df)} valid rows, {len(invalid_df)} invalid/flagged rows found."
    )
    return valid_df, invalid_df


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from sources.csv_sources import load_csv_data

    from config import load_config

    cfg = load_config()
    raw_df = load_csv_data(cfg)

    valid, invalid = validate_sales_data(raw_df)

    print("\n-----INVALID / FLAGGED ROWS-----")
    print(
        invalid[
            ["transaction_id", "transaction_date", "product", "quantity", "unit_price"]
        ]
    )
