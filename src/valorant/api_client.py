import requests

class ValorantAPIClient:
    def __init__(self):
        self.base_url = "https://api.henrikdev.xyz/valorant"

    def get_match_history(self, region: str, name: str, tag: str, size: int = 10) -> list[dict]:
        url = f"{self.base_url}/v3/matches/{region}/{name}/{tag}?size={size}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])