import os
import yaml
from dotenv import load_dotenv
from models import AppConfig

# Load the .env file into environment variables
load_dotenv()

# setups the app configuration by reading from .env and config.yaml, then validating with Pydantic
def load_config() -> AppConfig:
    """Read .env and config.yaml, combine them, validate with Pydantic."""

    # --- Read from .env ---
    app_name = os.getenv("APP_NAME", "CSV Reporter")
    default_file = os.getenv("DEFAULT_FILE", "sample.csv")
    max_rows = int(os.getenv("MAX_ROWS", "1000"))

    # --- Read from config.yaml ---
    with open("config.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)

    delimiter = yaml_data["defaults"]["delimiter"]
    encoding = yaml_data["defaults"]["encoding"]
    available_stats = yaml_data["stats"]["available"]


config = AppConfig(
    app_name=app_name,
    default_file=default_file,
    max_rows=max_rows,
    delimiter=delimiter,
    encoding=encoding,
    available_stats=available_stats,
)

return config