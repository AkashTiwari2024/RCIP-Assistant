import requests
from bs4 import BeautifulSoup
import pandas as pd

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
        locations[i]
        .text
        .replace("Location", "")
        .strip()
        if i < len(locations)
        else "N/A"
    )

    job = {
        "title": title,
        "company": company,
        "location": location
    }

    jobs.append(job)

print(jobs)

df = pd.DataFrame(jobs)

df.to_csv("jobs.csv", index=False)

print("jobs.csv saved successfully")