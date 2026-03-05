import typer
from rich.console import Console
from rich.table import Table
from config import load_config
from reporter import (
    load_csv,
    get_summary,
    get_column_stats
)

# --- Setup ---
app = typer.Typer(help="CSV Reporter — analyze your CSV files from the terminal.")
console = Console()
config = load_config()

