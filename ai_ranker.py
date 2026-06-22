import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def rank_job(resume_text, job_description):

    prompt = f"""
You are a professional ATS (Applicant Tracking System).

You evaluate job-resume matches.

IMPORTANT SCORING RULES:
- 0–30 = poor match (no relevant skills)
- 31–60 = partial match (some overlap)
- 61–85 = strong match (good fit)
- 86–100 = excellent match (direct fit)

You MUST spread scores across this range.

Return ONLY valid JSON:

{{
  "score": 0-100,
  "strengths": [],
  "gaps": [],
  "recommendation": "apply | maybe | skip"
}}

RESUME:
{resume_text}

JOB:
{job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content