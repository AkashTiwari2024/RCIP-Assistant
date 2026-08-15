import streamlit as st

from ai_pipeline import analyze_job_description
from scoring import calculate_total_score


st.set_page_config(
    page_title="Analyze Job"
)


st.title("Analyze a Job Description")

st.write(
    "Paste a complete job posting below and let RCIP Assistant "
    "evaluate how well it matches your profile."
)


job_description = st.text_area(
    "Job Description",
    height=350,
    placeholder="Paste the complete job posting here..."
)


analyze = st.button(
    "Analyze Job"
)


if analyze:

    if not job_description.strip():

        st.warning(
            "Please paste a job description."
        )

    else:

        with st.spinner(
            "Analyzing job..."
        ):

            result = analyze_job_description(
                description=job_description
            )

            analysis = result["analysis"]

            classification = result[
                "classification"
            ]

            score_data = calculate_total_score(
                analysis
            )

            score = score_data["score"]

            strengths = analysis.get(
                "strengths",
                []
            )

            gaps = analysis.get(
                "gaps",
                []
            )


        # -----------------------------
        # Recommendation
        # -----------------------------

        if score >= 70:

            recommendation = "Apply"

        elif score >= 45:

            recommendation = "Maybe"

        else:

            recommendation = "Skip"


        # -----------------------------
        # Results
        # -----------------------------

        st.success(
            "Analysis complete!"
        )


        st.subheader(
            "Job Classification"
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Category",
            classification["category"].upper()
        )

        col2.metric(
            "Confidence",
            f"{classification['confidence']:.0%}"
        )


        st.subheader(
            "Match Score"
        )

        score_col1, score_col2 = st.columns(2)

        score_col1.metric(
            "Score",
            f"{score}/100"
        )

        score_col2.metric(
            "Recommendation",
            recommendation
        )


        st.subheader(
            "Strengths"
        )

        if strengths:

            for item in strengths:

                st.write(
                    f"✅ {item}"
                )

        else:

            st.write(
                "No major strengths identified."
            )


        st.subheader(
            "Skill Gaps"
        )

        if gaps:

            for item in gaps:

                st.write(
                    f"⚠️ {item}"
                )

        else:

            st.write(
                "No major skill gaps identified."
            )