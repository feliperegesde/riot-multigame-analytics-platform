import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from src.api_client import LolAPIClient
from src.processor import MatchProcessor
from src.cluster_model import PlaystyleClusterer

app = FastAPI(title="LoL Advanced Analytics API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    api_key: str
    game_name: str
    tag_line: str
    match_count: int = 10

@app.post("/api/analyze")
def analyze_player(req: AnalysisRequest):
    try:
        client = LolAPIClient(req.api_key)
        puuid = client.get_puuid_by_riot_id(req.game_name, req.tag_line)
        match_ids = client.get_match_ids(puuid, count=req.match_count)
        
        if not match_ids:
            raise HTTPException(status_code=404, detail="Nenhuma partida recente encontrada para este invocador.")
        
        valid_stats = []
        for m in match_ids:
            try:
                match_details = client.get_match_details(m)
                parsed = MatchProcessor.extract_player_stats(match_details, puuid)
                if parsed:
                    valid_stats.append(parsed)
            except requests.exceptions.HTTPError as he:
                # Se bater rate limit da Riot (429), aguarda um momento ou ignora a partida isolada
                if he.response.status_code == 429:
                    time.sleep(1.0)
                    continue
                raise he
        
        if not valid_stats:
            raise HTTPException(status_code=404, detail="Não foi possível extrair estatísticas das partidas encontradas.")
            
        df = MatchProcessor.create_dataframe_from_stats(valid_stats)
        clusterer = PlaystyleClusterer()
        df = clusterer.fit_predict(df, ["kda", "cs_per_min", "damage_share_pct", "vision_score"])

        return {
            "summoner": f"{req.game_name}#{req.tag_line}",
            "total_matches": len(df),
            "winrate": round(float(df['win'].mean() * 100), 1),
            "avg_kda": round(float(df['kda'].mean()), 2),
            "avg_damage_share": round(float(df['damage_share_pct'].mean()), 1),
            "avg_cs_min": round(float(df['cs_per_min'].mean()), 1),
            "matches": df.to_dict(orient="records")
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)