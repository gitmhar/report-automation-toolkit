from pathlib import Path

import pandas as pd


def generate_excel_report(metrics_result, invalid_df, config):
    """
    Generates a formatted multi-sheet Excel report containing:
    - High-level metrics
    - Product summary table
    - Monthly summary table
    - Data-quality / invalid rows findings
    """
    
    project_root = Path(__file__).resolve().parent.parent.parent.parent

    output_dir = project_root / config["output"]["directory"]
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "sales_report.xlsx"

    print(f"Generating Excel report at: {output_file}")

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        overview_data = pd.DataFrame(
            [
                {"Metric": "Total Units Sold", "Value": metrics_result["total_units"]},
                {
                    "Metric": "Total Gross Sales",
                    "Value": metrics_result["total_gross_sales"],
                },
            ]
        )
        overview_data.to_excel(writer, sheet_name="Overview", index=False)

        metrics_result["product_summary"].to_excel(
            writer, sheet_name="Product Summary", index=False
        )

        metrics_result["monthly_summary"].to_excel(
            writer, sheet_name="Monthly Summary", index=False
        )

        if not invalid_df.empty:
            invalid_df.to_excel(writer, sheet_name="Data Quality Issues", index=False)
        else:
            pd.DataFrame({"Message": ["No invalid rows detected."]}).to_excel(
                writer, sheet_name="Data Quality Issues", index=False
            )

    print("Excel report successfully generated and saved.")
    return output_file

if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    
    from metrics.sales_metrics import calculate_sales_metrics
    from sources.csv_sources import load_csv_data
    from validation.sales_validator import validate_sales_data

    from config import load_config
    
    cfg = load_config()
    raw_df = load_csv_data(cfg)
    valid_df, invalid_df = validate_sales_data(raw_df)
    metrics = calculate_sales_metrics(valid_df)
    
    generate_excel_report(metrics, invalid_df, cfg)