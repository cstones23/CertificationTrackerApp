from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_connection
import os
import sqlite3



app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")


# Home page
@app.route("/")
def home():
    return render_template("index.html")



# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        dbconn = get_connection()

        user = dbconn.execute("""
            SELECT * FROM User
            WHERE username = ?
        """, (username,)).fetchone()

        dbconn.close()

        if user and check_password_hash(user["password_hash"], password):

            session.clear()
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("certifications"))

        else:
            return render_template(
                "login.html",
                error="Invalid username or password."
            )

    return render_template("login.html")








# Register page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]
        role = "user"

        if not username or not password:
            return render_template(
                "register.html",
                error="Please complete all fields."
            )

        if len(password) < 8:
            return render_template(
                "register.html",
                error="Password must be at least 8 characters."
            )

        password_hash = generate_password_hash(password)

        dbconn = get_connection()

        try:
            dbconn.execute("""
                INSERT INTO User (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username, password_hash, role))

            dbconn.commit()

        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="Username already exists."
            )

        finally:
            dbconn.close()

        return render_template(
            "register.html",
            success="Account registered successfully."
        )

    return render_template("register.html")









# Certifications page
@app.route("/certifications")
def certifications():

    if "user_id" not in session:
        return redirect(url_for("login"))

    dbconn = get_connection()

    certification_records = dbconn.execute("""
        SELECT * FROM Certification
    """).fetchall()

    dbconn.close()

    return render_template(
        "certifications.html",
        certifications=certification_records
    )



@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)
