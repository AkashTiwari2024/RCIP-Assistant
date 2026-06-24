from database import JobDatabase
import requests
from bs4 import BeautifulSoup
import hashlib
from urllib.parse import quote


db = JobDatabase()


# ---------------------------------
# Configuration
# ---------------------------------

SEARCH_TERMS = [
    "software developer",
    "data analyst",
    "cloud engineer",
    "cybersecurity analyst"
]


# ---------------------------------
# Generate unique job ID
# ---------------------------------

def make_id(title, company, location, index):

    raw = f"{title}|{company}|{location}|{index}"

    return hashlib.md5(
        raw.encode()
    ).hexdigest()



# ---------------------------------
# Build Job Bank URL
# ---------------------------------

def build_search_url(search_term):

    encoded_term = quote(search_term)

    return (
        "https://www.jobbank.gc.ca/"
        f"jobsearch/jobsearch?searchstring={encoded_term}"
    )



# ---------------------------------
# Scrape full job description
# ---------------------------------

def scrape_job_details(url):

    response = requests.get(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    description = soup.find(
        "div",
        class_="job-posting-detail"
    )


    if description:
        return description.text.strip()


    return "No description found"



# ---------------------------------
# Scrape search results
# ---------------------------------

def scrape_jobs(search_term):

    search_url = build_search_url(search_term)


    print("\nSearching:", search_term)


    response = requests.get(search_url)


    print(
        "Status:",
        response.status_code
    )


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    titles = soup.find_all(
        "span",
        class_="noctitle"
    )


    links = soup.find_all(
        "a",
        class_="job-link"
    )


    companies = soup.find_all(
        "li",
        class_="business"
    )


    locations = soup.find_all(
        "li",
        class_="location"
    )


    jobs = []


    for i, title_element in enumerate(titles):


        title = title_element.text.strip()


        company = (
            companies[i].text.strip()
            if i < len(companies)
            else "N/A"
        )


        location = (
            locations[i]
            .text
            .replace("Location", "")
            .strip()
            if i < len(locations)
            else "N/A"
        )


        # ----------------------------
        # Extract real job URL
        # ----------------------------

        if i < len(links):

            job_url = (
                "https://www.jobbank.gc.ca"
                + links[i]["href"]
            )

        else:

            job_url = "N/A"



        # ----------------------------
        # Scrape real description
        # ----------------------------

        if job_url != "N/A":

            description = scrape_job_details(
                job_url
            )

        else:

            description = "No description"



        job = {

            "title": title,

            "company": company,

            "location": location,

            "url": job_url,

            "description": description,

            "source": "jobbank.gc.ca"

        }



        job["id"] = make_id(
            title,
            company,
            location,
            i
        )


        jobs.append(job)


    return jobs




# ---------------------------------
# Main pipeline
# ---------------------------------

if __name__ == "__main__":


    all_jobs = []


    for term in SEARCH_TERMS:


        jobs = scrape_jobs(term)


        for job in jobs:


            db.insert_job(job)

            all_jobs.append(job)



    db.close()


    print("\n===================")

    print(
        "Total scraped:",
        len(all_jobs)
    )

    print("===================")