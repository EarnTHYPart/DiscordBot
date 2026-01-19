"""
Utility functions for the Discord bot
"""
import json
import os
from typing import Dict, Any


def load_json_file(filepath: str, default: Any = None) -> Any:
    """
    Safely load a JSON file with error handling
    
    Args:
        filepath: Path to the JSON file
        default: Default value to return if file doesn't exist or has errors
    
    Returns:
        Parsed JSON data or default value
    """
    if default is None:
        default = {}
    
    if not os.path.exists(filepath):
        try:
            with open(filepath, "w") as f:
                json.dump(default, f)
        except Exception as e:
            print(f"Error creating {filepath}: {e}")
        return default
    
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON decode error in {filepath}: {e}")
        return default
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return default


def save_json_file(filepath: str, data: Any) -> bool:
    """
    Safely save data to a JSON file with error handling
    
    Args:
        filepath: Path to save the JSON file
        data: Data to serialize and save
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


def format_uptime(seconds: float) -> str:
    """
    Format uptime in seconds to a human-readable string
    
    Args:
        seconds: Number of seconds
    
    Returns:
        Formatted string like "2d 3h 45m"
    """
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    
    return " ".join(parts) if parts else "< 1m"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length with suffix
    
    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add when truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
