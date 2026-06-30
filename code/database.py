import json
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
            requirements TEXT,
            skills TEXT,
            education TEXT,
            tenure TEXT,
            source TEXT,
            status TEXT DEFAULT 'new',
            score INTEGER,
            strengths TEXT,
            gaps TEXT,
            recommendation TEXT,
            teer TEXT,

            category TEXT,
            confidence REAL,
            signals TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()


    def insert_job(self, job):
        self.cursor.execute("""
            INSERT OR IGNORE INTO jobs (
                id, title, company, location, url,
                description, source, teer
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job["id"],
            job["title"],
            job["company"],
            job["location"],
            job["url"],
            job["description"],
            job["source"],
            job["teer"]
        ))
        self.conn.commit()


    def get_new_jobs(self):
        self.cursor.execute("""
            SELECT *
            FROM jobs
            WHERE status = 'new'
        """)
        return self.cursor.fetchall()


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


    def update_job_analysis(
        self,
        job_id,
        category,
        confidence,
        signals,
        score,
        recommendation,
        strengths,
        gaps
    ):
        query = """
        UPDATE jobs
        SET
            category = ?,
            confidence = ?,
            signals = ?,
            score = ?,
            recommendation = ?,
            strengths = ?,
            gaps = ?
        WHERE id = ?
        """

        self.cursor.execute(
            query,
            (
                category,
                confidence,
                json.dumps(signals),
                score,
                recommendation,
                json.dumps(strengths),
                json.dumps(gaps),
                job_id
            )
        )

        self.conn.commit()

    def get_apply_jobs(self):

        query = """
    SELECT
        title,
        company,
        location,
        score,
        recommendation,
        category,
        strengths,
        gaps,
        url
    FROM jobs
    WHERE recommendation = 'apply'
    ORDER BY score DESC
    """

        self.cursor.execute(query)

        return self.cursor.fetchall()
    
    def get_high_confidence_it_jobs(self):
        self.cursor.execute("""
            SELECT *
            FROM jobs
            WHERE category = 'it'
            AND confidence >= 0.7
            ORDER BY score DESC
            """)
        return self.cursor.fetchall()
    
    def get_sales_jobs(self):
        self.cursor.execute("""
            SELECT *
            FROM jobs
            WHERE category = 'sales'
            ORDER BY score DESC
            """)
        return self.cursor.fetchall()

    def get_hybrid_jobs(self):
        self.cursor.execute("""
            SELECT *
            FROM jobs
            WHERE category = 'hybrid'
            ORDER BY confidence ASC
            """)
        return self.cursor.fetchall()


    def get_low_confidence_jobs(self):
        self.cursor.execute("""
            SELECT *
            FROM jobs
            WHERE confidence < 0.5
            ORDER BY confidence ASC
            """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    def get_maybe_jobs(self):

        query = """
    SELECT
        title,
        company,
        location,
        score,
        recommendation,
        category,
        url
    FROM jobs
    WHERE recommendation = 'maybe'
    ORDER BY score DESC
    """

        self.cursor.execute(query)

        return self.cursor.fetchall()
    
    def get_top_jobs(self, limit=10):

        query = """
    SELECT
        title,
        company,
        location,
        score,
        recommendation,
        category
    FROM jobs
    WHERE score IS NOT NULL
    ORDER BY score DESC
    LIMIT ?
    """

        self.cursor.execute(
        query,
        (limit,)
    )

        return self.cursor.fetchall()


if __name__ == "__main__":
    db = JobDatabase()
    print("Database created")
    db.close()