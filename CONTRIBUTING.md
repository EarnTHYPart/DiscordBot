# Contributing to Discord Bot

Thank you for considering contributing to this Discord bot project! 

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/EarnTHYPart/DiscordBot/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (Python version, OS, etc.)

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue describing:
   - The feature and its benefits
   - Potential implementation approach
   - Any drawbacks or considerations

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Follow existing code style
   - Add docstrings to new functions
   - Update documentation as needed
   - Test your changes thoroughly

4. **Commit your changes**:
   ```bash
   git commit -m "Add: brief description of changes"
   ```
   
   Use conventional commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Provide clear title and description
   - Reference any related issues
   - Explain what changes were made and why

### Code Style Guidelines

- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Handle errors gracefully with try-except blocks
- Follow PEP 8 style guide for Python code

### Testing

Before submitting a PR:
- Test the bot in a development Discord server
- Verify all slash commands work
- Test moderation features
- Ensure no sensitive data is committed

### What NOT to Commit

- Your `.env` file (contains tokens)
- Your personal `strikes.json` data
- Cache files or `__pycache__`
- IDE-specific configuration files

### Questions?

Feel free to open an issue for questions or clarifications!

---

Thank you for contributing! 🎉
