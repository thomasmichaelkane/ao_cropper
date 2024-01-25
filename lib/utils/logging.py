from rich.console import Console

def warning(message):
    """
    Displays a warning message in the console.
    """

    console = Console()
    
    style = "bold blue on red"
    warning_text = f"Warning: {message}"
    
    console.print(warning_text, style=style)

