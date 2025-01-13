import os
from random import choice, randint
from typing import Final
from dotenv import load_dotenv
import requests

load_dotenv()
KEY: Final[str] = os.getenv('API_KEY')
print(KEY)

def giveRank(username,hashtag: str) -> str:
    LOLUserName = username
    LOLhashtag = hashtag
    resp1 = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{LOLUserName}/{LOLhashtag}" + '?api_key=' + KEY)
    if resp1.status_code == 200:
        player_info = resp1.json()
        player_puuid = player_info['puuid']
        resp2 = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{player_puuid}" + '?api_key=' + KEY)
        player_info2 = resp2.json()
        player_summunerid = player_info2['id']
        resp3 = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{player_summunerid}" + '?api_key=' + KEY)
        player_info3 = resp3.json()
        if player_info3 == []:
            return f"""
RiotID: {LOLUserName}#{LOLhashtag}
Solo/Duo Ranked: Not Played Yet...
Flex Ranked: Not Played Yet...
"""
        else:
            if len(player_info3) == 2:
                player_solo_duo_info = player_info3[0]
                player_flex_info = player_info3[1]
            else:
                player_unknown_info = player_info3[0]
                if player_unknown_info['queueType'] == "RANKED_FLEX_SR":
                    player_flex_info = player_unknown_info
                    return f"""
RiotID: {LOLUserName}#{LOLhashtag}
Solo/Duo Ranked: Not Played Yet...
Flex Ranked: {player_flex_info['tier']} {player_flex_info['rank']} {player_flex_info['leaguePoints']} LP Wins: {player_flex_info['wins']}, Losses: {player_flex_info['losses']}
"""
                else:
                    player_solo_duo_info = player_unknown_info
                    return f"""
RiotID: {LOLUserName}#{LOLhashtag}
Solo/Duo Ranked: {player_solo_duo_info['tier']} {player_solo_duo_info['rank']} {player_solo_duo_info['leaguePoints']} LP Wins: {player_solo_duo_info['wins']}, Losses: {player_solo_duo_info['losses']}
Flex Ranked: Not Played Yet...
"""
            return f"""
RiotID: {LOLUserName}#{LOLhashtag}
Solo/Duo Ranked: {player_solo_duo_info['tier']} {player_solo_duo_info['rank']} {player_solo_duo_info['leaguePoints']} LP Wins: {player_solo_duo_info['wins']}, Losses: {player_solo_duo_info['losses']}
Flex Ranked: {player_flex_info['tier']} {player_flex_info['rank']} {player_flex_info['leaguePoints']} LP Wins: {player_flex_info['wins']}, Losses: {player_flex_info['losses']}
"""
    else:
        return f"Riot Username and/or Hashtag was not found. Status Code Error {resp1.status_code}"

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'league ranked' in lowered:
        rest = user_input[13:]
        usernameandhashtag = rest.split("#")
        username = usernameandhashtag[0]
        hashtag = usernameandhashtag[1]
        return giveRank(username,hashtag)
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
$
"""
    else:
        return choice(['I do not understand...', 
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])