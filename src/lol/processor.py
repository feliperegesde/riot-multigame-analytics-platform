import pandas as pd

class LolMatchProcessor:
    @staticmethod
    def extract_player_stats(match_data: dict, target_puuid: str) -> dict | None:
        if not match_data or "info" not in match_data:
            return None

        info = match_data.get("info", {})
        participants = info.get("participants", [])
        game_duration = info.get("gameDuration", 1)

        player_data = None
        team_id = None
        for participant in participants:
            if participant.get("puuid") == target_puuid:
                player_data = participant
                team_id = participant.get("teamId")
                break
        
        if not player_data:
            return None

        team_total_damage = sum(
            p.get("totalDamageDealtToChampions", 0) 
            for p in participants if p.get("teamId") == team_id
        )
        player_damage = player_data.get("totalDamageDealtToChampions", 0)
        damage_share = (player_damage / max(team_total_damage, 1)) * 100

        kills = player_data.get("kills", 0)
        deaths = player_data.get("deaths", 0)
        assists = player_data.get("assists", 0)
        total_minions = player_data.get("totalMinionsKilled", 0) + player_data.get("neutralMinionsKilled", 0)
        game_duration_min = max(game_duration / 60, 1)

        return {
            "match_id": match_data.get("metadata", {}).get("matchId", "UNKNOWN"),
            "champion_name": player_data.get("championName", "Unknown"),
            "individual_position": player_data.get("individualPosition", "UNKNOWN"),
            "win": 1 if player_data.get("win", False) else 0,
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "kda": round((kills + assists) / max(deaths, 1), 2),
            "gold_earned": player_data.get("goldEarned", 0),
            "vision_score": player_data.get("visionScore", 0),
            "wards_placed": player_data.get("wardsPlaced", 0),
            "wards_killed": player_data.get("wardsKilled", 0),
            "cs_per_min": round(total_minions / game_duration_min, 2),
            "damage_share_pct": round(damage_share, 2),
            "game_duration_min": round(game_duration_min, 1)
        }

    @staticmethod
    def create_dataframe(stats_list: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(stats_list)