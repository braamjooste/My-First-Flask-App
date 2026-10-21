from flask import Flask

app = Flask(__name__)

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
    """

@app.route("/about")
def about():
    return "<h1>About</h1><p>This is my first Flask app.</p>"

if __name__ == "__main__":
    app.run(debug=True)