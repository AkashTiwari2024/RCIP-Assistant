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


def calculate_total_score(analysis):

    matched = analysis.get("required_skills", {}).get("matched", [])
    missing = analysis.get("required_skills", {}).get("missing", [])

    # Base score from match ratio
    total_skills = len(matched) + len(missing)

    if total_skills == 0:
        return {"score": 0}

    match_ratio = len(matched) / total_skills

    # ENTRY-LEVEL BOOST SYSTEM
    score = 30  # baseline (IMPORTANT FIX)

    # skill contribution
    score += match_ratio * 50  # up to +50

    # small penalty for missing skills
    score -= len(missing) * 2

    # clamp
    score = max(0, min(100, score))

    return {"score": int(score)}