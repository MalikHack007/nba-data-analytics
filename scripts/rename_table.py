import sqlite3

conn = sqlite3.connect("nba.db")

cursor = conn.cursor()

cursor.execute("""
ALTER TABLE games
RENAME TO playoff_games;
""")

conn.commit()

conn.close()

print("Table renamed!")