import requests

class LolAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"X-Riot-Token": self.api_key}
        self.regional_routing = "americas.api.riotgames.com"

    def get_puuid_by_riot_id(self, game_name: str, tag_line: str) -> str:
        url = f"https://{self.regional_routing}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("puuid")

    def get_match_ids(self, puuid: str, count: int = 10) -> list[str]:
        url = f"https://{self.regional_routing}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_match_details(self, match_id: str) -> dict:
        url = f"https://{self.regional_routing}/lol/match/v5/matches/{match_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()