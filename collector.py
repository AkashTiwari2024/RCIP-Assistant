import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib


# -----------------------------
# Generate unique job ID
# -----------------------------
def make_id(title, company, location):
    raw = title + company + location
    return hashlib.md5(raw.encode()).hexdigest()


# -----------------------------
# Save job to database
# -----------------------------
def save_job(job):

    connection = sqlite3.connect("jobs.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO jobs
        (id, title, company, location, url, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        job["id"],
        job["title"],
        job["company"],
        job["location"],
        job["url"],
        job["description"]
    ))

    connection.commit()
    connection.close()


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

    location = (
        locations[i].text.replace("Location", "").strip()
        if i < len(locations)
        else "N/A"
    )

    job = {
        "title": title,
        "company": company,
        "location": location,
        "url": "N/A",
        "description": "N/A"
    }

    # add unique ID
    job["id"] = make_id(job["title"], job["company"], job["location"])

    jobs.append(job)
    save_job(job)


# -----------------------------
# Save CSV backup
# -----------------------------
df = pd.DataFrame(jobs)
df.to_csv("jobs.csv", index=False)

print("jobs.csv saved successfully")
print(f"Total jobs scraped: {len(jobs)}")