import subprocess
import os
import platform

def execute_command(command):
    """Execute a shell command and return its output and error (if any)."""
    try:
        # Create a subshell environment
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr
    except Exception as e:
        return 1, "", str(e)


def is_first_run():
    """Check if this is the first run of the application."""
    from .config import CONFIG_FILE
    return not CONFIG_FILE.exists()


def get_terminal_size():
    """Get the current terminal size."""
    try:
        columns, rows = os.get_terminal_size()
        return columns, rows
    except:
        return 80, 24  # Default fallback


def get_system_info():
    """Get basic system information."""
    system = platform.system()
    release = platform.release()
    return system, release