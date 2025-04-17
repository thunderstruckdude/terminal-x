#!/usr/bin/env python3
# filepath: /home/blaze/terminal-x-test/install.py

import os
import subprocess
import sys
import platform
from pathlib import Path

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_color(text, color):
    """Print colored text."""
    print(f"{color}{text}{RESET}")

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print_color("Terminal X requires Python 3.7 or higher.", RED)
        print_color(f"You are using Python {platform.python_version()}", RED)
        return False
    return True

def create_virtual_env():
    """Create a virtual environment for Terminal X."""
    venv_path = Path.home() / ".terminalx-venv"
    
    # Check if venv already exists
    if venv_path.exists():
        print_color("Virtual environment already exists.", YELLOW)
        recreate = input("Do you want to recreate it? (y/N): ").lower() == 'y'
        if recreate:
            print_color("Recreating virtual environment...", YELLOW)
            subprocess.run(["rm", "-rf", str(venv_path)], check=True)
        else:
            return venv_path
    
    print_color("Creating virtual environment...", GREEN)
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    return venv_path

def install_terminal_x(venv_path):
    """Install Terminal X in the virtual environment."""
    pip_path = venv_path / "bin" / "pip"
    
    print_color("Installing Terminal X and dependencies...", GREEN)
    subprocess.run([str(pip_path), "install", "-e", "."], check=True)
    return venv_path / "bin" / "terminal"

def create_shortcut(terminal_path):
    """Create a shortcut script in ~/bin."""
    bin_dir = Path.home() / "bin"
    
    # Create bin directory if it doesn't exist
    if not bin_dir.exists():
        bin_dir.mkdir(parents=True)
    
    # Create shortcut script
    shortcut_path = bin_dir / "terminalx"
    with open(shortcut_path, "w") as f:
        f.write(f"""#!/bin/bash
# Terminal X launcher
{terminal_path} "$@"
""")
    
    # Make the script executable
    shortcut_path.chmod(0o755)
    
    # Check if bin directory is in PATH
    if str(bin_dir) not in os.environ.get("PATH", ""):
        print_color(f"\nAdd {bin_dir} to your PATH by adding this to your shell profile:", YELLOW)
        print(f"export PATH=\"$HOME/bin:$PATH\"")

def main():
    print_color("\n=== Terminal X Installer ===\n", BOLD + GREEN)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    try:
        # Create virtual environment
        venv_path = create_virtual_env()
        
        # Install Terminal X
        terminal_path = install_terminal_x(venv_path)
        
        # Create shortcut
        create_shortcut(terminal_path)
        
        print_color("\n✅ Terminal X installed successfully!", BOLD + GREEN)
        print_color("You can now run 'terminalx' from your terminal.", GREEN)
        print_color("For first-time setup, run 'terminalx --reset'", YELLOW)
        
    except Exception as e:
        print_color(f"\n❌ Installation failed: {str(e)}", RED)
        sys.exit(1)

if __name__ == "__main__":
    main()