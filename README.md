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
## Project Idea – Simple Stock and Ordering App

If I had an evening instead of a quarter to build an application, I would create a simple stock and ordering system for a small business.

The idea would be to allow staff to select products from a predefined list, enter the quantities they need and generate an order. Products could be grouped into categories, making it easier to find what they need without having to type everything out each time.

I would start with a basic Flask application, keeping the interface simple and avoiding unnecessary features. The first version wouldn't need a complicated database or supplier integration. It could use a small sample product list and display the completed order on screen.

The aim would be to reduce repetitive work and make ordering quicker and more consistent. If the basic version worked well, I could expand it later to include stock levels, suppliers and pricing comparisons.