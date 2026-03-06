import typer
from rich.console import Console
from rich.table import Table
from config import load_config
from reporter import load_csv, get_summary, get_column_stats

app = typer.Typer(
    help="""
CSV Reporter — analyze your CSV files from the terminal.

Examples:

  python app.py summary --file sample.csv

  python app.py stats --file sample.csv --column salary --stat mean

  python app.py stats --column age --stat max
""",
    no_args_is_help=True, # Show help text automatically when no command is given
)

console = Console()       # Rich console used for all terminal output
config = load_config()    # Load app config once at startup (shared across commands)

# Command: summary
@app.command()
def summary(
    file: str = typer.Option(
        None,
        "--file", "-f",
        help="Path to the CSV file. Example: --file data.csv",
    ),
):
    """
    Print a full summary of a CSV file.

    Shows row count, column count, data types, and missing values.

    Examples:

      python app.py summary --file sample.csv

      python app.py summary
    """
    # Use the provided file path or fall back to the default from config

    filepath = file or config.default_file

    console.print(f"\n[bold cyan]Loading file:[/bold cyan] {filepath}\n")

    try:
          # Load the CSV into a DataFrame and compute the summary

        df = load_csv(filepath, config.delimiter, config.encoding)
        result = get_summary(df)

        # Print top-level counts
        console.print(f"[bold]Total Rows:[/bold]    {result['total_rows']}")
        console.print(f"[bold]Total Columns:[/bold] {result['total_columns']}")

        # Build a Rich table showing each column's name, type, and missing value count
        table = Table(title="Columns Overview", show_header=True)
        table.add_column("Column Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Missing Values", style="red")

        for col in result["columns"]:
            col_type = "numeric" if col in result["numeric_columns"] else "text"
            missing = str(result["missing_values"][col])
            table.add_row(col, col_type, missing)

        console.print(table)
        console.print(f"\n[dim]Tip: Run 'python app.py stats --column <name> --stat <stat>' to analyse a column.[/dim]\n")

    except FileNotFoundError:
        # File path was invalid or the file doesn't exist
        console.print(f"\n[bold red]Error:[/bold red] File '[yellow]{filepath}[/yellow]' was not found.")
        console.print("[dim]Tip: Make sure the file exists in your current folder or provide the full path.[/dim]")
        console.print("[dim]Example: python app.py summary --file data.csv[/dim]\n")
        raise typer.Exit(code=1)

    except ValueError as e:
         # Catch data-related errors raised by reporter.py (e.g. empty file, bad format)
        console.print(f"\n[bold red]Error:[/bold red] {e}\n")
        raise typer.Exit(code=1)

# Command: stats
@app.command()
def stats(
    file: str = typer.Option(
        None,
        "--file", "-f",
        help="Path to the CSV file. Example: --file data.csv",
    ),
    column: str = typer.Option(
        None,
        "--column", "-c",
        help="Column name to analyse. Example: --column salary",
    ),
    stat: str = typer.Option(
        "mean",
        "--stat", "-s",
        help="Stat to compute: mean, sum, min, max, count, median. Example: --stat mean",
    ),
):
    """
    Compute a specific stat on a column.

    Available stats: mean, sum, min, max, count, median

    Examples:

      python app.py stats --column salary --stat mean

      python app.py stats --file data.csv --column age --stat max

      python app.py stats -c score -s median
    """

    # Use the provided file path or fall back to the default from config
    filepath = file or config.default_file

    # --- Guard: column is required, show helpful message if missing ---
    if column is None:
        console.print("\n[bold red]Error:[/bold red] Missing required option [yellow]--column[/yellow] / [yellow]-c[/yellow]")
        console.print("[dim]You need to tell the tool which column to analyse.[/dim]")

        # Attempt to load the CSV and hint the user with available column names
        try:
            df = load_csv(filepath, config.delimiter, config.encoding)
            result = get_summary(df)
            console.print(f"\n[bold]Available columns in '{filepath}':[/bold]")
            for col in result["columns"]:
                col_type = "numeric" if col in result["numeric_columns"] else "text"
                console.print(f"  [cyan]{col}[/cyan] [dim]({col_type})[/dim]")
            console.print(f"\n[dim]Example: python app.py stats --column {result['numeric_columns'][0]} --stat mean[/dim]\n")
        except Exception:
              # If CSV can't be loaded, fall back to a generic example
            console.print(f"\n[dim]Example: python app.py stats --column salary --stat mean[/dim]\n")

        raise typer.Exit(code=1)

    # --- Guard: validate stat before running ---
    valid_stats = config.available_stats
    if stat not in valid_stats:
        console.print(f"\n[bold red]Error:[/bold red] '[yellow]{stat}[/yellow]' is not a valid stat.")
        console.print(f"[dim]Available stats: {', '.join(valid_stats)}[/dim]")
        console.print(f"[dim]Example: python app.py stats --column {column} --stat mean[/dim]\n")
        raise typer.Exit(code=1)

    # Echo back the active parameters so the user knows what's being computed
    console.print(f"\n[bold cyan]File:[/bold cyan]   {filepath}")
    console.print(f"[bold cyan]Column:[/bold cyan] {column}")
    console.print(f"[bold cyan]Stat:[/bold cyan]   {stat}\n")

    try:
         # Load CSV and compute the requested stat on the specified column
        df = load_csv(filepath, config.delimiter, config.encoding)
        result = get_column_stats(df, column, stat)
        console.print(f"[bold green]{stat.upper()} of '{column}':[/bold green] {result}\n")

    except FileNotFoundError:
        console.print(f"\n[bold red]Error:[/bold red] File '[yellow]{filepath}[/yellow]' was not found.")
        console.print("[dim]Tip: Make sure the file path is correct.[/dim]")
        console.print("[dim]Example: python app.py stats --file data.csv --column salary --stat mean[/dim]\n")
        raise typer.Exit(code=1)

    except ValueError as e:
        error_msg = str(e)
        console.print(f"\n[bold red]Error:[/bold red] {error_msg}")

        # If the column wasn't found, load the CSV again and show what columns are available
        if "not found" in error_msg:
            try:
                df = load_csv(filepath, config.delimiter, config.encoding)
                result = get_summary(df)
                console.print(f"\n[bold]Available columns:[/bold]")
                for col in result["columns"]:
                    col_type = "numeric" if col in result["numeric_columns"] else "text"
                    console.print(f"  [cyan]{col}[/cyan] [dim]({col_type})[/dim]")
                console.print(f"\n[dim]Example: python app.py stats --column {result['numeric_columns'][0]} --stat mean[/dim]\n")
            except Exception: 
                pass  # Silently skip if the CSV can't be re-loaded at this point


        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()