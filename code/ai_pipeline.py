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
        "developer": 5,
        "python": 5,
        "sql": 5,
        "engineer": 4,
        "cloud": 3,
        "cyber": 5,
        "api": 4,
        "backend": 5,
        "database": 4,
        "network": 4,
        "linux": 4,
        "programming": 5
    }


    sales_keywords = {

        "sales": 5,
        "marketing": 5,
        "retail": 3,
        "customer": 3,
        "client": 3,
        "brand": 3,
        "promotion": 3,
        "revenue": 4,
        "commission": 4,
        "account management": 4
    }


    tech_score = 0
    sales_score = 0

    tech_signals = []
    sales_signals = []


    for keyword, weight in tech_keywords.items():

        if keyword in text:
            tech_score += weight
            tech_signals.append(keyword)


    for keyword, weight in sales_keywords.items():

        if keyword in text:
            sales_score += weight
            sales_signals.append(keyword)


    title = text.split("\n")[0]


    if any(word in title for word in [
        "developer",
        "engineer",
        "programmer",
        "analyst"
    ]):

        tech_score += 5


    if any(word in title for word in [
        "sales",
        "representative",
        "marketing",
        "advisor"
    ]):

        sales_score += 5


    total = tech_score + sales_score


    if total == 0:

        return {

            "category": "unknown",
            "confidence": 0,
            "tech_score": 0,
            "sales_score": 0,
            "signals": {}

        }


    difference = abs(
        tech_score - sales_score
    )


    confidence = min(
        difference / 10,
        1
    )


    if difference <= 2:

        category = "hybrid"

    elif tech_score > sales_score:

        category = "it"

    else:

        category = "sales"


    return {

        "category": category,
        "confidence": round(confidence, 2),
        "tech_score": tech_score,
        "sales_score": sales_score,
        "signals": {

            "tech": tech_signals,
            "sales": sales_signals

        }

    }




# -----------------------------
# Clean AI JSON output
# -----------------------------
def clean_json(text):

    text = text.strip()

    text = re.sub(
        r"```json",
        "",
        text
    )

    text = re.sub(
        r"```",
        "",
        text
    )

    return text.strip()




# -----------------------------
# Main Pipeline
# -----------------------------
def run_pipeline():


    jobs = db.get_new_jobs()


    print(
        f"Jobs to analyze: {len(jobs)}"
    )


    for job in jobs:


        job_id = job[0]

        title = job[1]

        company = job[2]

        location = job[3]

        description = job[5]



        job_text = f"""

REAL JOB POSTING ANALYSIS


TITLE:
{title}


COMPANY:
{company}


LOCATION:
{location}


FULL DESCRIPTION:

{description}


TASK:

1. Extract required skills
2. Match against candidate profile
3. Allow transferable skills
4. Do not over-penalize missing enterprise tools

"""



        classification = classify_job(title)


        profile_type = classification["category"]


        if profile_type not in RESUMES:

            profile_type = "it"


        resume = RESUMES[profile_type]



        try:


            result = analyze_job(
                resume,
                job_text
            )


            cleaned = clean_json(result)


            analysis = json.loads(cleaned)



            score_data = calculate_total_score(
                analysis
            )


            score = score_data["score"]



            if score >= 70:

                recommendation = "apply"


            elif score >= 45:

                recommendation = "maybe"


            else:

                recommendation = "skip"



            # -----------------------------
            # Save AI results to database
            # -----------------------------

            db.update_job_analysis(

                job_id,

                classification["category"],

                classification["confidence"],

                classification["signals"],

                score,

                recommendation,

                analysis["strengths"],

                analysis["gaps"]

            )



            print("\n" + "="*50)

            print(
                f"Job: {title}"
            )

            print(
                f"Type: {profile_type}"
            )

            print(
                f"Score: {score}"
            )

            print(
                f"Recommendation: {recommendation}"
            )

            print("="*50)




        except Exception as e:


            print(
                f"Error analyzing job {job_id}: {e}"
            )



    db.close()


    print(
        "\nAI processing complete"
    )




# -----------------------------
# Only run when executing file
# -----------------------------
if __name__ == "__main__":

    run_pipeline()