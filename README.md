# StudyFlow — Student Task Manager

A beginner-friendly Flask web application for managing student tasks. It uses SQLite, which is included with Python.

## Features
- Add tasks with a description, priority, and due date
- List, search, and filter tasks
- Mark tasks as completed or pending
- Edit and delete tasks
- Dashboard counts for all, pending, and completed tasks
- Tasks persist in the local `tasks.db` database

## Requirements
- Python 3.10 or newer
- pip
- A web browser

## Run on Windows
1. Extract the ZIP file.
2. Open Command Prompt or PowerShell in the `student_task_manager` folder.
3. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
4. Activate it:
   ```powershell
   .venv\Scripts\activate
   ```
5. Install Flask:
   ```powershell
   py -m pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   py app.py
   ```
7. Open `http://127.0.0.1:5000` in your browser.

If `py` is not recognized, try replacing `py` with `python`.

## Run on macOS or Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`.

## How the project works
- `app.py`: Flask routes, validation, and database queries
- `templates/`: HTML pages rendered by Flask
- `static/style.css`: page styling
- `tasks.db`: created automatically on first run and stores your tasks

## Test checklist
1. Add a task titled `Practise Python loops`.
2. Add another task with High priority and a due date.
3. Search for `Python`; check that matching tasks appear.
4. Choose Pending and then mark one task completed.
5. Choose Completed and confirm the task appears there.
6. Edit a task and save the changes.
7. Delete a test task.
8. Stop the server with `Ctrl+C`, restart it, and confirm remaining tasks are still saved.

## Troubleshooting
- **`No module named flask`**: activate your virtual environment and run `python -m pip install -r requirements.txt`.
- **Port 5000 is busy**: close the other app using port 5000, or change the last line to `app.run(debug=True, port=5001)` and open `http://127.0.0.1:5001`.
- **Browser cannot connect**: keep the terminal running while you use the website.
- **Changes are not showing**: refresh the browser. Flask debug mode reloads Python changes automatically.

## Learning notes
This is a local learning project, not a production deployment. Before publishing it online, use a secure random secret key, turn off debug mode, add CSRF protection, and review security settings.
