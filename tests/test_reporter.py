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

#TESTS — load_csv()

#Happy path tests
def test_load_csv_success():
    """Happy path — loading a real CSV file works."""
    df = load_csv("sample.csv")
    assert df is not None
    assert len(df) > 0

#Error cases tests
def test_load_csv_file_not_found():
    """Error case — file that doesn't exist raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_csv("nonexistent.csv")


def test_load_csv_wrong_extension():
    """Error case — non CSV file raises ValueError."""
    with pytest.raises(ValueError):
        load_csv("config.yaml")

# TESTS — get_summary()

#Happy path tests

 def test_get_summary_row_count(sample_df):
    """Happy path — correct number of rows."""
    result = get_summary(sample_df)
    assert result["total_rows"] == 4


def test_get_summary_column_count(sample_df):
    """Happy path — correct number of columns."""
    result = get_summary(sample_df)
    assert result["total_columns"] == 5


def test_get_summary_numeric_columns(sample_df):
    """Happy path — numeric columns are correctly identified."""
    result = get_summary(sample_df)
    assert "salary" in result["numeric_columns"]
    assert "age" in result["numeric_columns"]
    assert "score" in result["numeric_columns"]


def test_get_summary_text_columns(sample_df):
    """Happy path — text columns are correctly identified."""
    result = get_summary(sample_df)
    assert "name" in result["text_columns"]
    assert "department" in result["text_columns"]


def test_get_summary_no_missing_values(sample_df):
    """Happy path — no missing values in clean data."""
    result = get_summary(sample_df)
    for col, count in result["missing_values"].items():
        assert count == 0

#Error case tests
def test_get_summary_with_missing_values():
    """Edge case — missing values are counted correctly."""
    data = {
        "name":   ["Alice", "Bob", None],
        "salary": [95000, None, 58000],
    }
    df = pd.DataFrame(data)
    result = get_summary(df)
    assert result["missing_values"]["name"] == 1
    assert result["missing_values"]["salary"] == 1