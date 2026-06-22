import json
from database import JobDatabase
from ai_ranker import rank_job

db = JobDatabase()

# -----------------------------
# Resume (you can improve later)
# -----------------------------
resume = """
Python developer with experience in:
- Python (advanced)
- SQL and database design
- Flask and REST APIs
- Data analysis (Pandas, NumPy)
- Git and Linux basics

Looking for backend or data engineering roles.
"""

# -----------------------------
# Get jobs from DB
# -----------------------------
jobs = db.get_new_jobs()

print(f"Jobs to analyze: {len(jobs)}")

# -----------------------------
# AI Processing Loop
# -----------------------------
for job in jobs:

    job_id = job[0]
    title = job[1]
    company = job[2]
    location = job[3]
    description = job[5]

    job_text = f"""
JOB TITLE:
{title}

COMPANY:
{company}

LOCATION:
{location}

INSTRUCTION:
Expand this job title into a realistic job posting.

Then evaluate match against resume.
"""

    try:
        result = rank_job(resume, job_text)

        data = json.loads(result)

        print("Analyzed:", title, "Score:", data["score"])

        db.update_job_ai(
            job_id,
            data["score"],
            ",".join(data["strengths"]),
            ",".join(data["gaps"]),
            data["recommendation"]
        )

    except Exception as e:
        print("Error processing job:", title)
        print("Error:", e)

# -----------------------------
# Cleanup
# -----------------------------
db.close()
print("AI processing complete")