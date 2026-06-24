def calculate_skill_score(data):
    skills = data.get("required_skills", {})

    required = skills.get("job_skills", [])
    matched = skills.get("matched", [])

    if not required:
        return 0

    return round((len(matched) / len(required)) * 40)


def calculate_experience_score(data):
    experience = data.get("experience", {})

    match = experience.get("match", "").lower()

    if "strong" in match:
        return 25

    if "partial" in match:
        return 15

    if "some" in match:
        return 10

    return 5


def calculate_responsibility_score(data):

    responsibilities = data.get("responsibilities", {})

    required = (
        responsibilities.get("matched", [])
        +
        responsibilities.get("missing", [])
    )

    matched = responsibilities.get("matched", [])

    if not required:
        return 0

    return round((len(matched) / len(required)) * 20)


def calculate_education_score(data):

    education = data.get("education", {})

    matched = education.get("matched", [])

    if len(matched) > 0:
        return 10

    return 0


def calculate_total_score(data):

    skill = calculate_skill_score(data)
    experience = calculate_experience_score(data)
    responsibility = calculate_responsibility_score(data)
    education = calculate_education_score(data)

    total = (
        skill +
        experience +
        responsibility +
        education
    )

    return {
        "score": total,
        "skill_score": skill,
        "experience_score": experience,
        "responsibility_score": responsibility,
        "education_score": education
    }