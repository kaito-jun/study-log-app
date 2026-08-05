import os
import sqlite3
from datetime import datetime

from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "study_log.db")


def get_db():
    if "db" not in g:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            minutes INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/", methods=["GET"])
def index():
    db = get_db()
    logs = db.execute(
        "SELECT * FROM logs ORDER BY created_at DESC"
    ).fetchall()
    summary = db.execute(
        """
        SELECT subject, SUM(minutes) AS total_minutes, COUNT(*) AS count
        FROM logs
        GROUP BY subject
        ORDER BY total_minutes DESC
        """
    ).fetchall()
    return render_template("index.html", logs=logs, summary=summary)


@app.route("/add", methods=["POST"])
def add_log():
    subject = request.form.get("subject", "").strip()
    content = request.form.get("content", "").strip()
    minutes = request.form.get("minutes", "").strip()

    if subject and content and minutes.isdigit():
        db = get_db()
        db.execute(
            "INSERT INTO logs (subject, content, minutes, created_at) VALUES (?, ?, ?, ?)",
            (subject, content, int(minutes), datetime.now().strftime("%Y-%m-%d %H:%M")),
        )
        db.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:log_id>", methods=["POST"])
def delete_log(log_id):
    db = get_db()
    db.execute("DELETE FROM logs WHERE id = ?", (log_id,))
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
