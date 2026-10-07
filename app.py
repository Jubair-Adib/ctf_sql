"""
RED ACCESS — a tiny, intentionally vulnerable CTF challenge.

The /login route builds its SQL query by directly splicing the submitted
username/password into the query string. This is a classic SQL Injection
vulnerability and it is THE challenge — do not parameterize this query.

Everything else (session handling, the admin-only check on /admin, and
flag.txt only ever being read from inside that check) is intentionally
solid, so the *only* way in as admin is through the injection.
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, abort

from init_db import init_db, DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FLAG_PATH = os.path.join(BASE_DIR, "flag.txt")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # session signing only — not part of the challenge


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    if session.get("role") == "admin":
        return redirect(url_for("admin"))
    if session.get("username"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # ============================================================
        # VULNERABLE BY DESIGN — DO NOT "FIX" THIS QUERY.
        #
        # User input is spliced directly into the SQL string instead
        # of being passed as bound parameters. This is the entire
        # point of the challenge: craft input that changes the query's
        # logic (e.g. closes the string and comments out the password
        # check) to log in as admin without knowing the password.
        # ============================================================
        query = (
            "SELECT * FROM users WHERE username = '"
            + username
            + "' AND password = '"
            + password
            + "'"
        )

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(query)
            user = cur.fetchone()
        except sqlite3.Error:
            user = None
        conn.close()

        if user:
            session["username"] = user["username"]
            session["role"] = user["role"]
            if user["role"] == "admin":
                return redirect(url_for("admin"))
            return redirect(url_for("dashboard"))

        error = "Access denied. Invalid credentials."

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if not session.get("username"):
        return redirect(url_for("login"))
    if session.get("role") == "admin":
        return redirect(url_for("admin"))
    return render_template("dashboard.html", username=session["username"])


@app.route("/admin")
def admin():
    # Server-side role check — this is what the injection has to defeat.
    # There is no way to reach the flag without the session role being
    # 'admin', and the only way to set that is through the /login query.
    if session.get("role") != "admin":
        abort(403)

    with open(FLAG_PATH, "r") as f:
        flag = f.read().strip()

    return render_template("admin.html", username=session.get("username"), flag=flag)


@app.errorhandler(403)
def forbidden(e):
    return render_template("denied.html"), 403


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
