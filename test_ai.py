from ai_ranker import rank_job

resume = """
Python developer with experience in SQL, Flask, and data analysis.
"""

job = """
Looking for a Python developer with SQL and API experience.
"""

result = rank_job(resume, job)

print(result)