import json
from database import JobDatabase
from ai_ranker import analyze_job
from scoring import calculate_total_score

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
        result = analyze_job(
            resume,
            job_text
        )

        try:
            analysis = json.loads(result)
        except Exception as e:
            print("\n❌ RAW AI OUTPUT:")
            print(result)
            print("\n❌ PARSE ERROR:", e)
            continue

        print("\nMatched Skills:")
        print(", ".join(
            analysis["required_skills"]["matched"]
        ))

        print("\nMissing Skills:")
        print(", ".join(
            analysis["required_skills"]["missing"]
        ))

        print("\nGaps:")
        for gap in analysis["gaps"]:
            print("-", gap)

        score_data = calculate_total_score(analysis)

        score = score_data["score"]

        strengths = analysis.get("strengths", [])

        gaps = analysis.get("gaps", [])

        if score >= 70:
            recommendation = "apply"

        elif score >= 45:
            recommendation = "maybe"

        else:
            recommendation = "skip"

        print("\n" + "=" * 50)
        print(f"Job: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Score: {score}/100")
        print(f"Recommendation: {recommendation}")
        print("=" * 50)

    except Exception as e:
        print(f"Error analyzing job {job_id}: {e}")
        continue

# -----------------------------
# Cleanup
# -----------------------------

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0,
    response_format={"type": "json_object"}  # 🔥 ADD THIS
)
db.close()
print("AI processing complete")