# Get My ID Bot

A simple Telegram bot that extracts user IDs, chat IDs, and other identifiers from messages and forwarded messages.

## Features

-   Get your user ID and current chat ID with `/start` command
-   Extract IDs from forwarded messages (user IDs, chat IDs, usernames)
-   Handle privacy-protected forwarded messages
-   Get IDs from replied messages
-   Detailed help with `/help` command

## Quick Start

### Using Docker (Recommended)

1. **Setup environment:**

    ```bash
    make setup-env
    ```

2. **Edit `.env` file and add your bot token:**

    ```bash
    BOT_TOKEN=your_bot_token_here
    ```

3. **Build and run:**
    ```bash
    make quick-start
    ```

### Using Poetry (Development)

1. **Install dependencies:**

    ```bash
    make install
    ```

2. **Setup environment:**

    ```bash
    make setup-env
    # Edit .env file with your BOT_TOKEN
    ```

3. **Run locally:**
    ```bash
    make dev
    ```

## Available Commands

### Make Commands

-   `make help` - Show all available commands
-   `make quick-start` - Setup env, build and run (Docker)
-   `make quick-start-detached` - Setup env, build and run (Docker, detached)
-   `make quick-dev` - Install deps and run locally
-   `make build` - Build Docker image
-   `make run` - Run bot in Docker container
-   `make run-detached` - Run bot in background
-   `make stop` - Stop running container
-   `make logs` - Show container logs
-   `make clean` - Clean up containers and images
-   `make format` - Format code with black
-   `make lint` - Lint code with flake8

### Bot Commands

-   `/start` - Get your user ID and current chat ID
-   `/help` - Show detailed help information
-   Forward any message to get sender's ID and original chat ID

## Bot Functionality

The bot extracts the following information:

### From `/start` command:

-   Your user ID
-   Current chat ID

### From forwarded messages:

-   Forwarded from user ID (if from user)
-   Forwarded from chat ID (if from channel/group)
-   Forwarded from username (if available)
-   Forwarded from chat title (if from channel/group)
-   Forwarded from sender name (if privacy settings enabled)

### From replied messages:

-   Replying to user ID
-   Replying to username (if available)

### From regular messages:

-   Message sender ID
-   Message sender username (if available)

## Getting a Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token and add it to your `.env` file

## Project Structure

```
get-my-id-bot/
├── src/
│   ├── bot/
│   │   └── __init__.py      # Main bot logic
│   └── main.py              # Entry point
├── Dockerfile               # Docker configuration
├── Makefile                 # Build and run commands
├── pyproject.toml           # Poetry dependencies
├── env.example              # Environment variables template
└── README.md                # This file
```

## Dependencies

-   `python-telegram-bot` - Telegram Bot API wrapper
-   `python-dotenv` - Environment variables management
-   `poetry` - Dependency management

## Development

### Code Style

The project uses:

-   **Black** for code formatting
-   **Flake8** for linting
-   **Poetry** for dependency management

### Running Tests

```bash
make test
```

### Formatting Code

```bash
make format
```

### Linting

```bash
make lint
```

## Docker

The bot runs in a Docker container with:

-   Python 3.11 slim base image
-   Non-root user for security
-   Poetry for dependency management
-   Environment variables from `.env` file

## License

This project is open source and available under the MIT License.
