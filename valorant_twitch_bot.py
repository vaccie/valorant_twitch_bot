import requests
from datetime import datetime
import pytz
from twitchio.ext import commands
import json

# load json file
with open('config.json') as config_file:
    config = json.load(config_file)

name = config['PlayerName']
tag = config['PlayerTag']
region = config['Region']
platform = config['Platform']
oauth_token = config['OAuthToken']
api_key = config['APIKey']
channel_name = config['ChannelName']

class ValorantBot(commands.Bot):
    def __init__(self):
        super().__init__(token=oauth_token, prefix='!', initial_channels=[channel_name])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def rank(self, ctx: commands.Context):
        valorant_mmr = self.get_valorant_mmr(region, name, tag)
        if "error" not in valorant_mmr:
            if 'data' in valorant_mmr and len(valorant_mmr['data']) > 0:
                last_result = valorant_mmr['data'][0]
                current_tier_patched = last_result.get('currenttierpatched', 'N/A')
                ranking_in_tier = last_result.get('ranking_in_tier', 'N/A')
                mmr_change_to_last_game = last_result.get('mmr_change_to_last_game', 'N/A')
                response_message = f"{current_tier_patched}, RR: {ranking_in_tier} ({mmr_change_to_last_game})"
            else:
                response_message = "Error."
        else:
            response_message = f"Error: {valorant_mmr['error']}"

        await ctx.send(response_message)

    @commands.command()
    async def recap(self, ctx: commands.Context):
        match_history = self.get_valorant_match_history(region, platform, name, tag)
        if "error" not in match_history:
            win_loss_string = self.update_win_loss_string(match_history['data'], name)
            response_message = win_loss_string
            await ctx.send(response_message)
        else:
            await ctx.send(f"Error: {match_history['error']}")

    def get_valorant_match_history(self, region, platform, name, tag):
        url = f"https://api.henrikdev.xyz/valorant/v4/matches/{region}/{platform}/{name}/{tag}"
        params = {
        "mode": "competitive",
        "size": 10 
        }
        headers = {
            "Authorization": api_key
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error. Status code: {response.status_code}"}

    def get_valorant_mmr(self, region, name, tag):
        url = f"https://api.henrikdev.xyz/valorant/v1/mmr-history/{region}/{name}/{tag}"
        headers = {
            "Authorization": api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error. Status code: {response.status_code}"}

    def filter_today_matches_for_player(self, matches, player_name):
        current_date = datetime.now(pytz.utc).strftime("%Y-%m-%d")
        today_matches = []
        for match in matches:
            if match['metadata']['started_at'].startswith(current_date):
                player_data = next((player for player in match['players'] if player['name'].lower() == player_name.lower()), None)
                if player_data:
                    winning_team = None
                    for team in match['teams']:
                        if team['won']:
                            winning_team = team
                            break
                    match_data = {
                        "metadata": match['metadata'],
                        "player": player_data,
                        "winning_team": winning_team
                    }
                    today_matches.append(match_data)
        return today_matches

    def update_win_loss_string(self, matches, player_name):
        wins = 0
        losses = 0
        today_player_matches = self.filter_today_matches_for_player(matches, player_name)
        for match in today_player_matches:
            player_team_id = match.get("player", {}).get("team_id")
            winning_team_id = match.get("winning_team", {}).get("team_id")
            if player_team_id and winning_team_id:
                if player_team_id == winning_team_id:
                    wins += 1
                else:
                    losses += 1
        win_loss_string = f"{wins}W - {losses}L"
        return win_loss_string

if __name__ == "__main__":
    bot = ValorantBot()
    bot.run()
