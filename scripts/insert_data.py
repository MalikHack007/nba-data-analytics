import sqlite3
from nba_api.stats.endpoints import leaguegamefinder

#get all playoff games
games = leaguegamefinder.LeagueGameFinder(
    season_type_nullable='Playoffs'
)

games_df = games.get_data_frames()[0]

games_df = games_df.drop_duplicates(subset=['GAME_ID'])

conn = sqlite3.connect("nba.db")

games_df.to_sql(
    "playoff_games",
    conn,
    if_exists="append",
    index=False
)

conn.close()

print("Data inserted!")
