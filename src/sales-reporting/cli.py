import argparse
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
if str(current_dir.parent) not in sys.path:
    sys.path.append(str(current_dir.parent))

from pipeline import run_pipeline


def main():
    """
    Command-line interface entry point for the Sales Reporting Automation Toolkit.
    """

    parser = argparse.ArgumentParser(
        description="Automated Sales Reporting Toolkit - Converts raw CSV/Excel sales data into validated, structured reports."
    )

    parser.add_argument(
        "--config",
        type=str,
        default="../../config/cli_default.json",
        help="Path to the JSON configuration file (default: config/cli_default.json)",
    )

    args = parser.parse_args()

    try:
        run_pipeline(config_input=args.config)
    except Exception as e:
        print(f"\n[ERROR] Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
