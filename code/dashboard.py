import json
import streamlit as st
from database import JobDatabase
from demo_data import load_demo_jobs




# MUST be first Streamlit call
st.set_page_config(
    page_title="RCIP Assistant",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------

st.title("RCIP Assistant")

st.write(
    "AI-powered job matching dashboard"
)


# -----------------------------
# Database
# -----------------------------

db = JobDatabase()

jobs = db.get_dashboard_jobs()
load_demo_jobs(db)


# -----------------------------
# Summary
# -----------------------------

total_jobs = len(jobs)

apply_count = sum(
    1
    for job in jobs
    if job["recommendation"] == "apply"
)

maybe_count = sum(
    1
    for job in jobs
    if job["recommendation"] == "maybe"
)

skip_count = sum(
    1
    for job in jobs
    if job["recommendation"] == "skip"
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Analyzed Jobs",
    total_jobs
)

col2.metric(
    "Apply",
    apply_count
)

col3.metric(
    "Maybe",
    maybe_count
)

col4.metric(
    "Skip",
    skip_count
)


# -----------------------------
# Filters
# -----------------------------

st.subheader("Filters")


filter_col1, filter_col2 = st.columns(2)


with filter_col1:

    category_filter = st.selectbox(
        "Job Category",
        [
            "All",
            "IT",
            "Sales",
            "Hybrid"
        ]
    )


with filter_col2:

    recommendation_filter = st.selectbox(
        "Recommendation",
        [
            "All",
            "Apply",
            "Maybe",
            "Skip"
        ]
    )


# -----------------------------
# Apply Filters
# -----------------------------

filtered_jobs = []


for job in jobs:

    category_match = (
        category_filter == "All"
        or job["category"] == category_filter.lower()
    )

    recommendation_match = (
        recommendation_filter == "All"
        or job["recommendation"]
        == recommendation_filter.lower()
    )

    if category_match and recommendation_match:

        filtered_jobs.append(job)


# -----------------------------
# Jobs Display
# -----------------------------

st.subheader(
    f"Recommended Jobs ({len(filtered_jobs)})"
)


if not filtered_jobs:

    st.info(
        "No jobs match the selected filters."
    )


for job in filtered_jobs:

    title = job["title"]
    company = job["company"]
    location = job["location"]
    score = job["score"]
    recommendation = job["recommendation"]
    category = job["category"]
    confidence = job["confidence"]
    url = job["url"]


    # Convert JSON strings back into lists
    try:
        strengths = json.loads(
            job["strengths"]
        ) if job["strengths"] else []

    except (json.JSONDecodeError, TypeError):

        strengths = []


    try:
        gaps = json.loads(
            job["gaps"]
        ) if job["gaps"] else []

    except (json.JSONDecodeError, TypeError):

        gaps = []


    with st.expander(
        f"{title} — Score: {score}"
    ):

        st.write(
            "**Company:**",
            company
        )

        st.write(
            "**Location:**",
            location
        )

        st.write(
            "**Category:**",
            category.upper()
            if category
            else "UNKNOWN"
        )

        st.write(
            "**Recommendation:**",
            recommendation.upper()
            if recommendation
            else "N/A"
        )

        if confidence is not None:

            st.write(
                "**Classification Confidence:**",
                f"{confidence:.0%}"
            )


        st.write("**Strengths:**")

        if strengths:

            for strength in strengths:
                st.write(
                    f"✅ {strength}"
                )

        else:
            st.write(
                "No strengths recorded."
            )


        st.write("**Skill Gaps:**")

        if gaps:

            for gap in gaps:
                st.write(
                    f"⚠️ {gap}"
                )

        else:
            st.write(
                "No major gaps recorded."
            )


        if url:

            st.link_button(
                "Open Job Posting",
                url
            )


db.close()