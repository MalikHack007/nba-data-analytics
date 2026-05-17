import sqlite3

conn = sqlite3.connect("../data/nba.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS playoff_line_scores (
    gameId TEXT,
    teamId INTEGER,
    teamCity TEXT,
    teamName TEXT,
    teamTricode TEXT,
    teamSlug TEXT,
    teamWins INTEGER,
    teamLosses INTEGER,
    period1Score INTEGER,
    period2Score INTEGER,
    period3Score INTEGER,
    period4Score INTEGER,
    score INTEGER,

    PRIMARY KEY (gameId, teamId)
)
""")

conn.commit()

print("playoff_line_scores table created!")

conn.close()