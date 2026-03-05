from pydantic import BaseModel, field_validator
from typing import List


class AppConfig(BaseModel):
    """Validates and holds all config values for the app."""
    
    app_name: str
    default_file: str
    max_rows: int
    delimiter: str
    encoding: str
    available_stats: List[str]

    @field_validator("max_rows")
    @classmethod
    def max_rows_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("max_rows must be a positive number")
        return value

    @field_validator("delimiter")
    @classmethod
    def delimiter_must_be_single_char(cls, value):
        if len(value) != 1:
            raise ValueError("delimiter must be a single character")
        return value