import json
from pathlib import Path


def load_config(config_path=None):
    """
    Loads the JSON configuration file from the given path.
    """

    if config_path is None:
        project_root = Path(__file__).resolve().parent.parent.parent
        path = project_root / "config" / "default.json"
    else:
        path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path.absolute()}")

    with open(path, "r", encoding="utf-8") as file:
        config_data = json.load(file)

    print(f"Successfully loaded configuration from {path}.")
    return config_data


if __name__ == "__main__":
    cfg = load_config()
    print("Sample config setting - Input path:", cfg["source"]["path"])
