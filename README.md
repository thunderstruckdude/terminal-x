# Terminal X

A natural language terminal command assistant that translates English instructions into shell commands.

## Features

- Translate natural language into shell commands using AI
- Execute generated commands with confirmation
- Support for multiple LLM providers (Claude, Gemini)
- Command history tracking
- Direct command execution with '!' prefix

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/terminal-x.git
cd terminal-x

# Install the package
pip install -e .
```

## Usage

```bash
# Start Terminal X
terminal

# Reset configuration
terminal --reset
```

## Examples

```
TerminalX> create a folder called projects and inside that create 3 files named index.html, style.css, and script.js

Generated command: mkdir -p projects && touch projects/index.html projects/style.css projects/script.js

Do you want to execute this command? [y/N]: y
```

## Requirements

- Python 3.7+
- An API key for Claude or Gemini

## License

MIT