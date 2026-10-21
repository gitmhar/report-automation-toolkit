from pathlib import Path

import pandas as pd


def load_excel_data(config):
    """
    Load raw Excel data using paths and column mappings from the configuration.
    """
    
    project_root = Path(__file__).resolve().parent.parent.parent.parent
        
    file_path = project_root / config["source"]["path"]
    
    if not file_path.exists():
        raise FileNotFoundError(f"Source Excel file not found at: {file_path.absolute()}.")
    
    print(f"Reading Excel file from: {file_path}...")
    
    df = pd.read_excel(file_path)
    
    column_mapping = config["columns"]
    inverted_mapping  = {v: k for k, v in column_mapping.items()}
    
    missing_columns = [col for col in inverted_mapping if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns in Excel: {missing_columns}")
    
    df = df.rename(columns=inverted_mapping)
    
    print(f"Successfully loaded and normalize {len(df)} rows from Excel.")
    return df

if __name__ == "__main__":
    import sys
            
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from config import load_config
        
    cfg = load_config()
    df_data = load_excel_data(cfg)
    print("\nPreview of normalized data:")
    print(df_data.head(10))