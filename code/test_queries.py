from database import JobDatabase

db = JobDatabase()

print("\nTOP APPLY JOBS")
for job in db.get_apply_jobs():
    print(job["title"], job["score"])

print("\nHIGH CONFIDENCE IT JOBS")
for job in db.get_high_confidence_it_jobs():
    print(job["title"], job["confidence"])

print("\nHYBRID JOBS")
for job in db.get_hybrid_jobs():
    print(job["title"], job["confidence"])