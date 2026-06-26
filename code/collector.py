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


LOCATION = "Thunder Bay"


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

def build_search_url(term):

    return (
        BASE_URL +
        "/jobsearch/jobsearch"
        f"?searchstring={quote(term)}"
        f"&locationstring={quote(LOCATION)}"
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

def scrape_jobs(term):

    url = build_search_url(term)

    print("\nSearching:", term)

    response = requests.get(url, headers=HEADERS)

    print("Status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # ONLY job posting links
    links = soup.select("a[href*='/jobsearch/jobposting/']")

    print("Found job links:", len(links))

    for link in links:

        href = link["href"]

        job_url = (
            BASE_URL + href
            if href.startswith("/")
            else href
        )

        print("Fetching:", job_url)

        details = scrape_job_details(job_url)

        job = {
            "id": make_id(job_url),
            "title": details["title"],
            "company": "N/A",
            "location": LOCATION,
            "url": job_url,
            "description": details["description"],
            "source": "jobbank.gc.ca",
            "teer": details.get("teer", "N/A")
        }

        jobs.append(job)

    return jobs


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":


    all_jobs = []


    for term in SEARCH_TERMS:


        jobs = scrape_jobs(term)



        for job in jobs:


            # TEER filter

            if job["teer"]:

                if job["teer"] not in [
                    "0",
                    "1",
                    "2"
                ]:

                    continue



            db.insert_job(
                job
            )


            all_jobs.append(
                job
            )



    db.close()



    print(
        "\n==================="
    )

    print(
        "Total stored:",
        len(all_jobs)
    )

    print(
        "==================="
    )