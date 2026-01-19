# Discord Moderation Bot

A feature-rich Discord bot built with discord.py that provides moderation tools, interactive UI components, and automated content filtering.

## Features

### 🛡️ Moderation & Auto-Moderation
- **Profanity Filter**: Automatically detects and deletes messages containing banned words
- **Strike System**: Tracks user violations with automatic banning after reaching threshold
- **Spam Detection**: Identifies and bans users sending too many messages in a short time window
- **Manual Moderation**: Commands for kick, ban, unban, and role management
- **Mod Logging**: Optional logging channel for all moderation actions

### 🎨 Interactive Components
- **Color Role Selection**: React-based role assignment system with emoji reactions
- **Dropdown Menus**: Interactive select menus for user choices
- **Buttons**: Custom button interfaces with multiple styles
- **Embeds**: Rich embedded messages with formatting

### 💬 Basic Features
- Slash commands for modern Discord interaction
- Message event handlers
- Reaction role system
- Custom greetings

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)
- Discord Server with appropriate permissions

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/EarnTHYPart/DiscordBot.git
   cd DiscordBot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows (PowerShell):
     ```bash
     .\.venv\Scripts\Activate.ps1
     ```
   - Windows (Git Bash):
     ```bash
     source .venv/Scripts/activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   
   Copy the example file and fill in your values:
   ```bash
   cp .env.example .env
   ```
   
   Or create a `.env` file manually:
   ```env
   DISCORD_BOT_TOKEN=your_bot_token_here
   DISCORD_GUILD_ID=your_server_id_here
   MOD_LOG_CHANNEL_ID=your_log_channel_id_here
   BANNED_WORDS=word1,word2,word3
   SPAM_TIME_WINDOW=7
   SPAM_MESSAGE_LIMIT=5
   STRIKES_TO_BAN=3
   COMMAND_PREFIX=!
   ```

## Configuration

The bot uses a centralized configuration system through `config.py` which loads all settings from your `.env` file.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DISCORD_BOT_TOKEN` | Your bot's authentication token | *Required* |
| `DISCORD_GUILD_ID` | Your Discord server ID | *Required* |
| `MOD_LOG_CHANNEL_ID` | Channel ID for moderation logs | *Optional* |
| `BANNED_WORDS` | Comma-separated list of profanity | `` |
| `SPAM_TIME_WINDOW` | Time window for spam detection (seconds) | `7` |
| `SPAM_MESSAGE_LIMIT` | Max messages allowed in time window | `5` |
| `STRIKES_TO_BAN` | Number of strikes before auto-ban | `3` |
| `COMMAND_PREFIX` | Bot command prefix | `!` |

**Note**: An `.env.example` file is provided as a template. Copy it to `.env` and fill in your actual values.

### Bot Permissions

Ensure your bot has these permissions:
- Send Messages
- Manage Messages (for deleting profanity/spam)
- Manage Roles (for color roles and role commands)
- Ban Members (for auto-moderation)
- Kick Members (for manual moderation)
- Add Reactions (for reaction roles)
- Read Message History
- View Channels

### Setting Up Roles

For the color role system to work, create these roles in your server:
- Red
- Green
- Blue
- Yellow
- Pink

## Usage

### Running the Bot

**Basic version** (`main.py` - simplified features):
```bash
python main.py
```

**Advanced version** (`secondary.py` - full moderation):
```bash
python secondary.py
```

### Available Commands

#### Slash Commands (/)

| Command | Description | Permission Required |
|---------|-------------|---------------------|
| `/hello` | Bot greets you | Everyone |
| `/print <text>` | Echo text back | Everyone |
| `/embed` | Display an example embed | Everyone |
| `/menu` | Show a dropdown menu | Everyone |
| `/button` | Display interactive buttons | Everyone |
| `/colorrole` | Create color role selection message | Administrator |

#### Prefix Commands (!)

| Command | Description | Permission Required |
|---------|-------------|---------------------|
| `!ping` | Check bot latency | Everyone |
| `!addrole @user <role>` | Add role to user | Manage Roles |
| `!removerole @user <role>` | Remove role from user | Manage Roles |
| `!kick @user [reason]` | Kick a user | Kick Members |
| `!ban @user [reason]` | Ban a user | Ban Members |
| `!unban username#0000` | Unban a user | Ban Members |
| `!mention <text>` | Send a mention message | Administrator |

### Auto-Moderation Features

**Profanity Filter**:
- Automatically deletes messages containing banned words
- Issues strikes to offending users
- Auto-bans users after reaching strike threshold
- Logs all actions to mod log channel

**Spam Detection**:
- Monitors message frequency per user
- Auto-bans users exceeding message limit in time window
- Configurable thresholds via environment variables

**Reaction Roles**:
- Use `/colorrole` to create a color selection message
- Users react with emoji to get corresponding role
- Removing reaction removes the role

## Project Structure

```
DiscordBot/
├── main.py              # Basic bot implementation
├── secondary.py         # Advanced bot with full moderation
├── config.py            # Centralized configuration module
├── utils.py             # Utility functions (JSON handling, formatting)
├── requirements.txt     # Python dependencies
├── strikes.json         # Persistent strike data (auto-generated)
├── .env                 # Environment configuration (create this)
├── .env.example         # Example environment configuration
├── .gitignore          # Git ignore file
├── LICENSE             # MIT License
├── CONTRIBUTING.md     # Contribution guidelines
└── README.md           # This file
```

## Files Description

- **main.py**: Simplified version with basic commands, reaction roles, and UI components
- **secondary.py**: Full-featured version with auto-moderation, profanity filter, spam detection, and all commands
- **config.py**: Centralized configuration management - loads and validates all settings from `.env`
- **utils.py**: Reusable utility functions for JSON handling, text formatting, and more
- **strikes.json**: JSON file storing user strike counts (automatically created)
- **.env.example**: Template for environment variables - copy to `.env` and configure
- **requirements.txt**: List of required Python packages
- **LICENSE**: MIT License for the project
- **CONTRIBUTING.md**: Guidelines for contributing to the project

## Dependencies

- `discord.py` - Discord API wrapper
- `python-dotenv` - Environment variable management
- `requests` - HTTP library
- `aiohttp` - Async HTTP client/server

See [requirements.txt](requirements.txt) for complete list with versions.

## Troubleshooting

### Bot not responding to commands
- Verify bot token is correct in `.env`
- Check bot has proper permissions in your server
- Ensure GUILD_ID matches your Discord server ID
- Commands may take a minute to sync after first startup

### Color roles not working
- Create roles named exactly: Red, Green, Blue, Yellow, Pink
- Ensure bot's role is higher than color roles in hierarchy
- Bot needs "Manage Roles" permission

### Profanity filter not working
- Check BANNED_WORDS in `.env` is set correctly
- Bot needs "Manage Messages" permission
- Ensure secondary.py is being used (not main.py)

### Module not found errors
- Activate virtual environment
- Run `pip install -r requirements.txt`

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## Security Notes

- **Never commit your `.env` file** - it contains sensitive tokens
- Add `.env` to `.gitignore`
- Rotate your bot token if accidentally exposed
- Use environment variables for all sensitive configuration

## License

This project is provided as-is for educational and personal use.

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Check the [Discord.py documentation](https://discordpy.readthedocs.io/)
- Review this README thoroughly
- Check your bot permissions and configuration

---

**Note**: This bot includes two versions:
- `main.py`: Lightweight version for basic functionality
- `secondary.py`: Production-ready version with comprehensive moderation

Choose the version that best fits your needs!
