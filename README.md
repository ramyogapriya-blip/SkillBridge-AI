# SkillBridge AI 🎓

SkillBridge AI is a student-focused career discovery platform that analyzes education, interests and current skills to recommend a career direction, identify skill gaps, and surface learning resources and sample internship opportunities.

## Features
- Career-path recommendation engine
- Skill-gap analysis
- Career readiness score
- Curated free learning resources
- Internship/opportunity matching demo
- Assessment activity dashboard
- SQLite persistence
- Flask REST endpoints
- Responsive UI
- Render-ready deployment configuration

## Run locally
```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Deploy on Render
Create a Web Service from this GitHub repository.

- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Root Directory: leave blank
- Plan: Free

No environment variables or API keys are required for the demo.

## Project structure
```text
SkillBridge-AI/
├── app.py
├── requirements.txt
├── Procfile
├── render.yaml
├── runtime.txt
├── .gitignore
├── README.md
├── templates/
│   ├── index.html
│   └── dashboard.html
└── static/
    ├── app.js
    └── style.css
```

## Note
The recommendation engine is intentionally self-contained so the project can run without paid AI APIs. For a production/SIH prototype, it can later be upgraded with a trained ML model, resume parsing, verified government-scheme data, and live internship APIs.
