import streamlit as st
from ai_pipeline import analyze_job_description

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

       with st.spinner("Analyzing job..."):

        result = analyze_job_description(
        description=job_description
    )
        analysis = result["analysis"]
classification = result["classification"]

score = analysis.get("score", "N/A")
strengths = analysis.get("strengths", [])
gaps = analysis.get("gaps", [])

st.success("Analysis complete!")

st.subheader("Classification")

st.write("Category:", classification["category"])
st.write("Confidence:", classification["confidence"])

st.subheader("Match Score")

st.metric("Score", score)

recommendation = (
    "Apply" if score != "N/A" and score >= 70
    else "Maybe" if score != "N/A" and score >= 45
    else "Skip"
)

st.write("Recommendation:", recommendation)

st.subheader("Strengths")

for item in strengths:
    st.write(f"✅ {item}")

st.subheader("Skill Gaps")

for item in gaps:
    st.write(f"❌ {item}")