"""Send requests directly to Flask, bypassing browser validation."""
import unittest
from unittest.mock import patch

from app import app


class ContactTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()
        self.valid = {"name": "Alex", "email": "alex@example.com", "message": "Hello!"}

    def test_form_loads(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertIn(b"My First Flask App", self.client.get("/").data)
        self.assertIn(b'href="/contact"', self.client.get("/").data)
        self.assertEqual(self.client.get("/about").status_code, 200)
        self.assertEqual(self.client.get("/contact").status_code, 200)
        with self.client.get("/static/style.css") as response:
            self.assertEqual(response.status_code, 200)

    def test_empty_and_whitespace_submissions(self):
        for data in ({}, dict.fromkeys(self.valid, " \t\n ")):
            with self.subTest(data=data):
                response = self.client.post("/contact", data=data)
                self.assertEqual(response.status_code, 400)
                for field in (b"name-error", b"email-error", b"message-error"):
                    self.assertIn(field, response.data)

    def test_missing_and_malformed_email(self):
        for email in ("", "   ", "bad", "notanemail", "a@@example.com", "a..b@example.com", "a@-example.com"):
            with self.subTest(email=email):
                response = self.client.post("/contact", data={**self.valid, "email": email})
                self.assertEqual(response.status_code, 400)
                self.assertIn(b"email-error", response.data)

    def test_limits_are_checked_on_server(self):
        for field, value in (("name", "a" * 101), ("email", "a" * 250 + "@x.com"), ("message", "a" * 2001)):
            response = self.client.post("/contact", data={**self.valid, field: value})
            self.assertEqual(response.status_code, 400)
            self.assertIn(f'{field}-error'.encode(), response.data)

    def test_invalid_submission_preserves_and_escapes_input(self):
        data = {"name": '  <script>alert("x")</script>  ', "email": "bad", "message": "  Hello!  "}
        response = self.client.post("/contact", data=data)
        self.assertIn(b"  &lt;script&gt;alert(&#34;x&#34;)&lt;/script&gt;  ", response.data)
        self.assertIn(b'value="bad"', response.data)
        self.assertIn(b"  Hello!  </textarea>", response.data)
        self.assertNotIn(b"<script>", response.data)

    def test_valid_submission_redirects_without_storing_values(self):
        with patch("socket.socket", side_effect=AssertionError("Network access attempted")):
            response = self.client.post("/contact", data=self.valid)
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.location, "/contact/confirmation")
        self.assertNotIn("Set-Cookie", response.headers)
        page = self.client.get(response.location)
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"Your form passed validation.", page.data)
        self.assertNotIn(b"alex@example.com", page.data)
        self.assertEqual(self.client.get(response.location).status_code, 200)

    def test_long_invalid_message_is_preserved(self):
        message = "a" * 17000
        response = self.client.post("/contact", data={**self.valid, "message": message})
        self.assertEqual(response.status_code, 400)
        self.assertIn(message.encode(), response.data)

    def test_script_in_message_is_escaped_on_validation_error(self):
        response = self.client.post("/contact", data={
            **self.valid, "email": "bad", "message": "<script>alert(1)</script>"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"&lt;script&gt;alert(1)&lt;/script&gt;", response.data)
        self.assertNotIn(b"<script>alert(1)</script>", response.data)

    def test_script_in_message_is_not_rendered_on_success(self):
        response = self.client.post("/contact", data={
            **self.valid, "message": "<script>alert(1)</script>"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"<script>alert(1)</script>", response.data)


if __name__ == "__main__":
    unittest.main()
