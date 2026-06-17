from flask import Flask,render_template, request, redirect, session, send_file
import pandas as pd
from utils.database import (
    create_users_table,
    create_reports_table,
    save_report,
    get_reports,
    get_statistics,
    get_analytics,
    get_recent_reports,
    get_all_users,
    get_all_reports,
    count_users,
    count_reports,
    search_users,
    delete_report,
    delete_user,
    get_user_reports
)


from utils.auth import register_user, login_user
from utils.database import get_statistics
from utils.pdf_reader import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.matcher import calculate_match
from utils.recommendation import (
    recommend_jobs,
    recommend_courses,
    improvement_suggestions
)
from utils.charts import create_pie_chart, create_bar_chart
from utils.report_generator import generate_report
import os
import sqlite3

app = Flask(__name__)

app.secret_key = "apsana_secret_key"

create_users_table()
create_reports_table()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        success = login_user(email, password)

        if success:

            session['user'] = email

            return redirect('/dashboard')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

  

    if request.method == 'POST':
       

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        return "POST reached"
        print("Success =", success)
        if success == True:
             return redirect('/login')
        else:
             return str(success)
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    stats = get_statistics()

    recent_reports = get_recent_reports(
        session['user']
    )


    return render_template(
        'dashboard.html',
        total_reports=stats[0],
        highest_score=stats[1],
        average_score=round(stats[2],2)
        if stats[2] else 0,
        email=session['user'],
        recent_reports=recent_reports
    )

def get_recent_reports(user_email):

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT score, skills
        FROM reports
        WHERE user_email = ?
        ORDER BY id DESC
        LIMIT 5
        """,
        (user_email,)
    )

    reports = cursor.fetchall()

    conn.close()

    return reports




@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        file = request.files['resume']
        job_description = request.form.get('job_description')

        if file:

            filepath = os.path.join("uploads", file.filename)

            file.save(filepath)

            text = extract_text_from_pdf(filepath)

           

            resume_skills = extract_skills(text)

            if job_description:
                jd_skills = extract_skills(job_description)
            else:
                jd_skills = []


            matching_skills = list(
                set(resume_skills) & set(jd_skills)
            )

            missing_skills = list(
                set(jd_skills) - set(resume_skills)
            )
            if len(jd_skills) > 0:

               jd_match_score = round(
                    (len(matching_skills) / len(jd_skills)) * 100,
                    2
                )

            else:

                jd_match_score = 0
            job_skills = [
                "python",
                "sql",
                "html",
                "css",
                "javascript",
                "machine learning",
                "power bi",
                "excel"
            ]

            match_percentage, missing_skills = calculate_match(
                resume_skills,
                job_skills
            )

            recommended_jobs = recommend_jobs(resume_skills)

            recommended_courses = recommend_courses(missing_skills)
            suggestions = improvement_suggestions(missing_skills)
            pie_chart = create_pie_chart(match_percentage)

            bar_chart = create_bar_chart(resume_skills)

            generate_report(
                match_percentage,
                resume_skills,
                missing_skills,
                recommended_courses,
                recommended_jobs
            )

            save_report(
                session['user'],
                match_percentage,
                ", ".join(resume_skills)
            )

            return render_template(
                'result.html',
                skills=resume_skills,
                score=match_percentage,
                missing_skills=missing_skills,
                courses=recommended_courses,
                recommended_jobs=recommended_jobs,
                suggestions=suggestions,
                jd_match_score=jd_match_score,

                matching_skills=matching_skills,
                pie_chart=pie_chart.to_html(full_html=False),
                bar_chart=bar_chart.to_html(full_html=False)
            )

    return render_template('upload.html')




@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')
@app.route('/history')
def history():

    if 'user' not in session:
        return redirect('/login')

    reports = get_reports(session['user'])

    return render_template(
        'history.html',
        reports=reports
    )
@app.route('/download-report')
def download_report():

    return send_file(
        "reports/report.pdf",
        as_attachment=True
    )
@app.route('/export-users')
@app.route('/export-reports')
def export_reports():

    reports = get_all_reports()

    df = pd.DataFrame(
        reports,
        columns=[
            'User Email',
            'ATS Score',
            'Date',
            'ID'
        ]
    )

    df.to_excel(
        'reports.xlsx',
        index=False
    )

    return send_file(
        'reports.xlsx',
        as_attachment=True
    )

    df.to_excel(
        'reports.xlsx',
        index=False
    )

    return send_file(
        'reports.xlsx',
        as_attachment=True
    )   

    users = get_all_users()

    df = pd.DataFrame(
    users,
    columns=[
        'Name',
        'Email'
    ]
)
    df.to_excel(
        'reports.xlsx',
        index=False
    )

    return send_file(
        'reports.xlsx',
        as_attachment=True
    )

@app.route('/profile')
def profile():

    if 'user' not in session:
        return redirect('/login')

    stats = get_statistics()

    return render_template(
        'profile.html',
        email=session['user'],
        total_reports=stats[0],
        highest_score=stats[1],
        average_score=round(stats[2], 2)
        if stats[2] else 0
    )


@app.route('/analytics')
def analytics():

    if 'user' not in session:
        return redirect('/login')

    data = get_analytics(session['user'])

    return render_template(
        'analytics.html',
        total_reports=data[0],
        highest_score=data[1],
        lowest_score=data[2],
        average_score=round(data[3], 2)
        if data[3] else 0
    )
@app.route('/admin')
def admin():
    if session.get('user') != "apsanasa03@gmail.com":
        return "Access Denied"

    print(session.get('user'))

    search = request.args.get('search')

    if search:
        users = search_users(search)
    else:
        users = get_all_users()

        reports = get_all_reports()
        highest_score, lowest_score, average_score, total_reports = get_statistics()

        total_users = count_users()

        total_reports = count_reports()

        return render_template(
        'admin.html',
        users=users,
        reports=reports,
        highest_score=highest_score,
        lowest_score=lowest_score,
        average_score=average_score,
        total_users=total_users,
        total_reports=total_reports
    )
@app.route('/delete-report/<int:report_id>')
def remove_report(report_id):

    delete_report(report_id)

    return redirect('/admin')
@app.route('/delete-user/<email>')
def remove_user(email):

    delete_user(email)

    return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True)




