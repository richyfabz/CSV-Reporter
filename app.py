import typer
from rich.console import Console
from rich.table import Table
from config import load_config
from reporter import load_csv, get_summary, get_column_stats