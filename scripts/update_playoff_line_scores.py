import sqlite3
import pandas as pd
import time

from nba_api.stats.endpoints import boxscoresummaryv3

# -----------------------------------
# CONNECT TO DATABASE
# -----------------------------------

conn = sqlite3.connect("../data/nba.db")

# -----------------------------------
# FIND MISSING GAME IDS
# -----------------------------------

query = """
SELECT DISTINCT game_id AS GAME_ID
FROM playoff_games

WHERE GAME_ID NOT IN (

    SELECT DISTINCT gameId
    FROM playoff_line_scores
)
"""

missing_games_df = pd.read_sql(query, conn)

missing_game_ids = missing_games_df["GAME_ID"].tolist()

print(f"Missing games: {len(missing_game_ids)}")

# -----------------------------------
# HANDLE NO NEW GAMES
# -----------------------------------

if len(missing_game_ids) == 0:

    print("playoff_line_scores already up to date.")

else:

    for game_id in missing_game_ids:

        print(f"Processing {game_id}")

        try:

            summary = boxscoresummaryv3.BoxScoreSummaryV3(
                game_id=game_id
            )

            line_scores = summary.line_score.get_data_frame()

            # keep only columns we want
            line_scores = line_scores[
                [
                    'gameId',
                    'teamId',
                    'teamCity',
                    'teamName',
                    'teamTricode',
                    'teamSlug',
                    'teamWins',
                    'teamLosses',
                    'period1Score',
                    'period2Score',
                    'period3Score',
                    'period4Score',
                    'score'
                ]
            ]

            # insert into sqlite
            line_scores.to_sql(
                "playoff_line_scores",
                conn,
                if_exists="append",
                index=False
            )

            print(f"Inserted {game_id}")

            time.sleep(0.6)

        except Exception as e:

            print(f"Failed on {game_id}")
            print(e)

conn.close()

print("Done.")