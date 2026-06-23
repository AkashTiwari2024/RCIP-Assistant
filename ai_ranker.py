import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_job(resume_text, job_description):

    prompt = f"""
You are an ATS resume analysis engine.

Your job is NOT to give a final score.

Your job is to extract matching evidence between a resume and a job posting.

Return ONLY valid JSON.

Format:

{{
  "required_skills": {{
    "job_skills": [],
    "matched": [],
    "missing": []
  }},

  "experience": {{
    "required": "",
    "candidate": "",
    "match": ""
  }},

  "responsibilities": {{
    "matched": [],
    "missing": []
  }},

  "education": {{
    "matched": [],
    "missing": []
  }},

  "strengths": [],
  "gaps": []
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

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Empty response from OpenAI")

    return content