from datetime import date
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key-for-production"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "tasks.db"


def get_db_connection():
    """Open a database connection and return rows that behave like dictionaries."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the tasks table the first time the application runs."""
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'Medium',
                due_date TEXT DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@app.route("/")
def index():
    status = request.args.get("status", "all")
    search = request.args.get("search", "").strip()

    query = "SELECT * FROM tasks WHERE 1=1"
    parameters = []

    if status == "pending":
        query += " AND completed = 0"
    elif status == "completed":
        query += " AND completed = 1"

    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        search_term = f"%{search}%"
        parameters.extend([search_term, search_term])

    query += """
        ORDER BY completed ASC,
        CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
        CASE WHEN due_date = '' THEN 1 ELSE 0 END,
        due_date ASC,
        id DESC
    """

    with get_db_connection() as connection:
        tasks = connection.execute(query, parameters).fetchall()
        counts = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) AS completed
            FROM tasks
            """
        ).fetchone()

    stats = {
        "total": counts["total"] or 0,
        "pending": counts["pending"] or 0,
        "completed": counts["completed"] or 0,
    }

    return render_template(
        "index.html",
        tasks=tasks,
        stats=stats,
        status=status,
        search=search,
        today=date.today().isoformat(),
    )


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Medium")
    due_date = request.form.get("due_date", "").strip()

    if not title:
        flash("Please enter a task title.", "error")
        return redirect(url_for("index"))

    if priority not in {"Low", "Medium", "High"}:
        priority = "Medium"

    with get_db_connection() as connection:
        connection.execute(
            """
            INSERT INTO tasks (title, description, priority, due_date)
            VALUES (?, ?, ?, ?)
            """,
            (title, description, priority, due_date),
        )

    flash("Task added successfully.", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    with get_db_connection() as connection:
        task = connection.execute(
            "SELECT completed FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if task is None:
            flash("Task not found.", "error")
        else:
            new_status = 0 if task["completed"] else 1
            connection.execute(
                "UPDATE tasks SET completed = ? WHERE id = ?",
                (new_status, task_id),
            )
            flash("Task status updated.", "success")

    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    with get_db_connection() as connection:
        task = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if task is None:
            flash("Task not found.", "error")
            return redirect(url_for("index"))

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            priority = request.form.get("priority", "Medium")
            due_date = request.form.get("due_date", "").strip()

            if not title:
                flash("Please enter a task title.", "error")
                return render_template("edit.html", task=task)

            if priority not in {"Low", "Medium", "High"}:
                priority = "Medium"

            connection.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, priority = ?, due_date = ?
                WHERE id = ?
                """,
                (title, description, priority, due_date, task_id),
            )
            flash("Task updated successfully.", "success")
            return redirect(url_for("index"))

    return render_template("edit.html", task=task)


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    with get_db_connection() as connection:
        connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


init_db()

if __name__ == "__main__":
    app.run(debug=True)
