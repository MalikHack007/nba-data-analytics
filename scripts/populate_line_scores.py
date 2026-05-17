import sqlite3
import pandas as pd
import time

from nba_api.stats.endpoints import boxscoresummaryv3

# connect to database
conn = sqlite3.connect("../data/nba.db")

# get all playoff game ids
games_df = pd.read_sql("""
SELECT DISTINCT game_id
FROM playoff_games
""", conn)

game_ids = games_df["game_id"]

count = 0
for game_id in game_ids:

    print(f"Processing {game_id}")

    try:
        summary = boxscoresummaryv3.BoxScoreSummaryV3(
            game_id=game_id
        )

        # line scores dataframe
        line_scores = summary.line_score.get_data_frame()

        # insert into sqlite
        line_scores.to_sql(
            "playoff_line_scores",
            conn,
            if_exists="append",
            index=False
        )
        count += 1
        print(f"Games processed:{count}")
        time.sleep(0.6)

    except Exception as e:
        print(f"Failed on game {game_id}")
        print(e)

conn.close()

print("Done!")