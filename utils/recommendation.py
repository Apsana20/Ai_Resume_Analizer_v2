def recommend_jobs(skills):

    jobs = []

    skills = [skill.lower() for skill in skills]

    if "python" in skills:
        jobs.append("Python Developer")

    if "sql" in skills:
        jobs.append("Data Analyst")

    if "javascript" in skills:
        jobs.append("Frontend Developer")

    if "java" in skills:
        jobs.append("Java Developer")

    if "machine learning" in skills:
        jobs.append("ML Engineer")

    return jobs
def recommend_courses(missing_skills):

    courses = []

    skills = [skill.lower() for skill in missing_skills]

    if "python" in skills:
        courses.append("Python for Everybody")

    if "sql" in skills:
        courses.append("SQL Bootcamp")

    if "javascript" in skills:
        courses.append("JavaScript Essentials")

    if "java" in skills:
        courses.append("Java Programming Masterclass")

    if "html" in skills:
        courses.append("HTML & CSS Complete Course")

    if "css" in skills:
        courses.append("CSS Flexbox and Grid")

    return courses
def improvement_suggestions(missing_skills):

    suggestions = []

    for skill in missing_skills:

        if skill.lower() == "machine learning":
            suggestions.append(
                "Learn Machine Learning fundamentals."
            )

        elif skill.lower() == "power bi":
            suggestions.append(
                "Practice Power BI dashboards."
            )

        elif skill.lower() == "sql":
            suggestions.append(
                "Improve SQL query skills."
            )

        elif skill.lower() == "excel":
            suggestions.append(
                "Learn Excel formulas and pivot tables."
            )

        else:
            suggestions.append(
                f"Improve your {skill} skills."
            )

    return suggestions