"""A small contact form for learning Flask routes, templates, and validation."""

import re

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# A practical ASCII email format check for this lab; no network requests.
EMAIL = re.compile(
    r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}"
)


@app.route("/")
def home():
    return """
    <h1>My First Flask App</h1>
    <p>My first AI-generated web application.</p>
    <ul>
        <li>Learn Python</li>
        <li>Learn Flask</li>
        <li>Push my project to GitHub</li>
    </ul>
    <a href="/about">About this app</a>
    <p><a href="/contact">Contact us</a></p>
    """

@app.route("/about")
def about():
    return "<h1>About</h1><p>This is my first Flask app.</p>"


@app.route("/contact", methods=["GET", "POST"])
def contact():
    values = {"name": "", "email": "", "message": ""}
    errors = {}

    if request.method == "POST":
        # Keep the original values so an invalid form preserves all input.
        values = {field: request.form.get(field, "") for field in values}

        if not values["name"].strip():
            errors["name"] = "Please enter your name."
        elif len(values["name"]) > 100:
            errors["name"] = "Please use 100 characters or fewer."

        email = values["email"].strip()
        if not email:
            errors["email"] = "Please enter your email address."
        elif len(values["email"]) > 254:
            errors["email"] = "Please use 254 characters or fewer."
        elif not EMAIL.fullmatch(email) or len(email.partition("@")[0]) > 64:
            errors["email"] = "Please enter a valid email address, such as alex@example.com."

        if not values["message"].strip():
            errors["message"] = "Please enter a message."
        elif len(values["message"]) > 2000:
            errors["message"] = "Please use 2,000 characters or fewer."

        if not errors:
            # Do not save, log, email, or put submitted values in a session.
            return redirect(url_for("confirmation"), code=303)

    return render_template("contact.html", values=values, errors=errors), (400 if errors else 200)


@app.get("/contact/confirmation")
def confirmation():
    return render_template("confirmation.html")


if __name__ == "__main__":
    app.run()
