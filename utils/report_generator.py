from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
        score,
        skills,
        missing_skills,
        courses,
        jobs):

    doc = SimpleDocTemplate("reports/report.pdf")
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("AI Resume Analysis Report", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"ATS Score: {score}%", styles['Heading2']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Extracted Skills", styles['Heading2']))
    elements.append(
        ListFlowable(
            [ListItem(Paragraph(skill, styles['BodyText'])) for skill in skills]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Missing Skills", styles['Heading2']))
    elements.append(
        ListFlowable(
            [ListItem(Paragraph(skill, styles['BodyText'])) for skill in missing_skills]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Recommended Courses", styles['Heading2']))
    elements.append(
        ListFlowable(
            [ListItem(Paragraph(course, styles['BodyText'])) for course in courses]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Recommended Jobs", styles['Heading2']))
    elements.append(
        ListFlowable(
            [ListItem(Paragraph(job, styles['BodyText'])) for job in jobs]
        )
    )

    doc.build(elements)