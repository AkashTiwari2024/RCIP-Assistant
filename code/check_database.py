from database import JobDatabase


db = JobDatabase()


db.cursor.execute(
    """
    SELECT title, url
    FROM jobs
    LIMIT 5
    """
)


rows = db.cursor.fetchall()


for row in rows:
    print("Title:", row["title"])
    print("URL:", row["url"])
    print("-" * 50)


db.close()