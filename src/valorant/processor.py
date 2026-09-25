import pandas as pd

class ValorantMatchProcessor:
    @staticmethod
    def extract_player_stats(match_data: dict, target_name: str) -> dict | None:
        players = match_data.get("players", {}).get("all_players", [])
        
        player_data = None
        for p in players:
            if p.get("name", "").lower() == target_name.lower():
                player_data = p
                break
                
        if not player_data:
            return None

        stats = player_data.get("stats", {})
        kills = stats.get("kills", 0)
        deaths = stats.get("deaths", 0)
        assists = stats.get("assists", 0)
        rounds_played = match_data.get("metadata", {}).get("rounds_played", 1)

        score = stats.get("score", 0)
        acs = score / max(rounds_played, 1)

        return {
            "match_id": match_data.get("metadata", {}).get("matchid"),
            "map": match_data.get("metadata", {}).get("map"),
            "agent": player_data.get("character"),
            "team": player_data.get("team"),
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "kda": (kills + assists) / max(deaths, 1),
            "acs": round(acs, 1),
            "damage_made": stats.get("damage", {}).get("made", 0)
        }

    @staticmethod
    def create_dataframe(stats_list: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(stats_list)