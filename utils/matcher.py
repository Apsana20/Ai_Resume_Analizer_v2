def calculate_match(resume_skills, job_skills):

    matched_skills = set(resume_skills) & set(job_skills)

    match_percentage = (len(matched_skills) / len(job_skills)) * 100

    missing_skills = set(job_skills) - set(resume_skills)

    return match_percentage, list(missing_skills)