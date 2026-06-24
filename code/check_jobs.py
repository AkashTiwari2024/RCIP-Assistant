from database import JobDatabase


db = JobDatabase()

jobs = db.search_jobs("developer")


for job in jobs[:5]:

    print("\n======================")
    print("TITLE:")
    print(job["title"])

    print("\nCOMPANY:")
    print(job["company"])

    print("\nURL:")
    print(job["url"])

    print("\nDESCRIPTION:")
    print(job["description"][:500])


db.close()