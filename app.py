import typer
from rich.console import Console
from rich.table import Table
from config import load_config
from reporter import load_csv, get_summary, get_column_stats

app = typer.Typer(help="CSV Reporter — analyze your CSV files from the terminal.")
console = Console()
config = load_config()


@app.command()
def summary(
    file: str = typer.Option(None, "--file", "-f", help="Path to the CSV file"),
):
    """Print a full summary of the CSV file."""

    filepath = file or config.default_file

    console.print(f"\n[bold cyan]Loading file:[/bold cyan] {filepath}\n")

    try:
        df = load_csv(filepath, config.delimiter, config.encoding)
        result = get_summary(df)

        console.print(f"[bold]Total Rows:[/bold]    {result['total_rows']}")
        console.print(f"[bold]Total Columns:[/bold] {result['total_columns']}")

        table = Table(title="Columns Overview", show_header=True)
        table.add_column("Column Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Missing Values", style="red")

        for col in result["columns"]:
            col_type = "numeric" if col in result["numeric_columns"] else "text"
            missing = str(result["missing_values"][col])
            table.add_row(col, col_type, missing)

        console.print(table)

    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def stats(
    file: str = typer.Option(None, "--file", "-f", help="Path to the CSV file"),
    column: str = typer.Option(..., "--column", "-c", help="Column to analyze"),
    stat: str = typer.Option("mean", "--stat", "-s", help="Stat to compute: mean, sum, min, max, count, median"),
):
    """Compute a specific stat on a column."""

    filepath = file or config.default_file

    console.print(f"\n[bold cyan]File:[/bold cyan]   {filepath}")
    console.print(f"[bold cyan]Column:[/bold cyan] {column}")
    console.print(f"[bold cyan]Stat:[/bold cyan]   {stat}\n")

    try:
        df = load_csv(filepath, config.delimiter, config.encoding)
        result = get_column_stats(df, column, stat)

        console.print(f"[bold green]{stat.upper()} of '{column}':[/bold green] {result}")

    except (FileNotFoundError, ValueError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()