# RCIP Job Assistant

RCIP Job Assistant is a Python project I created to help search and analyze Canadian job postings.

The main purpose of the project is to collect jobs from Job Bank, store them in a database, and use AI and a scoring system to help identify jobs that may be a good match for a candidate.

I originally started the project to make it easier to search through jobs related to my career goals instead of reviewing every posting manually.

## Live Demo

🌐 **[Open RCIP Job Assistant](https://rcip-assistant-unvyu8gnae9ztxzxvlhxqd.streamlit.app/)**

The live demo includes a dashboard with sample analyzed jobs and an AI-powered Analyze Job page where a job description can be entered for real-time analysis.

## Features

The project currently includes:

- Job scraping from Canada Job Bank
- SQLite database storage
- Duplicate job prevention
- AI job classification
- Resume/job skill matching
- Job match scoring
- Apply / Maybe / Skip recommendations
- IT, Sales, and Hybrid job classification
- Streamlit dashboard
- Job filtering
- Direct links to original job postings
- Manual job description analysis

## How the Project Works

The basic flow of the program is:

```text
Job Bank
   |
   v
Job Scraper
   |
   v
SQLite Database
   |
   v
AI Job Analysis
   |
   v
Scoring
   |
   v
Apply / Maybe / Skip
   |
   v
Streamlit Dashboard
```

The scraper collects job postings and saves them to the SQLite database.

The AI analysis looks at the job description and compares important skills and requirements against the candidate profile.

The scoring code then calculates a match score and gives the job one of three recommendations:

- **Apply** - strong match
- **Maybe** - some matching skills but also some gaps
- **Skip** - lower match

## Technologies Used

- Python
- SQLite
- OpenAI API
- Streamlit
- BeautifulSoup
- Requests
- Git / GitHub

## Project Files

```text
collector.py
```

Collects job postings from Canada Job Bank and stores them in the database.

```text
database.py
```

Handles the SQLite database, including inserting, reading, and updating job records.

```text
ai_ranker.py
```

Connects to the OpenAI API and performs AI-based analysis of job descriptions.

```text
ai_pipeline.py
```

Connects the database, AI analysis, and scoring parts of the program.

```text
scoring.py
```

Calculates the job match score and helps determine whether the recommendation should be Apply, Maybe, or Skip.

```text
dashboard.py
```

Runs the main Streamlit dashboard.

```text
pages/2_Analyze_job.py
```

Allows a user to paste a job description into the application and analyze it manually.

## Job Categories

The program currently classifies jobs into three main categories:

- IT
- Sales
- Hybrid

The dashboard allows the user to filter jobs by category and recommendation.

## Duplicate Job Handling

Job Bank URLs can contain temporary session information.

The program extracts the Job Bank posting number from the URL and uses it as the job ID.

For example:

```text
https://www.jobbank.gc.ca/jobsearch/jobposting/50025107
```

uses:

```text
50025107
```

as the ID.

Since the ID is stored as the primary key in SQLite, the same Job Bank posting is not added multiple times when the scraper is run again.

## Installation

Clone the repository and move into the project folder.

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

The project uses the OpenAI API.

Create a `.env` file and add:

```text
OPENAI_API_KEY=your_api_key_here
```

The `.env` file should not be uploaded to GitHub.

## Running the Job Collector

Run:

```bash
python collector.py
```

The collector searches Job Bank and saves the jobs into the SQLite database.

## Running the AI Analysis

Run:

```bash
python ai_pipeline.py
```

The pipeline reads jobs from the database, analyzes them, calculates their scores, and saves the results.

## Running the Dashboard

Run:

```bash
streamlit run dashboard.py
```

The dashboard displays the analyzed jobs and allows them to be filtered by job category and recommendation.

## Analyze Job Page

The Streamlit application also contains an Analyze Job page.

A full job description can be pasted into the page and the program will display:

- Job category
- Classification confidence
- Match score
- Recommendation
- Matching strengths
- Skill gaps

This allows jobs from other websites to be analyzed without adding them to the Job Bank scraper.

## Screenshots

### Main Dashboard

<img width="1920" height="1080" alt="Dashboard 1" src="https://github.com/user-attachments/assets/87b76933-de26-472b-a5f2-5cd044c96e04" />
<img width="1920" height="1080" alt="Dashboard 2" src="https://github.com/user-attachments/assets/ef7aaa08-32f4-496a-87fd-ace33920d102" />


### Job Analysis

<img width="1920" height="1080" alt="Dashboard 3" src="https://github.com/user-attachments/assets/4588b8a4-252d-4572-ac61-fa19b3b869f9" />

<img width="1920" height="1080" alt="Dashboard 4" src="https://github.com/user-attachments/assets/652f2880-34d1-447d-851e-12ccf278b4b8" />


## What I Learned

This project gave me practical experience connecting several different parts of a Python application.

Some of the main things I practiced were:

- Web scraping with BeautifulSoup
- Working with APIs
- Using SQLite with Python
- Reading and writing database records
- Using AI output inside a Python program
- Separating code into different modules
- Creating a basic scoring system
- Building a user interface with Streamlit
- Debugging data and database problems
- Preventing duplicate database records
- Using Git and GitHub during development

One of the main challenges was connecting the scraper, database, AI analysis, scoring system, and dashboard so that data could move correctly through each part of the program.

## Current Limitations

This is a student portfolio project and there are still areas that could be improved.

For example:

- The scraper currently focuses on Canada Job Bank.
- Job classification is limited to IT, Sales, and Hybrid.
- AI analysis requires an OpenAI API key.
- Job websites can change their HTML structure, which may require the scraper to be updated.
- The matching system could be expanded to support more resume profiles and job categories.

These would be possible improvements for a future version.

## Project Status

**Version 1.0 - Complete**

The main goals for the first version have been completed:

- Collect jobs
- Store jobs in SQLite
- Prevent duplicate postings
- Analyze jobs using AI
- Calculate job match scores
- Generate recommendations
- Display results using Streamlit
- Filter job results
- Analyze manually entered job descriptions

This project is now being used as part of my programming portfolio.
