from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import boxscoresummaryv3
import pandas as pd

import time

#get all playoff games
games = leaguegamefinder.LeagueGameFinder(
    season_type_nullable='Playoffs'
)

games_df = games.get_data_frames()[0]

games_df = games_df.drop_duplicates(subset=['GAME_ID'])

game_ids = games_df['GAME_ID']

# -----------------------------
# Tracking variables
# -----------------------------
total_15pt_deficits = 0
comeback_wins = 0

results = []

limit = 20
iterated = 0

# Iterate through games
for game_id in game_ids:
    iterated += 1
    try:
        # print(f"Processing game {game_id}")

        # Fetch box score summary
        summary = boxscoresummaryv3.BoxScoreSummaryV3(
            game_id=game_id
        )

        # Quarter-by-quarter scores
        line_score = summary.line_score.get_data_frame()

        # Skip malformed games
        if len(line_score) != 2:
            continue

        line_score['PTS_THROUGH_Q3'] = (
            line_score['period1Score']
            + line_score['period2Score']
            + line_score['period3Score']
        )

        team1 = line_score.iloc[0]
        team2 = line_score.iloc[1]

        q3_diff = team1['PTS_THROUGH_Q3'] - team2['PTS_THROUGH_Q3']

        # Final scores
        team1_final = team1['score']
        team2_final = team2['score']

        # -----------------------------
        # Determine if team1 was trailing
        # -----------------------------
        if q3_diff <= -15:

            total_15pt_deficits += 1

            trailing_team = team1['teamTricode']

            comeback = team1_final > team2_final

            if comeback:
                comeback_wins += 1

            results.append({
                'GAME_ID': game_id,
                'TRAILING_TEAM': trailing_team,
                'DEFICIT_ENTERING_Q4': abs(q3_diff),
                'COMEBACK_WIN': comeback
            })

        # -----------------------------
        # Determine if team2 was trailing
        # -----------------------------
        elif q3_diff >= 15:

            total_15pt_deficits += 1

            trailing_team = team2['teamTricode']

            comeback = team2_final > team1_final

            if comeback:
                comeback_wins += 1

            results.append({
                'GAME_ID': game_id,
                'TRAILING_TEAM': trailing_team,
                'DEFICIT_ENTERING_Q4': abs(q3_diff),
                'COMEBACK_WIN': comeback
            })

    except Exception as e:
        print(f"Error processing game {game_id}: {e}")
    if iterated > limit:
        print(f"Reached iteration limit of {limit}. Stopping.")
        break
    # Avoid rate limits
    time.sleep(0.6)

# -----------------------------
# Final Results
# -----------------------------
results_df = pd.DataFrame(results)

print("\n========================")
print("FINAL RESULTS")
print("========================")

print(f"Total 15+ point deficits entering Q4: {total_15pt_deficits}")
print(f"Comeback wins: {comeback_wins}")

if total_15pt_deficits > 0:
    comeback_rate = (
        comeback_wins / total_15pt_deficits
    ) * 100

    print(f"Comeback rate: {comeback_rate:.2f}%")

print("\nSample Results:")
print(results_df.head())

