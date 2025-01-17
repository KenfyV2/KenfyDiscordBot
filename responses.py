import os
from random import choice
import time
from typing import Final
from dotenv import load_dotenv
import requests

load_dotenv()
KEY: Final[str] = os.getenv('API_KEY')

def formatdata(rankData: dict) -> str:
    return f"{rankData['tier']} {rankData['rank']} {rankData['leaguePoints']} LP Wins: {rankData['wins']}, Losses: {rankData['losses']}"

def fetchdata(url: str, max_retries: int = 5) -> dict:
    for attempt in range(max_retries):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 429:
            retry_after = int(resp.headers.get('Retry-After', 1))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(f"Failed to fetch data. Status Code: {resp.status_code}, URL: {url}")
            return None
    print("Max retries reached. Giving up.")
    return None

def giveRank(username: str, tag: str) -> str:
    username, tag = username.strip(), tag.strip()
    if not username or not tag:
        return "Invalid username or tag provided."

    account_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tag}?api_key={KEY}"
    account_data = fetchdata(account_url)
    if not account_data:
        return "Failed to fetch account data. Please check the username and tag."

    puuid = account_data.get('puuid')
    if not puuid:
        return "Failed to retrieve PUUID. Ensure the username and tag are correct."

    summoner_url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={KEY}"
    summoner_data = fetchdata(summoner_url)
    if not summoner_data:
        return "Failed to fetch summoner data."

    summoner_id = summoner_data.get('id')
    if not summoner_id:
        return "Failed to retrieve summoner ID."

    rank_url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={KEY}"
    rank_data = fetchdata(rank_url)
    if not rank_data:
        return "Failed to fetch rank data."

    player_rank_flex = "Not Played Yet..."
    player_rank_solo_duo = "Not Played Yet..."
    for entity in rank_data:
        if entity['queueType'] == "RANKED_FLEX_SR":
            player_rank_flex = formatdata(entity)
        elif entity['queueType'] == "RANKED_SOLO_5x5":
            player_rank_solo_duo = formatdata(entity)

    return f"""
RiotID: {username}#{tag}
Solo/Duo Ranked: {player_rank_solo_duo}
Flex Ranked: {player_rank_flex}
"""



def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'league ranked' in lowered:
        Userinfo = user_input[13:].strip()
        if '#' not in user_input:
            return "Invalid format. Please provide Username#Tag"
        username, tag = Userinfo.split('#')
        return giveRank(username.strip(),tag.strip())
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'help' in lowered:
        return 'try $commands'
    elif 'commands' in lowered:
        return """ 
        Commands List:
$hello
$league ranked username#hashtag
$commands
$help
"""
    else:
        return choice(['I do not understand...', 
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])