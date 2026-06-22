from database import JobDatabase
import requests
from bs4 import BeautifulSoup
import hashlib

db = JobDatabase()

# -----------------------------
# Generate unique job ID
# -----------------------------
def make_id(title, company, location, index):
    raw = f"{title}|{company}|{location}|{index}"
    return hashlib.md5(raw.encode()).hexdigest()

# -----------------------------
# Scrape Job Bank
# -----------------------------
url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=information+technology+support"

response = requests.get(url)
print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("span", class_="noctitle")
companies = soup.find_all("li", class_="business")
locations = soup.find_all("li", class_="location")

jobs = []

for i in range(len(titles)):

    title = titles[i].text.strip()

    company = companies[i].text.strip() if i < len(companies) else "N/A"

    location = locations[i].text.replace("Location", "").strip() if i < len(locations) else "N/A"

    # -----------------------------
    # IMPORTANT FIX: Better description
    # -----------------------------
    description = f"""
This is a {title} role at {company} in {location}.
Likely responsibilities include:
- Technical troubleshooting
- User support
- System maintenance
- IT infrastructure support

Skills typically required:
- Problem solving
- Basic networking
- Windows/Linux support
- Communication skills
""".strip()

    job = {
    "title": title,
    "company": company,
    "location": location,
    "url": "N/A",
    "description": description,
    "source": "jobbank.gc.ca"
}

    job["id"] = make_id(title, company, location, i)

    jobs.append(job)

    db.insert_job(job)

db.close()

print(f"Total scraped: {len(jobs)}")
print("Total stored (approx check):", len(jobs))