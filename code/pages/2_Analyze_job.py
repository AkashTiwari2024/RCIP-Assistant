import streamlit as st

st.set_page_config(page_title="Analyze Job")

st.title("📝 Analyze a Job Description")

st.write(
    "Paste a complete job posting below and let RCIP Assistant "
    "evaluate how well it matches your resume."
)

job_description = st.text_area(
    "Job Description",
    height=350,
    placeholder="Paste the complete job posting here..."
)

analyze = st.button("Analyze Job")

if analyze:

    if not job_description.strip():

        st.warning("Please paste a job description.")

    else:

        st.success("Job description received!")