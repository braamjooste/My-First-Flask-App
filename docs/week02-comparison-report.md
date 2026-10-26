This comparison assessed three supplied contact-form implementations against one common specification. It evaluated the code, rather than the assistants generally. ChatGPT’s submission was explicitly labelled **“Current revised application”**; Claude’s and Gemini’s version histories were unknown. The applications were not rewritten.

**Scope and prompt influence.** The required outcome was a beginner-friendly Flask application using only Flask and Python’s standard library: a `/contact` form with name, email and message; authoritative server validation; HTTP 400 responses with clear errors and preserved input; a separate confirmation page; and no submitted-value storage, logging, email delivery or external services.

The original generation prompts were not supplied, so their precise influence cannot be established. The outputs show different interpretations or scopes: ChatGPT supplied a Flask project, Claude supplied an Express/Node application, and Gemini supplied a browser interface with simulated backend behaviour. These differences could reflect different prompts, conversation history, revisions or generation choices. They do not prove which explanation applies or that one assistant is generally better. ChatGPT’s known revision status also prevents treating this as a controlled comparison of equivalent first attempts.

| Criterion, scored 1–5 | ChatGPT, revised | Claude, version unknown | Gemini, version unknown |
|---|---|---|---|
| Correctness | **5:** Executed Flask checks confirmed validation, HTTP 400 errors, preserved values and confirmation through a 303 redirect. | **3:** Isolated handlers implement the main flow, but accept some malformed emails and return success directly from POST. Real Express execution was unverified. | **1:** No real backend, POST endpoint or HTTP error responses; simulated status values exist only in JavaScript objects. |
| Code quality | **4:** Clear separation of Python, templates and CSS. Dense email expression and unrelated home/about routes add complexity. | **3:** Readable helper names and structure, but large HTML/CSS strings share the server file; email validation is evaluated twice unnecessarily. | **2:** Reasonably named functions, but simulated networking, loading states, icon updates and class manipulation add complexity. Comments misidentify browser validation as server validation. |
| Completeness | **5:** Supplies application, dependency declaration, form template, confirmation template and stylesheet. | **2:** Substantial Express implementation, but no dependency manifest or Flask implementation; exact preservation and refresh behaviour are incomplete. | **1:** Supplies an interface and simulation, without the required Flask backend, real error responses or separate confirmation page. |
| Security | **5:** Direct POST validation, safely escaped output, debug off, and no prohibited submitted-value handling or external services found. | **3:** Server validation and explicit escaping are strengths, but email validation has gaps and external fonts violate the restrictions. | **2:** Browser-only validation is bypassable and external scripts/fonts violate the restrictions. No demonstrated user-input-to-HTML injection path was found. |

**Verification limits.** ChatGPT’s JSON arrays were joined using newline characters before execution. Its five reconstructed files were checked against the supplied arrays. Python 3.12.14 and Flask 3.1.3 were used; 17 Flask test-client cases ran with no expected-status failures. Claude’s JavaScript passed a syntax check, and its original handlers were exercised with stand-in request/response objects. Express was unavailable and its download failed, so actual startup and HTTP integration were not verified. Gemini’s original simulated validation function was executed separately; this did not constitute a backend test.

Live browser navigation to the local server was blocked by the environment. Chrome therefore rendered actual Flask test-client HTML with the supplied CSS offline. Full browser-to-server interaction was not verified. These environment restrictions were not treated as application defects.

