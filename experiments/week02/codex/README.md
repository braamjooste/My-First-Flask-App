# Codex experiment evidence

`prompt.txt` contains the original contact-form request copied verbatim from the
conversation. It did not include the lab's Flask-and-standard-library-only rule.

`snapshot-before-lab-correction/` is the runnable project recovered on 26 October
2026, before removing the email-validator dependency. It includes later UI changes
and tests. It is an iterated snapshot, not the unmodified first assistant answer.
Its original requirements file is kept so the dependency mismatch remains visible.

The conversation records a 404 investigation and a change to port 5055 because
port 5000 served a different Flask application. This does not establish whether the
first generated answer ran unmodified. No first-time-success claim is made.

The selected, corrected implementation is at the repository root. See
`docs/week02-tool-comparison.md` for the assessment and remaining work.
