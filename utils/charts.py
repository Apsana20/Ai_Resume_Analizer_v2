import plotly.express as px


def create_pie_chart(match_percentage):

    values = [match_percentage, 100 - match_percentage]

    labels = ["Matched Skills", "Missing Skills"]

    fig = px.pie(
        values=values,
        names=labels,
        title="Resume Match Analysis"
    )

    return fig


def create_bar_chart(resume_skills):

    values = [1] * len(resume_skills)

    fig = px.bar(
        x=resume_skills,
        y=values,
        title="Skills Distribution"
    )

    return fig