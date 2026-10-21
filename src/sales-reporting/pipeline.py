from pathlib import Path

from metrics.sales_metrics import calculate_sales_metrics
from output.excel_report import generate_excel_report
from sources.csv_sources import load_csv_data
from sources.excel_sources import load_excel_data
from validation.sales_validator import validate_sales_data

from config import load_config


def run_pipeline(config_input=None):
    """
    Executes the complete end-to-end sales reporting automation pipeline.
    Accepts either a config path (str/Path) or a pre-loaded config dictionary.
    """

    print("=" * 50)
    print("STARTING SALES REPORTING AUTOMATION PIPELINE")
    print("=" * 50)

    if isinstance(config_input, dict):
        config = config_input  
    else:
        if config_input is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            config_input = project_root / "config" / "default.json"
        config = load_config(config_input)
        
    source_type = config["source"]["type"].lower()
    if source_type == "csv":
        raw_df = load_csv_data(config)
    elif source_type == "excel":
        raw_df = load_excel_data(config)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")

    valid_df, invalid_df = validate_sales_data(raw_df)

    metrics = calculate_sales_metrics(valid_df)

    output_path = generate_excel_report(metrics, invalid_df, config)

    print("=" * 50)
    print("PIPELINE EXECUTED SUCCESSFULLY!")
    print(f"Final Report Location: {output_path}")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()
