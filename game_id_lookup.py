from nba_api.stats.endpoints import boxscoresummaryv3

game_id = "0042500137"

game = boxscoresummaryv3.BoxScoreSummaryV3(
    game_id=game_id
)

print(game.get_data_frames())