from sqlmodel import Field, SQLModel, create_engine, Session

class PlayerMatchStats(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    puuid: str = Field(index=True)
    match_id: str = Field(index=True)
    champion_name: str
    win: bool
    kills: int
    deaths: int
    assists: int
    gold_earned: int
    vision_score: int
    total_minions_killed: int
    game_duration: int

DATABASE_URL = "sqlite:///lol_scouting.db"
engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)