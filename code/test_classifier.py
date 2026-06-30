from ai_pipeline import classify_job


jobs = [

    {
        "title": "Junior Python Developer",
        "description": "Looking for a developer with Python, SQL, backend API experience"
    },

    {
        "title": "Sales Representative",
        "description": "Responsible for customer relationships, marketing, and revenue growth"
    },

    {
        "title": "Technical Account Manager",
        "description": "Work with clients using cloud software solutions and account management"
    },

    {
        "title": "IT Support Technician",
        "description": "Troubleshooting networks, computers, software and technical issues"
    }

]


for job in jobs:

    # combine title + description because classifier currently accepts text
    job_text = (
        job["title"] 
        + "\n" 
        + job["description"]
    )

    result = classify_job(job_text)

    print("=" * 50)
    print("JOB:")
    print(job["title"])

    print("\nRESULT:")
    print(result)