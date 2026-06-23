import sqlite3

DATABASE_NAME = "jobs.db"


class JobDatabase:

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            url TEXT,
            description TEXT,
            source TEXT,
            status TEXT DEFAULT 'new',
            score INTEGER,
            strengths TEXT,
            gaps TEXT,
            recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def insert_job(self, job):
        self.cursor.execute("""
        INSERT OR IGNORE INTO jobs (
            id, title, company, location, url, description, source
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            job["id"],
            job["title"],
            job["company"],
            job["location"],
            job["url"],
            job["description"],
            job["source"]
        ))
        self.conn.commit()

    def search_jobs(self, keyword):
        self.cursor.execute("""
        SELECT *
        FROM jobs
        WHERE title LIKE ?
        OR company LIKE ?
        OR location LIKE ?
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ))
        return self.cursor.fetchall()

    def get_new_jobs(self):
        self.cursor.execute("""
        SELECT *
        FROM jobs
        WHERE status = 'new'
        """)
        return self.cursor.fetchall()

    def update_job_ai(self, job_id, score, strengths, gaps, recommendation):
        self.cursor.execute("""
        UPDATE jobs
        SET score = ?,
            strengths = ?,
            gaps = ?,
            recommendation = ?,
            status = 'analyzed'
        WHERE id = ?
        """, (
            score,
            strengths,
            gaps,
            recommendation,
            job_id
        ))
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = JobDatabase()
    print("Database created")

    # Optional quick debug test (keep it simple)
    for row in db.get_new_jobs():
        print(row)

    db.close()