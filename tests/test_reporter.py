import pytest
import pandas as pd
from reporter import load_csv, get_summary, get_column_stats

# FIXTURES — reusable test data

@pytest.fixture
def sample_df():
    """Creates a small DataFrame we can reuse across all tests."""
    data = {
        "name":       ["Alice", "Bob", "Carol", "David"],
        "age":        [30, 25, 35, 28],
        "department": ["Engineering", "Marketing", "Engineering", "HR"],
        "salary":     [95000, 62000, 110000, 58000],
        "score":      [88, 74, 95, 69],
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_df():
    """Creates an empty DataFrame for edge case testing. """
    return pd.DataFrame()

# TESTS — load_csv()
ef test_load_csv_success():
    """Happy path — loading a real CSV file works."""
    df = load_csv("sample.csv")
    assert df is not None
    assert len(df) > 0


def test_load_csv_file_not_found():
    """Error case — file that doesn't exist raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_csv("nonexistent.csv")


def test_load_csv_wrong_extension():
    """Error case — non CSV file raises ValueError."""
    with pytest.raises(ValueError):
        load_csv("config.yaml")