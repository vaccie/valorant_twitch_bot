# ValorantBot - Twitch Chat Bot for Valorant Player Stats

## Description
ValorantBot is a Twitch chat bot designed to provide real-time Valorant player stats directly within a Twitch channel. The bot retrieves and displays information about a player's current rank, match history, and performance in competitive matches. It uses the Henrik-3rd-party-API to fetch Valorant data.

## Features
- **Rank Command (`!rank`)**: Displays the player's current rank, rank rating (RR), and the RR change from the last game.
- **Recap Command (`!recap`)**: Provides a summary of the player's win-loss record for the day in competitive matches.

## How It Works
- The bot listens for commands in the Twitch chat and responds with the relevant Valorant statistics.
- It fetches player data from the Henrik API and formats it for display in the Twitch chat.
- Configurations such as the player's name, tag, region, and platform, as well as the bot's OAuth token and API key, are stored securely in the `config.json` file that is already included in the repository.

## Getting Started

### Prerequisites
- Python 3.7+
- TwitchIO library
- A valid Twitch OAuth token
- A Henrik API key

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ValorantBot.git
   cd ValorantBot

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Configure config.json: Edit the config.json file in the root directory of the project to include your specific settings**:
   ```json
   {
    "OAuthToken": "your-oauth-token",
    "APIKey": "your-henrik-api-key",
    "ChannelName": "your-twitch-channel",
    "PlayerName": "your-valorant-name",
    "PlayerTag": "your-valorant-tag",
    "Region": "your-region",
    "Platform": "your-platform"
   }

4. **Run the bot**:
   ```bash
   python valorant_twitch_bot.py
