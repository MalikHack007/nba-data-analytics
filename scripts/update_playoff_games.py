import sqlite3
import pandas as pd

from nba_api.stats.endpoints import leaguegamefinder

# -----------------------------------
# CONNECT TO DATABASE
# -----------------------------------

conn = sqlite3.connect("../data/nba.db")

# -----------------------------------
# GET LATEST GAME DATE
# -----------------------------------

query = """
SELECT MAX(GAME_DATE) AS latest_game
FROM playoff_games
"""

latest_game_df = pd.read_sql(query, conn)

latest_game = latest_game_df.iloc[0]["latest_game"]

print(f"Latest game in DB: {latest_game}")

# -----------------------------------
# FETCH PLAYOFF GAMES
# -----------------------------------

games = leaguegamefinder.LeagueGameFinder(
    season_type_nullable="Playoffs"
)

games_df = games.get_data_frames()[0]

# -----------------------------------
# FILTER ONLY NEWER GAMES
# -----------------------------------

games_df["GAME_DATE"] = pd.to_datetime(
    games_df["GAME_DATE"]
)

latest_game = pd.to_datetime(latest_game)

new_games_df = games_df[
    games_df["GAME_DATE"] > latest_game
]

new_games_df = new_games_df.drop_duplicates(subset=['GAME_ID'])
# -----------------------------------
# HANDLE NO NEW GAMES
# -----------------------------------

if len(new_games_df) == 0:

    print("No new playoff games found.")

else:

    print(f"Found {len(new_games_df)} new rows.")

    # append into sqlite
    new_games_df.to_sql(
        "playoff_games",
        conn,
        if_exists="append",
        index=False
    )

    print("Inserted new playoff games.")

conn.close()