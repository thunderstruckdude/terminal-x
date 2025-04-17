import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".terminalx"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / ".history"

DEFAULT_CONFIG = {
    "llm_provider": None,
    "api_key": None,
    "max_history_entries": 100,
}


def ensure_config_dir():
    """Ensure the config directory exists."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)


def load_config():
    """Load configuration from file or create a default one."""
    ensure_config_dir()
    
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # If config is corrupted, reset to default
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to file."""
    ensure_config_dir()
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def update_config(key, value):
    """Update a specific config value."""
    config = load_config()
    config[key] = value
    save_config(config)


def reset_config():
    """Reset configuration to defaults."""
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()


def add_to_history(prompt, command):
    """Add a prompt and generated command to history."""
    ensure_config_dir()
    
    config = load_config()
    max_entries = config.get("max_history_entries", 100)
    
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []
    
    # Add new entry
    history.append({"prompt": prompt, "command": command, "timestamp": import_time()})
    
    # Keep only the most recent entries
    history = history[-max_entries:]
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def get_history():
    """Get command history."""
    ensure_config_dir()
    
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def import_time():
    """Helper to import time for timestamps."""
    from datetime import datetime
    return datetime.now().isoformat()