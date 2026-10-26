"""A small contact form for learning Flask routes, templates, and validation."""

from email_validator import EmailNotValidError, validate_email
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.get("/")
def index():
    return redirect(url_for("contact"))


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
        else:
            try:
                # Syntax only: no DNS queries or mailbox existence checks.
                validate_email(email, check_deliverability=False)
            except EmailNotValidError:
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
