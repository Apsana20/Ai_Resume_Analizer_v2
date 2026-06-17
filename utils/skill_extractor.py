def extract_skills(text):

    skills_database = [
        "python",
        "sql",
        "html",
        "css",
        "javascript",
        "java",
        "c++",
        "machine learning",
        "power bi",
        "excel",
        "pandas",
        "numpy"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_database:
        if skill in text:
            found_skills.append(skill)

    return found_skills