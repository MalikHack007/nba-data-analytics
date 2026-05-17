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



limit = 0

for game_id in game_ids:
    if limit >=5:
        break
    summary = boxscoresummaryv3.BoxScoreSummaryV3(game_id=game_id)
    print(summary.line_score.get_data_frame())
    limit+=1
    






