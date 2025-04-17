import os
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm

from .config import (
    load_config, save_config, reset_config, 
    add_to_history, get_history
)
from .llm import LLMProvider, get_provider_choices
from .utils import execute_command, is_first_run, get_terminal_size

console = Console()

def show_welcome_screen():
    """Display a stylish welcome screen with ASCII art."""
    console.print("\n")
    
    # ASCII art for Terminal X
    terminal_x_ascii = r"""
    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗         ██╗  ██╗
    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║         ╚██╗██╔╝
       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║          ╚███╔╝ 
       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║          ██╔██╗ 
       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗    ██╔╝ ██╗
       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝
    """
    
    console.print(terminal_x_ascii, style="cyan bold")
    
    welcome_text = Text("Natural Language Terminal Command Assistant", style="italic green")
    version_text = Text("v0.1.0", style="dim")
    
    console.print(Panel.fit(
        welcome_text + "\n\n" + version_text,
        border_style="bright_blue",
        padding=(1, 4)
    ))
    console.print("\n")
    

def setup_config():
    """First-time setup to configure the application."""
    show_welcome_screen()
    
    console.print("Let's get you set up with Terminal X.", style="bold")
    console.print("You'll need an API key for your preferred LLM provider.\n")
    
    providers = get_provider_choices()
    provider_options = ", ".join(providers)
    
    provider = Prompt.ask(
        f"Which LLM provider would you like to use? [{provider_options}]",
        choices=providers,
        default=providers[0]
    )
    
    api_key = Prompt.ask(f"Please enter your {provider.capitalize()} API key", password=True)
    
    config = load_config()
    config["llm_provider"] = provider
    config["api_key"] = api_key
    save_config(config)
    
    console.print("\n✅ Setup complete! You can now start using Terminal X.", style="green bold")
    console.print("Type your requests in natural language, and I'll convert them to shell commands.")
    console.print("Use '!command' to execute a command directly.")
    console.print("Type 'exit' to quit.\n")


def handle_direct_command(command):
    """Handle a direct command (prefixed with !)."""
    # Remove the ! prefix
    command = command[1:].strip()
    
    if not command:
        console.print("Please provide a command after '!'", style="yellow")
        return
    
    console.print(f"Executing: [bold]{command}[/bold]")
    exit_code, stdout, stderr = execute_command(command)
    
    if stdout:
        console.print(stdout)
    if stderr:
        console.print(f"[red]{stderr}[/red]")
    
    if exit_code != 0:
        console.print(f"[red]Command failed with exit code {exit_code}[/red]")
    else:
        console.print("[green]Command executed successfully[/green]")


def process_natural_language(prompt, llm_provider):
    """Process natural language input and generate a shell command."""
    console.print(f"Generating command for: [italic]{prompt}[/italic]")
    
    with console.status("Thinking..."):
        command, error = llm_provider.generate_command(prompt)
    
    if error:
        console.print(f"[red]Error: {error}[/red]")
        return None
    
    console.print(f"Generated command: [bold green]{command}[/bold green]")
    
    # Add to history
    add_to_history(prompt, command)
    
    execute = Confirm.ask("Do you want to execute this command?", default=False)
    if execute:
        console.print(f"Executing: [bold]{command}[/bold]")
        exit_code, stdout, stderr = execute_command(command)
        
        if stdout:
            console.print(stdout)
        if stderr:
            console.print(f"[red]{stderr}[/red]")
        
        if exit_code != 0:
            console.print(f"[red]Command failed with exit code {exit_code}[/red]")
        else:
            console.print("[green]Command executed successfully[/green]")
    else:
        console.print("Command execution cancelled.")


@click.command()
@click.option("--reset", is_flag=True, help="Reset configuration")
def main(reset):
    """Terminal X: Natural Language Terminal Command Assistant."""
    if reset:
        if Confirm.ask("Are you sure you want to reset all Terminal X settings?", default=False):
            reset_config()
            console.print("[green]Configuration reset successfully.[/green]")
        return
    
    # Check for first run
    if is_first_run():
        setup_config()
    
    config = load_config()
    provider = config.get("llm_provider")
    api_key = config.get("api_key")
    
    if not provider or not api_key:
        console.print("[yellow]Configuration incomplete. Running setup...[/yellow]")
        setup_config()
        config = load_config()
        provider = config.get("llm_provider")
        api_key = config.get("api_key")
    
    # Create LLM provider
    llm_provider = LLMProvider(provider, api_key)
    
    console.print(f"\n[bold cyan]Terminal X[/bold cyan] is ready! (using {provider.capitalize()})")
    console.print("Type '!command' to execute a command directly.")
    console.print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold green]TerminalX>[/bold green]").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                console.print("[cyan]Goodbye! 👋[/cyan]")
                break
            
            if user_input.startswith("!"):
                handle_direct_command(user_input)
            else:
                process_natural_language(user_input, llm_provider)
                
        except KeyboardInterrupt:
            console.print("\n[cyan]Goodbye! 👋[/cyan]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    main()