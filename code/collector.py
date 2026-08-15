from database import JobDatabase

import requests
from bs4 import BeautifulSoup

import hashlib
import re
from urllib.parse import quote


db = JobDatabase()


# ---------------------------------
# Configuration
# ---------------------------------

BASE_URL = "https://www.jobbank.gc.ca"


SEARCH_TERMS = [
    "software developer",
    "data analyst",
    "cloud engineer",
    "cybersecurity analyst"
]




LOCATIONS = [
    "Ontario",
    "Saskatchewan",
    "Manitoba",
    "Alberta",
    "British Columbia",
    "Nova Scotia",
    "New Brunswick",
    "Prince Edward Island",
    "Newfoundland and Labrador"
]



HEADERS = {
    "User-Agent":
        "Mozilla/5.0"
}



# ---------------------------------
# Helpers
# ---------------------------------

def clean_text(text):

    if not text:
        return ""

    return (
        text
        .replace("\n", " ")
        .replace("\t", " ")
        .strip()
    )



def make_id(url):

    match = re.search(
        r"/jobposting/(\d+)",
        url
    )

    if match:
        return match.group(1)

    return hashlib.md5(
        url.encode()
    ).hexdigest()


def extract_teer(text):

    match = re.search(
        r"TEER\s*[:\-]?\s*(\d)",
        text,
        re.IGNORECASE
    )


    if match:
        return match.group(1)


    return None



# ---------------------------------
# Build search URL
# ---------------------------------

def build_search_url(term, location):

    return (
        BASE_URL +
        "/jobsearch/jobsearch"
        f"?searchstring={quote(term)}"
        f"&locationstring={quote(location)}"
    )



# ---------------------------------
# Get Job Details
# ---------------------------------

def scrape_job_details(url):


    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        page_text = clean_text(
            soup.get_text(" ")
        )


        # Title

        title_tag = soup.find("h1")

        title = (
            clean_text(title_tag.text)
            if title_tag
            else "N/A"
        )



        # Description

        description = ""


        containers = [

            "job-posting-detail",

            "job-posting-description",

        ]


        for c in containers:

            section = soup.find(
                class_=c
            )


            if section:

                description = clean_text(
                    section.get_text(" ")
                )

                break



        if not description:

            description = page_text



        return {

            "title": title,

            "description": description,

            "teer": extract_teer(
                page_text
            )

        }



    except Exception as e:


        print(
            "Detail scrape failed:",
            e
        )


        return {

            "title": "N/A",

            "description": "",

            "teer": None
        }



# ---------------------------------
# Search Results
# ---------------------------------

def scrape_jobs(search_term, location):

    print(f"\nSearching: {search_term} in {location}")

    url = build_search_url(search_term, location)

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print("Search request failed")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    job_links = []

    # Find Job Bank posting links
    for link in soup.find_all("a", href=True):

        href = link["href"]

        if "/jobsearch/jobposting/" in href:

            job_url = (
                BASE_URL + href
                if href.startswith("/")
                else href
            )

            # Remove jsessionid and other temporary URL information
            match = re.search(
                r"(https://www\.jobbank\.gc\.ca/jobsearch/jobposting/\d+)",
                job_url
            )

            if match:
                clean_url = match.group(1)
            else:
                clean_url = job_url

            # Prevent duplicate links within this search
            if clean_url not in job_links:
                job_links.append(clean_url)

    print("Found job links:", len(job_links))

    jobs = []

    for job_url in job_links:

        print("Fetching:", job_url)

        details = scrape_job_details(job_url)

        if details is None:
            continue

        job = {
            "id": make_id(job_url),
            "title": details.get("title", ""),
            "company": details.get("company", ""),
            "location": details.get("location", ""),
            "url": job_url,
            "description": details.get("description", ""),
            "requirements": details.get("requirements", ""),
            "skills": details.get("skills", ""),
            "education": details.get("education", ""),
            "tenure": details.get("tenure", ""),
            "source": "Job Bank",
            "teer": details.get("teer", "")
        }

        jobs.append(job)

    return jobs


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    all_jobs = []

    for location in LOCATIONS:

        for term in SEARCH_TERMS:

            jobs = scrape_jobs(term, location)

            for job in jobs:

                # TEER filter
                if job["teer"]:

                    if job["teer"] not in ["0", "1", "2"]:
                        continue

                db.insert_job(job)

                all_jobs.append(job)

    db.close()

    print("\n===================")
    print("Jobs processed:", len(all_jobs))
    print("===================")