import pandas as pd


def calculate_sales_metrics(valid_df):
    """
    Performs deterministic sales calculations on the valid dataframe:
    - Gross line value (quantity * unit_price)
    - Total unites and total gross sales
    - Grouped summaries by product and calendar month
    """

    if valid_df.empty:
        print("Warning: No valid rows provided to metrics engine.")
        return {
            "total_units": 0,
            "total_gross_sales": 0.0,
            "product_summary": pd.DataFrame(),
            "monthly_summary": pd.DataFrame(),
        }

    df = valid_df.copy()

    df["gross_line_value"] = df["quantity"] * df["unit_price"]

    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["sales_month"] = df["transaction_date"].dt.to_period("M").astype(str)

    total_units = df["quantity"].sum()
    total_gross_sales = df["gross_line_value"].sum()

    product_summary = (
        df.groupby("product")
        .agg(
            total_units_sold=("quantity", "sum"),
            total_gross_sales=("gross_line_value", "sum"),
        )
        .reset_index()
        .sort_values(by="total_gross_sales", ascending=False)
    )

    monthly_summary = (
        df.groupby("sales_month")
        .agg(
            total_units_sold=("quantity", "sum"),
            total_gross_sales=("gross_line_value", "sum")
        )
        .reset_index()
        .sort_values(by="sales_month")
    )
    
    print("Metrics calculation complete successfully.")
    
    return {
        "processed_df": df,
        "total_units": total_units,
        "total_gross_sales": total_gross_sales,
        "product_summary": product_summary,
        "monthly_summary": monthly_summary
    }
    
if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from sources.csv_sources import load_csv_data
    from validation.sales_validator import validate_sales_data

    from config import load_config
    
    cfg = load_config()
    raw_df = load_csv_data(cfg)
    valid_df, _ = validate_sales_data(raw_df)
    
    metrics = calculate_sales_metrics(valid_df)
    
    print(f"\nTotal Units Sold: {metrics['total_units']}")
    print(f"Total Gross Sales: ${metrics['total_gross_sales']:,.2f}")
    
    print("\n--- PRODUCT SUMMARY ---")
    print(metrics["product_summary"])
    
    print("\n--- MONTHLY SUMMARY ---")
    print(metrics["monthly_summary"])