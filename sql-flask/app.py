from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "dev-secret-for-demo-only"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "example.db")


# ---------- DB helpers ----------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    db.executescript(
        """
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        INSERT INTO users (username, password) VALUES
            ('alice', 'password123'),
            ('bob',   'hunter2'),
            ('admin', 'supersecret');
        """
    )
    db.commit()



@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ---------- Routes ----------

@app.route("/")
def home():
    return render_template("home.html")


# --- Vulnerable login (classic SQL injection) ---
@app.route("/login-vuln", methods=["GET", "POST"])
def login_vuln():
    query = None
    users = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # VULNERABLE: user input concatenated directly into SQL
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        db = get_db()
        try:
            users = db.execute(query).fetchall()
        except sqlite3.Error as e:
            flash(f"SQL error: {e}", "error")
            users = []

        if users:
            return render_template(
                "login_success.html",
                user=users[0],
                mode="Vulnerable login",
                query=query,
                users=users,
            )
        else:
            flash("Invalid username or password (or your injection failed).", "error")

    return render_template("login_vuln.html", query=query)


# --- Fixed login (parameterized query) ---
@app.route("/login-fixed", methods=["GET", "POST"])
def login_fixed():
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    executed_params = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        db = get_db()
        users = db.execute(query, (username, password)).fetchall()
        executed_params = (username, password)

        if users:
            return render_template(
                "login_success.html",
                user=users[0],
                mode="Fixed login",
                query=query,
                params=executed_params,
                users=users,
            )
        else:
            flash("Invalid username or password.", "error")

    return render_template("login_fixed.html", query=query, params=executed_params)

def setup_app():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    with app.app_context():
        init_db()



if __name__ == "__main__":
    setup_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
