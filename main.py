import typer
from rich.console import Console
from agent import run_agent

def main(
    file: str = typer.Option(..., help="The path to the python file to refactor"),
    instruction: str = typer.Option(..., help="What you want the agent to improve")
):
    """
    Autonomous Agent that refactors code based on your instructions.
    """
    console = Console()
    console.print(f"[bold green]Starting Refactor Agent on {file}...[/bold green]")
    
    prompt = (
        f"Read the file at '{file}'. "
        f"Refactor the code following this instruction: '{instruction}'. "
        "Ensure the new code is syntactically correct using the validate_syntax tool. "
        f"If valid, overwrite the file at '{file}' with the improved code."
    )
    
    try:
        response = run_agent(prompt)
        console.print("\n[bold blue]Agent Finished:[/bold blue]")
        console.print(response)
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    typer.run(main)