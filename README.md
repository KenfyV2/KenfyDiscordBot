# KenfyDiscordBot

KenfyDiscordBot is a Discord bot designed to integrate with Riot Games' API and provide various functionalities for your Discord server. This bot requires some environment variables to be set up in a `.env` file to work correctly.

## Prerequisites

Make sure you have the following installed before setting up the bot:

- Python 3 (recommended version 3.x or later)
- A Discord Developer account with a bot token
- A Riot Games API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd KenfyDiscordBot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory of the project and add the following content:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   API_KEY=your_riot_api_key_here
   ```

   Replace `your_discord_bot_token_here` with your Discord bot token and `your_riot_api_key_here` with your Riot Games API key.

4. Run the bot:
   ```bash
   python3 .\main.py
   ```

## Environment Variables

The bot requires the following environment variables:

- `DISCORD_TOKEN`: The token for your Discord bot. Obtain this from the Discord Developer Portal.
- `API_KEY`: Your Riot Games API key. Obtain this from the [Riot Developer Portal](https://developer.riotgames.com/).

## Features

- Integration with Riot Games API for retrieving game data.
- Custom commands to interact with the bot on your Discord server.

## Commands

Below is an example of the bot commands you can use:

| Command            | Description                          |
|--------------------|--------------------------------------|
| `!help`            | Lists all available commands.        |
| `!league ranked [username]#[hashtag]` | Fetches ranked data for a given League of Legends summoner.   |
| `!commands` | Fetches stats for a given summoner. |
| `!help` | Provides help information about the bot and commands.   |

## Troubleshooting

- **Bot not responding:** Make sure the bot is running and has the necessary permissions to send messages in your server.
- **Invalid API key:** Ensure your Riot Games API key is valid and active.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Discord.js](https://discord.js.org/) for providing a great library for building Discord bots.
- [Riot Games API](https://developer.riotgames.com/) for game data access.

