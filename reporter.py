import pandas as pd
from pathlib import Path


def load_csv(filepath: str, delimiter: str = ",", encoding: str = "utf-8") -> pd.DataFrame:
    """Load a CSV file and return it as a DataFrame."""

    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if path.suffix != ".csv":
        raise ValueError(f"Expected a .csv file, got: {path.suffix}")

    df = pd.read_csv(filepath, delimiter=delimiter, encoding=encoding)

    if df.empty:
        raise ValueError("The CSV file is empty.")

    return df
