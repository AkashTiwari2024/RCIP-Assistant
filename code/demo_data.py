DEMO_JOBS = [
    {
        "id": "demo-001",
        "title": "IT Support Technician",
        "company": "Demo Technology Inc.",
        "location": "Ontario",
        "url": "",
        "description": "Demo job used to show the RCIP Assistant dashboard.",
        "source": "demo",
        "teer": "2",
        "category": "it",
        "confidence": 0.90,
        "signals": ["technical support", "troubleshooting", "networking"],
        "score": 82,
        "recommendation": "apply",
        "strengths": [
            "Technical troubleshooting",
            "Windows support",
            "Customer service",
            "Networking fundamentals"
        ],
        "gaps": [
            "Limited enterprise Active Directory experience"
        ]
    },

    {
        "id": "demo-002",
        "title": "Junior Systems Support Analyst",
        "company": "Demo Systems Ltd.",
        "location": "Ontario",
        "url": "",
        "description": "Demo job used to show the RCIP Assistant dashboard.",
        "source": "demo",
        "teer": "2",
        "category": "it",
        "confidence": 0.88,
        "signals": ["python", "sql", "linux", "support"],
        "score": 76,
        "recommendation": "apply",
        "strengths": [
            "Python",
            "SQL",
            "Linux fundamentals",
            "Technical troubleshooting"
        ],
        "gaps": [
            "Limited production server administration experience"
        ]
    },

    {
        "id": "demo-003",
        "title": "Technical Sales Representative",
        "company": "Demo Industrial Solutions",
        "location": "Manitoba",
        "url": "",
        "description": "Demo job used to show the RCIP Assistant dashboard.",
        "source": "demo",
        "teer": "2",
        "category": "sales",
        "confidence": 0.94,
        "signals": ["technical sales", "account management", "business development"],
        "score": 88,
        "recommendation": "apply",
        "strengths": [
            "Technical sales experience",
            "Account management",
            "Customer relationship management",
            "Business development"
        ],
        "gaps": [
            "Limited experience with the employer's specific product line"
        ]
    },

    {
        "id": "demo-004",
        "title": "Customer Success Specialist",
        "company": "Demo Software Corp.",
        "location": "Ontario",
        "url": "",
        "description": "Demo job used to show the RCIP Assistant dashboard.",
        "source": "demo",
        "teer": "2",
        "category": "hybrid",
        "confidence": 0.78,
        "signals": ["customer service", "software", "technical communication"],
        "score": 67,
        "recommendation": "maybe",
        "strengths": [
            "Customer service",
            "Technical communication",
            "Problem solving"
        ],
        "gaps": [
            "Limited SaaS customer success experience"
        ]
    },

    {
        "id": "demo-005",
        "title": "Network Support Technician",
        "company": "Demo Networks Inc.",
        "location": "Saskatchewan",
        "url": "",
        "description": "Demo job used to show the RCIP Assistant dashboard.",
        "source": "demo",
        "teer": "2",
        "category": "it",
        "confidence": 0.81,
        "signals": ["tcp/ip", "networking", "linux"],
        "score": 61,
        "recommendation": "maybe",
        "strengths": [
            "TCP/IP fundamentals",
            "Technical troubleshooting",
            "Linux fundamentals"
        ],
        "gaps": [
            "Cisco certification",
            "Enterprise networking experience"
        ]
    }
]


def load_demo_jobs(db):

    # Only load demo jobs when the dashboard database is empty
    if db.get_dashboard_jobs():
        return

    for job in DEMO_JOBS:

        db.insert_job(job)

        db.update_job_analysis(
            job["id"],
            job["category"],
            job["confidence"],
            job["signals"],
            job["score"],
            job["recommendation"],
            job["strengths"],
            job["gaps"]
        )