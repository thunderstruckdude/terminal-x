# Terminal X

A natural language terminal command assistant that translates English instructions into shell commands.

## Features

- Translate natural language into shell commands using AI
- Execute generated commands with confirmation
- Support for multiple LLM providers (Claude, Gemini, GPT-4o)
- Command history tracking
- Direct command execution with '!' prefix

## Installation

### Easy Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/terminal-x.git
cd terminal-x

# Run the installer script
python install.py
```

This will:
1. Create a virtual environment at ~/.terminalx-venv
2. Install all required dependencies
3. Create a shortcut at ~/bin/terminalx

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/terminal-x.git
cd terminal-x

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the package
pip install -e .
```

## Usage

```bash
# Start Terminal X
terminalx

# Reset configuration
terminalx --reset
```

## Examples

```
TerminalX> create a folder called projects and inside that create 3 files named index.html, style.css, and script.js

Generated command: mkdir -p projects && touch projects/index.html projects/style.css projects/script.js

Do you want to execute this command? [y/N]: y
```

## Requirements

- Python 3.7+
- An API key for Claude, Gemini, or GPT-4o

## License

MIT