# My First Flask App

This is my first AI-generated web application, created as part of my Certificate in Low-Code, No-Code & AI-Assisted Application Development at CCT College Dublin.

## What it does

The application uses Python and Flask to display a simple webpage with three tasks.

It has two routes:
- `/` — displays the homepage and task list.
- `/about` — displays information about the application.

## Requirements

- Python 3
- Flask

## How to run it

Open Git Bash in the project folder and run:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Notes

This is a basic Flask application generated with assistance from ChatGPT. I reviewed the code and tested the homepage and About page locally.

The project uses a virtual environment, which is excluded from GitHub using `.gitignore`.