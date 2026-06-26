import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_job(resume, job_text):

    messages = [
        {
            "role": "system",
            "content": """
You are an AI job matching system for ENTRY-LEVEL candidates.

Rules:
- Candidate is early career / student level
- Allow transferable skills
- Do not require enterprise tools
- Be realistic in scoring
- Prefer semantic matching

Return ONLY valid JSON:

{
  "required_skills": {
    "job_skills": [],
    "matched": [],
    "missing": []
  },
  "strengths": [],
  "gaps": [],
  "explanation": ""
}

No markdown. No extra text.
"""
        },
        {
            "role": "user",
            "content": f"""
CANDIDATE SKILLS:
{resume["skills"]}

EXPERIENCE FOCUS:
{resume.get("experience_focus", "general")}

JOB:
{job_text}
"""
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content