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

# --- Command 1: Summary ---
@app.command()
def summary(
    file: str = typer.Option(None, "--file", "-f", help="Path to the CSV file"),
):
    """Print a full summary of the CSV file."""

    # Use default file from config if none provided
    filepath = file or config.default_file

    console.print(f"\n[bold cyan]Loading file:[/bold cyan] {filepath}\n")