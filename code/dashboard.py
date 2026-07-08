import streamlit as st
from database import JobDatabase

# MUST be first Streamlit call
st.set_page_config(
    page_title="RCIP Assistant",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("RCIP Assistant")
st.write("AI-powered job matching dashboard")

# -----------------------------
# Database
# -----------------------------
db = JobDatabase()

jobs = db.get_apply_jobs()

# -----------------------------
# Jobs Display
# -----------------------------
st.subheader("Recommended Jobs")

for job in jobs:

    title = job["title"]
    company = job["company"]
    location = job["location"]
    score = job["score"]
    recommendation = job["recommendation"]
    strengths = job["strengths"]
    gaps = job["gaps"]
    url = job["url"]

    with st.expander(f"{title} — Score: {score}"):

        st.write("Company:", company)
        st.write("Location:", location)

        st.write("Recommendation:", recommendation.upper())

        st.write("Strengths:")
        st.write(strengths)

        st.write("Missing:")
        st.write(gaps)

        st.link_button("Open Job Posting", url)

db.close()