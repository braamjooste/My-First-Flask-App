const express = require("express");

const app = express();
const PORT = process.env.PORT || 3000;

// Parse standard HTML form submissions
app.use(express.urlencoded({ extended: false }));

// ---------- Validation (server side) ----------

// Practical email format check: something@something.tld, no spaces,
// a single @, and a dot-separated domain with a 2+ letter TLD.
const EMAIL_PATTERN = /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)*\.[A-Za-z]{2,}$/;

function validateContact({ name, email, message }) {
  const errors = [];
  const missing = [];

  if (!name) missing.push("name");
  if (!email) missing.push("email");
  if (!message) missing.push("message");

  if (missing.length) {
    errors.push(`Missing required ${missing.length > 1 ? "fields" : "field"}: ${joinList(missing)}.`);
  }

  if (email && !EMAIL_PATTERN.test(email)) {
    errors.push("Email address isn’t in a valid format, for example name@example.com.");
  }

  return { errors, missing, emailInvalid: Boolean(email) && !EMAIL_PATTERN.test(email) };
}

function joinList(items) {
  if (items.length === 1) return items[0];
  return items.slice(0, -1).join(", ") + " and " + items[items.length - 1];
}

// ---------- HTML rendering ----------

function escapeHtml(value = "") {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function page(title, body) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --ink: #1F2A44;
      --muted: #5B6680;
      --paper: #F6F8FB;
      --surface: #FFFFFF;
      --line: #C9D1DE;
      --accent: #2F5BEA;
      --error: #B42318;
      --error-bg: #FEF3F2;
      --ok: #13795B;
      --ok-bg: #ECFDF3;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: "Atkinson Hyperlegible", system-ui, -apple-system, "Segoe UI", sans-serif;
      font-size: 1.0625rem;
      line-height: 1.5;
      color: var(--ink);
      background: var(--paper);
      display: grid;
      place-items: start center;
      padding: 4rem 1.25rem;
    }
    main {
      width: 100%;
      max-width: 34rem;
      background: var(--surface);
      border: 1px solid var(--line);
      border-top: 6px solid var(--accent);
      border-radius: 4px;
      padding: 2.25rem 2rem 2rem;
    }
    h1 { font-size: 1.875rem; line-height: 1.2; margin: 0 0 .5rem; }
    .intro { color: var(--muted); margin: 0 0 1.75rem; }
    .field { margin-bottom: 1.25rem; }
    label { display: block; font-weight: 700; margin-bottom: .375rem; }
    input, textarea {
      width: 100%;
      font: inherit;
      color: inherit;
      padding: .7rem .8rem;
      border: 1.5px solid var(--line);
      border-radius: 4px;
      background: var(--surface);
    }
    textarea { min-height: 9rem; resize: vertical; }
    input:focus, textarea:focus, button:focus-visible {
      outline: 3px solid color-mix(in srgb, var(--accent) 35%, transparent);
      outline-offset: 1px;
      border-color: var(--accent);
    }
    .invalid { border-color: var(--error); }
    .hint { color: var(--error); font-size: .9375rem; margin-top: .3rem; }
    button {
      font: inherit;
      font-weight: 700;
      color: #fff;
      background: var(--accent);
      border: 0;
      border-radius: 4px;
      padding: .75rem 1.5rem;
      cursor: pointer;
    }
    button:hover { background: #2349C7; }
    .alert {
      border-left: 4px solid var(--error);
      background: var(--error-bg);
      color: var(--error);
      padding: .875rem 1rem;
      margin-bottom: 1.5rem;
      border-radius: 0 4px 4px 0;
    }
    .alert ul { margin: .25rem 0 0; padding-left: 1.2rem; }
    .alert p { margin: 0; font-weight: 700; }
    .success {
      border-left: 4px solid var(--ok);
      background: var(--ok-bg);
      color: var(--ok);
      padding: 1rem;
      border-radius: 0 4px 4px 0;
      margin-bottom: 1.5rem;
    }
    .success p { margin: 0; }
    a { color: var(--accent); }
    @media (max-width: 480px) {
      body { padding: 1.5rem .75rem; }
      main { padding: 1.75rem 1.25rem; }
    }
  </style>
</head>
<body>
  <main>
${body}
  </main>
</body>
</html>`;
}

function renderForm(values = {}, result = null) {
  const errors = result ? result.errors : [];
  const missing = result ? result.missing : [];
  const isBad = (field) =>
    missing.includes(field) || (field === "email" && result && result.emailInvalid);

  const fieldHint = (field) => {
    if (missing.includes(field)) return `<div class="hint" id="${field}-hint">Enter your ${field}.</div>`;
    if (field === "email" && result && result.emailInvalid)
      return `<div class="hint" id="email-hint">Use a format like name@example.com.</div>`;
    return "";
  };
  const describedBy = (field) => (isBad(field) ? ` aria-invalid="true" aria-describedby="${field}-hint"` : "");

  const alert = errors.length
    ? `<div class="alert" role="alert">
      <p>Your message wasn’t sent.</p>
      <ul>${errors.map((e) => `<li>${escapeHtml(e)}</li>`).join("")}</ul>
    </div>`
    : "";

  return page(
    "Contact us",
    `    <h1>Contact us</h1>
    <p class="intro">Send us a message and we’ll get back to you by email.</p>
    ${alert}
    <!-- novalidate: all validation is done on the server -->
    <form method="post" action="/contact" novalidate>
      <div class="field">
        <label for="name">Name</label>
        <input id="name" name="name" type="text" autocomplete="name"
          value="${escapeHtml(values.name)}" class="${isBad("name") ? "invalid" : ""}"${describedBy("name")}>
        ${fieldHint("name")}
      </div>
      <div class="field">
        <label for="email">Email</label>
        <input id="email" name="email" type="email" autocomplete="email"
          value="${escapeHtml(values.email)}" class="${isBad("email") ? "invalid" : ""}"${describedBy("email")}>
        ${fieldHint("email")}
      </div>
      <div class="field">
        <label for="message">Message</label>
        <textarea id="message" name="message" class="${isBad("message") ? "invalid" : ""}"${describedBy("message")}>${escapeHtml(values.message)}</textarea>
        ${fieldHint("message")}
      </div>
      <button type="submit">Send message</button>
    </form>`
  );
}

function renderSuccess(name) {
  return page(
    "Message sent",
    `    <h1>Message sent</h1>
    <div class="success" role="status">
      <p>Thanks, ${escapeHtml(name)}. We’ve received your message and will reply by email.</p>
    </div>
    <p><a href="/contact">Send another message</a></p>`
  );
}

// ---------- Routes ----------

app.get("/", (req, res) => res.redirect("/contact"));

app.get("/contact", (req, res) => {
  res.send(renderForm());
});

app.post("/contact", (req, res) => {
  // Trim so whitespace-only input counts as empty
  const values = {
    name: (req.body.name || "").trim(),
    email: (req.body.email || "").trim(),
    message: (req.body.message || "").trim(),
  };

  const result = validateContact(values);

  if (result.errors.length) {
    return res.status(400).send(renderForm(values, result));
  }

  // No storage for now — just confirm.
  res.send(renderSuccess(values.name));
});

app.listen(PORT, () => {
  console.log(`Contact form running at http://localhost:${PORT}/contact`);
});