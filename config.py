"""
Configuration module for Discord Bot
Centralizes all environment variable loading and configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BotConfig:
    """Central configuration class for the Discord bot"""
    
    # Discord Bot Settings
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))
    
    # Moderation Settings
    MOD_LOG_CHANNEL_ID = os.getenv("MOD_LOG_CHANNEL_ID")
    BANNED_WORDS = {w.lower() for w in os.getenv("BANNED_WORDS", "").split(",") if w.strip()}
    
    # Spam Detection Settings
    SPAM_TIME_WINDOW = int(os.getenv("SPAM_TIME_WINDOW", "7"))  # seconds
    SPAM_MESSAGE_LIMIT = int(os.getenv("SPAM_MESSAGE_LIMIT", "5"))  # messages
    
    # Strike System Settings
    STRIKES_TO_BAN = int(os.getenv("STRIKES_TO_BAN", "3"))
    STRIKE_FILE = "strikes.json"
    
    # Command Prefix
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.BOT_TOKEN:
            raise ValueError(
                "Bot token not found. Please set DISCORD_BOT_TOKEN in your .env file."
            )
        if not cls.GUILD_ID or cls.GUILD_ID == 0:
            raise ValueError(
                "Guild ID not found or invalid. Please set DISCORD_GUILD_ID in your .env file."
            )
        return True
    
    @classmethod
    def get_summary(cls):
        """Get a summary of current configuration (without sensitive data)"""
        return {
            "Guild ID": cls.GUILD_ID,
            "Spam Time Window": f"{cls.SPAM_TIME_WINDOW}s",
            "Spam Message Limit": cls.SPAM_MESSAGE_LIMIT,
            "Strikes to Ban": cls.STRIKES_TO_BAN,
            "Command Prefix": cls.COMMAND_PREFIX,
            "Banned Words Count": len(cls.BANNED_WORDS),
            "Mod Log Channel": "Configured" if cls.MOD_LOG_CHANNEL_ID else "Not Set"
        }
