from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("skillbridge.db")

COURSES = [
    {"title":"Python for Everybody", "skill":"Python", "level":"Beginner", "type":"Free", "url":"https://www.freecodecamp.org/learn/scientific-computing-with-python/"},
    {"title":"Java Programming", "skill":"Java", "level":"Beginner", "type":"Free", "url":"https://www.freecodecamp.org/learn/java/"},
    {"title":"SQL Fundamentals", "skill":"SQL", "level":"Beginner", "type":"Free", "url":"https://www.w3schools.com/sql/"},
    {"title":"Web Development", "skill":"HTML/CSS/JavaScript", "level":"Beginner", "type":"Free", "url":"https://www.freecodecamp.org/learn/"},
    {"title":"Data Structures & Algorithms", "skill":"DSA", "level":"Intermediate", "type":"Free", "url":"https://www.geeksforgeeks.org/data-structures/"},
    {"title":"Machine Learning", "skill":"Machine Learning", "level":"Intermediate", "type":"Free", "url":"https://www.kaggle.com/learn/intro-to-machine-learning"},
    {"title":"Git & GitHub", "skill":"Git/GitHub", "level":"Beginner", "type":"Free", "url":"https://skills.github.com/"},
    {"title":"Communication Skills", "skill":"Communication", "level":"Beginner", "type":"Free", "url":"https://www.coursera.org/articles/communication-skills"},
]

JOBS = [
    {"title":"Python Intern", "skills":"Python, SQL", "location":"Remote", "level":"Beginner"},
    {"title":"Frontend Intern", "skills":"HTML/CSS/JavaScript", "location":"Remote", "level":"Beginner"},
    {"title":"Java Developer Intern", "skills":"Java, SQL", "location":"India", "level":"Beginner"},
    {"title":"Data Analyst Intern", "skills":"Python, SQL, Excel", "location":"India", "level":"Intermediate"},
    {"title":"ML Intern", "skills":"Python, Machine Learning", "location":"Remote", "level":"Intermediate"},
    {"title":"Support & Communication Intern", "skills":"Communication, English", "location":"India", "level":"Beginner"},
]

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, education TEXT, interests TEXT, skills TEXT,
            goal TEXT, score INTEGER, recommendation TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

def skill_score(skills):
    skills = {s.strip().lower() for s in skills.split(",") if s.strip()}
    groups = {
        "software": {"python","java","c","c++","javascript","html","css","sql","git/github","dsa"},
        "data": {"python","sql","excel","machine learning"},
        "communication": {"communication","english","public speaking"},
    }
    result = {}
    for group, wanted in groups.items():
        result[group] = len(skills & wanted)
    return result

def recommend(education, interests, skills, goal):
    raw = (interests + "," + skills + "," + goal).lower()
    scores = {
        "Software Development": sum(k in raw for k in ["software","coding","python","java","web","developer","app"]),
        "Data & AI": sum(k in raw for k in ["data","ai","machine learning","analytics","ml"]),
        "Cybersecurity": sum(k in raw for k in ["cyber","security","network","ethical hacking"]),
        "Cloud & DevOps": sum(k in raw for k in ["cloud","devops","aws","deployment"]),
        "Communication & Business": sum(k in raw for k in ["communication","business","management","marketing"]),
    }
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        best = "Software Development"
    skill_gap = {
        "Software Development": ["Python/Java", "DSA", "Git/GitHub", "Web Development"],
        "Data & AI": ["Python", "SQL", "Statistics", "Machine Learning"],
        "Cybersecurity": ["Networking", "Linux", "Python", "Security Fundamentals"],
        "Cloud & DevOps": ["Linux", "Git/GitHub", "Docker", "Cloud Fundamentals"],
        "Communication & Business": ["Communication", "Presentation", "Excel", "Business Fundamentals"],
    }[best]
    matched = skill_score(skills)
    readiness = min(95, 35 + sum(matched.values()) * 12 + (10 if education else 0))
    return best, skill_gap, readiness

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/assessment", methods=["POST"])
def assessment():
    data = request.get_json(silent=True) or request.form
    name = str(data.get("name","Student")).strip() or "Student"
    education = str(data.get("education","")).strip()
    interests = str(data.get("interests","")).strip()
    skills = str(data.get("skills","")).strip()
    goal = str(data.get("goal","")).strip()
    career, skill_gap, readiness = recommend(education, interests, skills, goal)
    recommendation = f"{career} is your strongest starting path. Focus next on: {', '.join(skill_gap)}."
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO assessments(name,education,interests,skills,goal,score,recommendation) VALUES(?,?,?,?,?,?,?)",
                    (name,education,interests,skills,goal,readiness,recommendation))
    return jsonify({
        "name": name, "career": career, "skill_gap": skill_gap,
        "readiness": readiness, "recommendation": recommendation
    })

@app.route("/courses")
def courses():
    return jsonify(COURSES)

@app.route("/jobs")
def jobs():
    return jsonify(JOBS)

@app.route("/dashboard")
def dashboard():
    with sqlite3.connect(DB_PATH) as con:
        rows = con.execute("SELECT name, score, recommendation, created_at FROM assessments ORDER BY id DESC LIMIT 10").fetchall()
    return render_template("dashboard.html", rows=rows)

@app.route("/health")
def health():
    return {"status":"ok", "service":"SkillBridge AI"}

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
