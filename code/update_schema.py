from database import JobDatabase

db = JobDatabase()

db.cursor.execute("ALTER TABLE jobs ADD COLUMN category TEXT")
db.cursor.execute("ALTER TABLE jobs ADD COLUMN confidence REAL")
db.cursor.execute("ALTER TABLE jobs ADD COLUMN signals TEXT")

db.conn.commit()
db.close()

print("Schema updated")