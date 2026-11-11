from flask import Flask, render_template
from database import get_connection
import os


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "TestKey123")

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Login page
@app.route("/login")
def login():
    return render_template("login.html")


# Register page
@app.route("/register")
def register():
    return render_template("register.html")


# Certifications page
@app.route("/certifications")
def certifications():

    dbconn = get_connection()

    certification_records = dbconn.execute("""
        SELECT * FROM Certification
    """).fetchall()

    dbconn.close()

    return render_template(
        "certifications.html",
        certifications=certification_records
    )


if __name__ == "__main__":
    app.run(debug=True)
