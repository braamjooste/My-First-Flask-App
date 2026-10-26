# Flask contact form

A beginner lab with server-side validation and a separate confirmation page.
Submitted values are never saved, logged, emailed, or stored in a session.

## Run in Windows PowerShell (Python 3.10 or newer)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run
```

Open http://127.0.0.1:5000/contact. Press Ctrl+C to stop the server.
If `py` is unavailable, use `python -m venv .venv` for the first command.

## Validation

POST /contact checks all three fields on the server. Names and messages must
contain non-whitespace characters. Email validation checks syntax only, with
deliverability checks disabled. Invalid forms return HTTP 400, show field errors,
and preserve the original input. Jinja escapes input when displaying it.
Valid forms redirect with HTTP 303 to /contact/confirmation without storing values.
The form uses novalidate so the browser lets you test the server's errors directly.
Names have a 100-character limit, emails 254, and messages 2,000.

## Check

Submit an empty form, spaces in each field, an invalid email with other fields
filled, and then Alex / alex@example.com / Hello! Only the last should confirm.
On errors, check that all entered values remain visible. Refresh the confirmation
to verify that it does not repeat the POST.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