| Shared requirement or test | ChatGPT | Claude | Gemini |
|---|---|---|---|
| Flask and standard library only | Pass, inspection | Fail: Express/Node | Fail: no Flask; external libraries |
| Real `/contact` form route | Pass, executed | Present in inspected route registrations; real HTTP unverified | Fail: displaying a route label does not implement a route |
| Completely empty submission | Executed HTTP 400 with errors | Handler assigned 400 in isolation | Helper detected errors, but no real HTTP 400 |
| Whitespace-only name/message | Rejected, executed | Rejected by isolated handler | Rejected by browser helper only |
| Missing/whitespace-only email | Rejected, executed | Rejected by isolated handler | Rejected by browser helper only |
| `notanemail` and `alex@@example.com` | Rejected, executed | Rejected by isolated handler | Rejected by browser helper only |
| Alex / `alex@example.com` / Hello | Executed 303 redirect to GET confirmation returning 200 | Handler returned separate success HTML directly from POST | Inline success banner; no separate page |
| Browser checks bypassed | Direct POST validation passed | Server-handler validation present; integration unverified | Fails server requirement: no server validation |
| Script text in a valid message | Accepted safely; not reflected in confirmation | Not reflected in success HTML | No unsafe message insertion shown by inspection |
| Script text in an invalid submission | Escaped and preserved; browser rendering contained zero script elements | Escaped and preserved in isolated rendering | Existing field value retained; no HTML insertion shown by inspection |
| Exact preservation, including surrounding whitespace | Pass, executed | Fail: values trimmed before redisplay | Preserved during invalid handling, inspection |
| Confirmation refresh | Repeated GET returned 200 without repeating POST | No redirect; refresh may prompt for or repeat POST | No confirmation page; inline success state is not retained as a confirmation resource |
| No submitted-value storage, logging or delivery | None found, inspection | None found, inspection | None found, inspection |
| No external services | Pass, inspection | Fail: Google Fonts | Fail: Tailwind CDN, Lucide CDN and Google Fonts |
| No mailbox-existence lookup | Pass, inspection | Pass, inspection | Pass, inspection |

Additional checks found that ChatGPT rejected `.alex@example.com`, `alex..smith@example.com` and `alex@example..com`. Claude accepted the first two but rejected consecutive domain dots. Gemini’s helper accepted all three. These malformed dot-placement findings were checked against the [RFC 5322 dot-atom grammar](https://www.rfc-editor.org/rfc/rfc5322#section-3.2.3). Gemini’s claim that its expression was “RFC 5322 compliant” was therefore overstated. All three accepted the tested plus-tag address. ChatGPT also passed checks for attribute/textarea injection handling, a name exceeding 100 characters and a message exceeding 2,000 characters.

**Implementation findings.** ChatGPT preserved original input while validating trimmed copies, used field-specific errors, and separated POST processing from GET confirmation. Its confirmation accurately stated that messages were neither saved nor emailed. Its length limits were enforced on both the server and form.

Claude provided genuine server handlers, an error summary, associated field hints and explicit HTML escaping. Its separate success document deserved credit even though it remained a POST response. Its startup `console.log` printed the server address, not submitted values, so it was not a submitted-value logging violation.

Gemini’s helper correctly recognised the specifically requested invalid examples, but naming it `mockServerContactEndpoint` did not move execution to a server. Its `status: 400` property did not set an HTTP response status. It used `textContent` for displayed messages; its `innerHTML` assignments inserted fixed icon markup or cleared content, rather than inserting submitted message text. Accepting `<script>alert(1)</script>` as message text was not itself a defect: executable rendering, rather than the presence of those characters, was the relevant security question.

**Prioritised corrections, not implemented:**

1. **Gemini `contact.html`:** Supply a real Flask GET/POST handler, server validation, HTTP responses and a confirmation template. This requires backend work, not a one-line fix.
2. **Claude `server.js`:** Port the behaviour to Flask and declare Flask as a dependency. Adding an Express manifest alone would not satisfy the assignment.
3. **Claude and Gemini asset references:** Remove external fonts/scripts; use local CSS, system fonts and simple local or inline icons.
4. **Both email expressions:** Reject malformed local-part and domain dot placement; describe supported formats accurately without claiming complete email-standard coverage.
5. **Claude success handler:** Replace direct POST success rendering with a 303 redirect to a GET confirmation page, without storing submitted values or placing them in a query string