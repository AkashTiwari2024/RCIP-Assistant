import json
import re
from database import JobDatabase
from ai_ranker import analyze_job
from scoring import calculate_total_score

db = JobDatabase()

# -----------------------------
# Resume Profiles
# -----------------------------
RESUMES = {

    "it": {
        "skills": [
            "Python", "SQL", "C++", "Git",
            "REST APIs", "Linux", "Proxmox",
            "Debugging", "Data Analysis"
        ],
        "experience_focus": "technical"
    },

    "sales": {
        "skills": [
            "Stakeholder Management",
            "Marketing Strategy",
            "Retail Operations",
            "Budgeting",
            "Customer Engagement",
            "Project Coordination"
        ],
        "experience_focus": "business"
    }
}

# -----------------------------
# Job Classifier
# -----------------------------
def classify_job(job_text):

    text = job_text.lower()

    tech_keywords = {
        "software": 3,
        "developer": 3,
        "python": 4,
        "sql": 4,
        "engineer": 3,
        "cloud": 3,
        "it": 2,
        "cyber": 3,
        "api": 3,
        "backend": 3,
        "data": 2
    }

    sales_keywords = {
        "sales": 4,
        "marketing": 4,
        "retail": 3,
        "customer": 3,
        "brand": 3,
        "account": 3,
        "manager": 2,
        "business": 2,
        "promotion": 2
    }

    tech_score = sum(weight for k, weight in tech_keywords.items() if k in text)
    sales_score = sum(weight for k, weight in sales_keywords.items() if k in text)

    # IMPORTANT: add tie-breaker logic
    if abs(tech_score - sales_score) <= 2:
        # fallback based on title strength
        if "developer" in text or "engineer" in text:
            return "it"
        if "sales" in text or "marketing" in text:
            return "sales"

    return "it" if tech_score > sales_score else "sales"


# -----------------------------
# Clean AI JSON output
# -----------------------------
def clean_json(text):
    text = text.strip()
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()


# -----------------------------
# Get jobs
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
REAL JOB POSTING ANALYSIS

TITLE: {title}
COMPANY: {company}
LOCATION: {location}

FULL DESCRIPTION:
{description}

TASK:
1. Extract required skills from the job description
2. Match skills against candidate profile using both exact and transferable skills
3. Allow semantic matching (Python → scripting, automation, backend thinking)
4. Identify missing skills realistically for an entry-level candidate
5. Do NOT require enterprise tools for a positive score
"""

    # -----------------------------
    # Classify job type (cleaned)
    # -----------------------------
    profile_type = classify_job(title)

    if profile_type not in RESUMES:
        profile_type = "it"

    resume = RESUMES[profile_type]

    try:

        result = analyze_job(resume, job_text)

        cleaned = clean_json(result)
        analysis = json.loads(cleaned)

        # -----------------------------
        # Score calculation
        # -----------------------------
        score_data = calculate_total_score(analysis)
        score = score_data["score"]

        strengths = analysis.get("strengths", [])
        gaps = analysis.get("gaps", [])

        # -----------------------------
        # Recommendation logic
        # -----------------------------
        if score >= 70:
            recommendation = "apply"
        elif score >= 45:
            recommendation = "maybe"
        else:
            recommendation = "skip"

        # -----------------------------
        # Output
        # -----------------------------
        print("\n" + "=" * 50)
        print(f"Job: {title}")
        print(f"Company: {company}")
        print(f"Score: {score}/100")
        print(f"Recommendation: {recommendation}")
        print("=" * 50)

        print("\nMatched Skills:")
        print(", ".join(
            analysis.get("required_skills", {}).get("matched", [])
        ))

        print("\nMissing Skills:")
        print(", ".join(
            analysis.get("required_skills", {}).get("missing", [])
        ))

        print("\nGaps:")
        for gap in gaps:
            print("-", gap)

        # -----------------------------
        # OPTIONAL: store results in DB (if implemented)
        # -----------------------------
        # db.update_job(job_id, score, json.dumps(gaps), recommendation)

    except Exception as e:
        print(f"Error analyzing job {job_id}: {e}")


# -----------------------------
# Cleanup
# -----------------------------
db.close()

print("\nAI processing complete")