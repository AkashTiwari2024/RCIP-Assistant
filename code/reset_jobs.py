import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE jobs
SET status = 'new',
score = NULL,
strengths = NULL,
gaps = NULL,
recommendation = NULL
""")

conn.commit()
conn.close()

print("Jobs reset")