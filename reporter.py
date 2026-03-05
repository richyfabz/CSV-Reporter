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

def get_column_stats(df: pd.DataFrame, column: str, stat: str) -> float:
    """Run a single stat (mean, sum, etc.) on a specific column."""

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' is not numeric. Can't run stats on text.")

    operations = {
        "mean":   df[column].mean(),
        "sum":    df[column].sum(),
        "min":    df[column].min(),
        "max":    df[column].max(),
        "count":  df[column].count(),
        "median": df[column].median(),
    }

    if stat not in operations:
        raise ValueError(f"Unknown stat '{stat}'. Choose from: {list(operations.keys())}")

    return round(operations[stat], 2)

def get_summary(df: pd.DataFrame) -> dict:
    """Return a full summary of the CSV file."""

    summary = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "numeric_columns": list(df.select_dtypes(include="number").columns),
        "text_columns": list(df.select_dtypes(include="str").columns),
        "missing_values": df.isnull().sum().to_dict(),
    }

    return summary
