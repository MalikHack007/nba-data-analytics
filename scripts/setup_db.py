import sqlite3

# creates nba.db if it does not exist
conn = sqlite3.connect("playoff_games.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    season_id TEXT,
    team_id INTEGER,
    team_abbreviation TEXT,
    team_name TEXT,
    game_id TEXT,
    game_date TEXT,
    matchup TEXT,
    wl TEXT,
    min INTEGER,
    pts INTEGER,
    fgm INTEGER,
    fga INTEGER,
    fg_pct REAL,
    fg3m INTEGER,
    fg3a INTEGER,
    fg3_pct REAL,
    ftm INTEGER,
    fta INTEGER,
    ft_pct REAL,
    oreb INTEGER,
    dreb INTEGER,
    reb INTEGER,
    ast INTEGER,
    stl INTEGER,
    blk INTEGER,
    tov INTEGER,
    pf INTEGER,
    plus_minus INTEGER
)
""")

conn.commit()

print("Database and table created!")

conn.close()