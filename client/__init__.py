import os
from random import choice
import time
import requests

class RiotClient:
    def __init__(self, riot_key: str):
        self.riot_key = riot_key

    def _send_request(self, url: str, max_retries: int = 5) -> dict:
        for attempt in range(max_retries):
            resp = requests.get(url, headers = { "X-Riot-Token": self.riot_key })
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                retry_after = int(resp.headers.get('Retry-After', 1))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(f"Failed to fetch data. Status Code: {resp.status_code}, URL: {url}")
                return None # TODO errors
        print("Max retries reached. Giving up.")
        return None # TODO errors

    def get_puuid_from_username_and_tagline(self, username: str, tag: str) -> str:
        username, tag = username.strip(), tag.strip()

        account_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tag}"

        account_data = self._send_request(account_url)
        if not account_data:
            return "Failed to fetch account data. Please check the username and tag." # TODO errors

        puuid = account_data.get('puuid')
        if not puuid:
            return "Failed to retrieve PUUID. Ensure the username and tag are correct."

        return puuid

    def get_summoner_data(self, puuid: str) -> dict:
        summoner_url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        summoner_data = self._send_request(summoner_url)
        if not summoner_data:
            return "Failed to fetch summoner data."

        return summoner_data

    def get_rank_data(self, summoner_id: str) -> dict:
        rank_url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
        rank_data = self._send_request(rank_url)
        if not rank_data:
            return "Failed to fetch rank data."

        return rank_data
