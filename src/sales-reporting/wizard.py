import shutil
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

project_root = Path(__file__).resolve().parent.parent.parent

module_dir = Path(__file__).resolve().parent
if str(module_dir) not in sys.path:
    sys.path.insert(0, str(module_dir))


from config import load_config

from .pipeline import run_pipeline


def select_file_from_desktop():
    """
    Open a native file dialog to let user pick any CSV or Excel file from anywhere on their computer (Downloads,Desktop, etc.)
    """
    print("Opening file selection window...")
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Select Sales Report File",
        filetypes=[
            ("Spreadsheets & Data", "*.csv;*.xlsx"),
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx"),
        ],
    )

    root.destroy()
    return file_path


def import_file_to_input(source_file_path):
    """
    Copies the user-selected file into the project's data/input directory.
    """
    src_path = Path(source_file_path)
    if not src_path.exists():
        raise FileNotFoundError(f"Selected file not found: {src_path}")

    input_dir = project_root / "data" / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    dest_path = input_dir / src_path.name

    # Copy file over
    shutil.copy2(src_path, dest_path)
    print(f"Successfully imported '{src_path}' into 'data/input/'")

    return dest_path


def list_and_choose_input_file():
    """
    Scans data/input for available data files and presents an enumerated list.
    """

    input_dir = project_root / "data" / "input"
    if not input_dir.exists():
        print("[ERROR] 'data/input' directory does not exist.")
        return

    files = [
        f
        for f in input_dir.iterdir()
        if f.is_file() and f.suffix.lower() in [".csv", ".xlsx", "xls"]
    ]

    if not files:
        print("[ERROR] No valid data files found in 'data/input'")
        return

    print("=" * 50)
    print("AVAILABLE FILES IN 'data/input':")
    print("=" * 50)

    for idx, file in enumerate(files, start=1):
        print(f"[{idx}] {file.name}")
    print("=" * 50)

    while True:
        prompt = f"Select a file number to generate report (1-{len(files)}): ".strip()
        choice = input(prompt)

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(files):
                selected_file = files[choice_idx]
                print(f"Selected: {selected_file}")
                return selected_file
            else:
                print("[WARNING] Invalid number. Please select from the list.")
        except ValueError:
            print("[WARNING] Please enter a valid integer number.")


def main():
    print("=" * 50)
    print("SALES REPORTING AUTOMATION WIZARD")
    print("=" * 50)

    config_path = project_root / "config" / "default.json"

    # Step 1: Report Type Selection Menu
    print("\nSelect Report Type:")
    print("1. Sales Summary Report")
    print("2. Inventory Report (Coming Soon)")
    print("3. Attendance Report (Coming Soon)")

    choice = input("\nEnter your choice(default 1): ").strip()
    if choice != "" and choice != "1":
        print(
            "[INFO] Only Sales Summary Report is implemented right now. Defaulting to Sales."
        )

    # Step 2: Choose file from anywhere on PC
    selected_file = select_file_from_desktop()
    if not selected_file:
        print("\n[WARNING] No file is selected. Operation cancelled.")
        return

    # Step 3: Copy file to data/input/
    imported_file_path = import_file_to_input(selected_file)

    # Step 4: Dynamic File Scanning & User Selection
    target_file = list_and_choose_input_file()
    if not target_file:
        return

    print(f"\nConfiguring pipeline for: {target_file.name}")
    config = load_config(config_path)

    config["source"]["path"] = str(target_file).replace("\\", "/")

    if target_file.suffix.lower() == ".csv":
        config["source"]["type"] = "csv"
    elif target_file.suffix.lower() in [".xlsx", ".xls"]:
        config["source"]["type"] = "excel"

    print("-" * 50)
    run_pipeline(config_input=config)


if __name__ == "__main__":
    main()
