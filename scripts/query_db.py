import sqlite3
import pandas as pd

conn = sqlite3.connect("nba.db")

query = """
SELECT
    TEAM_NAME,
    GAME_DATE,
    MATCHUP,
    WL,
    PTS
FROM playoff_games
LIMIT 100
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()