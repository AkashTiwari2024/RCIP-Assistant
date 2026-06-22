import sqlite3

def search_jobs(query):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, company, location, url
        FROM jobs
        WHERE title LIKE ?
        OR company LIKE ?
        OR location LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))

    results = cursor.fetchall()

    conn.close()

    return results


query = input("Search jobs: ")

results = search_jobs(query)

for job in results:
    print(job)