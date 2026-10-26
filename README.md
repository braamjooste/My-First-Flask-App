# My First Flask App

This is my first AI-generated web application, created as part of my Certificate in Low-Code, No-Code & AI-Assisted Application Development at CCT College Dublin.

## What it does

The application uses Python and Flask to display a simple webpage with three tasks.

It has four routes:
- `/` — displays the homepage and task list.
- `/about` — displays information about the application.
- `/contact` — displays and validates the contact form.
- `/contact/confirmation` — displays confirmation after a valid submission.

## Requirements

- Python 3
- Flask

## How to run it

Open Git Bash in the project folder and run:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m flask --app app run --port 5055
```

Open `http://127.0.0.1:5055` in your browser.

## Notes

This is a basic Flask application generated with assistance from ChatGPT. I reviewed the code and tested the homepage and About page locally.

The project uses a virtual environment, which is excluded from GitHub using `.gitignore`.
## Project Idea – Simple Stock and Ordering App

If I had an evening instead of a quarter to build an application, I would create a simple stock and ordering system for a small business.

The idea would be to allow staff to select products from a predefined list, enter the quantities they need and generate an order. Products could be grouped into categories, making it easier to find what they need without having to type everything out each time.

I would start with a basic Flask application, keeping the interface simple and avoiding unnecessary features. The first version wouldn't need a complicated database or supplier integration. It could use a small sample product list and display the completed order on screen.

The aim would be to reduce repetitive work and make ordering quicker and more consistent. If the basic version worked well, I could expand it later to include stock levels, suppliers and pricing comparisons.


## Session 2 - Contact form

The contact form checks name, email and message on the server, returns HTTP 400
with errors and the original values when invalid, and redirects to a separate
confirmation when valid. It saves nothing, uses no sessions, logs no submitted
values, and sends no email. The email check uses Python's `re` module for ordinary
ASCII addresses; it does not perform DNS, mailbox or deliverability checks.
Only Flask is required in addition to the Python standard library.

The existing homepage and About page are retained. The contact form and confirmation
use a 1970s cream, orange, mustard, olive and chocolate colour scheme.

### Run in Git Bash on Windows

```bash
py -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m flask --app app run --port 5055
```

Open http://127.0.0.1:5055/contact. Port 5055 avoids the other local app previously
using port 5000. Press Ctrl+C to stop. If `py` is unavailable, use `python` for
the first command. Activate the virtual environment again when opening a new Git Bash terminal.

### Automated checks

```bash
python -m unittest discover -s tests -v
```

### Manual checks

1. Submit all fields empty: three errors, HTTP 400.
2. Submit spaces in name/message and a valid email: errors for name and message.
3. Submit Alex / notanemail / Hello: email error, with entered values preserved.
4. In DevTools remove `required` and repeat the empty submission: server errors
   must still appear. The form already uses `novalidate` to expose these errors.
5. Put `<script>alert(1)</script>` in Message and an invalid email: the script
   appears as text and does not execute. With a valid email, only confirmation appears.
6. Submit Alex / alex@example.com / Hello: separate confirmation, with no message
   stored or emailed. Refreshing confirmation should not repeat the POST.

The regex is a practical lab format check, not a complete implementation of every
unusual email syntax. It rejects missing addresses, missing dots, consecutive dots
in the local part and domain labels beginning or ending with hyphens.

### Coursework evidence - comparison findings recorded

- [Comparison write-up](docs/week02-tool-comparison.md)
- [Original Codex prompt and recovered output](experiments/week02/codex/README.md)
- [Supplied three-code comparison report](docs/week02-comparison-report.md)
- [Claude source evidence still needed](experiments/week02/claude/README.md)
- [Gemini source evidence still needed](experiments/week02/gemini/README.md)
- [Selected implementation test report](docs/week02-selected-tests.txt)
- [Recovered snapshot test report](docs/week02-snapshot-tests.txt)

The recovered experiment intentionally retains its old email-validator requirement
as evidence of the mismatch. The runnable application at the repository root does
not depend on it. The supplied review of ChatGPT, Claude and Gemini is recorded with
its scores and verification limits. The exact prompts for all three assistants are
saved. Original Claude/Gemini source outputs still need to be archived; their reported
results have not been independently rerun here. The Block B forum post is not yet done.
