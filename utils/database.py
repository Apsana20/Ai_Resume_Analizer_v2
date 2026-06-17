import sqlite3
from datetime import datetime
def create_users_table():

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT UNIQUE,

        password TEXT

    )
    """)

    conn.commit()

    conn.close()

def create_reports_table():

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_email TEXT,

        score REAL,

        skills TEXT
        date TEXT
    )
    """)

    conn.commit()

    conn.close()
def save_report(user_email, score, skills):

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()
    date = datetime.now().strftime("%d-%m-%Y")

    cursor.execute(
        """
        INSERT INTO reports(user_email, score, skills,date)
        VALUES (?, ?, ?,?)
        """,
        (
            user_email,
            score,
            skills,
            date
        )
    )

    conn.commit()

    conn.close()

def get_reports(user_email):

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT score, skills
        FROM reports
        WHERE user_email = ?
        """,
        (user_email,)
    )

    reports = cursor.fetchall()

    conn.close()

    return reports

def get_statistics(user_email):

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*),
               MAX(score),
               AVG(score)
        FROM reports
        WHERE user_email = ?
        """,
        (user_email,)
    )

    stats = cursor.fetchone()

    conn.close()

    return stats

def get_analytics(user_email):

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*),
               MAX(score),
               MIN(score),
               AVG(score)
        FROM reports
        WHERE user_email = ?
        """,
        (user_email,)
    )

    analytics = cursor.fetchone()

    conn.close()

    return analytics

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
def get_all_users():

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, email
        FROM users
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users


def get_all_reports():

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
       SELECT user_email, score,date, id
       FROM reports
        """
    )

    reports = cursor.fetchall()

    conn.close()

    return reports
def count_users():

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def count_reports():

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM reports
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total

def search_users(keyword):

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, email
        FROM users
        WHERE name LIKE ?
        OR email LIKE ?
        """,
        (f"%{keyword}%", f"%{keyword}%")
    )

    users = cursor.fetchall()

    conn.close()

    return users

def delete_report(report_id):

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM reports
        WHERE id = ?
        """,
        (report_id,)
    )

    conn.commit()

    conn.close()
def delete_user(email):

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE email = ?
        """,
        (email,)
    )

    conn.commit()
    conn.close()
def get_user_reports(email):

    conn = sqlite3.connect("database/users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT score, skills, date
        FROM reports
        WHERE user_email = ?
        ORDER BY id DESC
        """,
        (email,)
    )

    reports = cursor.fetchall()

    conn.close()

    return reports
def get_statistics():

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(score) FROM reports")
    highest_score = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(score) FROM reports")
    lowest_score = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM reports")
    average_score = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports")
    total_reports = cursor.fetchone()[0]

    conn.close()

    if average_score:
        average_score = round(average_score, 2)
    else:
        average_score = 0

    return (
        highest_score,
        lowest_score,
        average_score,
        total_reports
    )

   


