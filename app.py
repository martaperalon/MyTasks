from flask import Flask, render_template, request, redirect, session  # framework stuff
from flask_session import Session  # framework stuff
from werkzeug.security import generate_password_hash, check_password_hash  # password hashing
import sqlite3  # sql database

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False  # Session ends when browser closes
app.config["SESSION_TYPE"] = "filesystem"  # Session saves in disk
Session(app)

# function that connects with database


def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row  # access data like it's dicitionaries
    return conn


# create users table if it doesn't exist, with unique id, username and hash (encrypted password)
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hash TEXT NOT NULL
        )
    """)

# homepage


@app.route("/")
def index():
    if "user_id" not in session:  # checks user_id exists in dictionary session
        return redirect("/login")  # if user is not logged, redirects them to login page
    return redirect("/tasks")  # if they are logged, redirects them to tasks page

# user register


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":  # if method is POST collect username, password and confirmation
        username = request.form["username"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]

        if not username or not password or not confirmation:  # verifies fields are correct
            error = "Todos los campos son obligatorios."
        elif password != confirmation:
            error = "Las contraseñas no coinciden."
        else:
            hash_pw = generate_password_hash(password)  # creates password hash (encrypts it)
            try:
                with get_db() as db:
                    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                               (username, hash_pw))
                return redirect("/login")  # redirects to login page
            except sqlite3.IntegrityError:
                error = "El nombre de usuario ya existe."  # if user already exists, throws an error

    return render_template("register.html", error=error)  # if method is GET, shows register form

# login


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()  # closes session if there's a session
    error = None
    if request.method == "POST":  # if method is POST, gets username and password
        username = request.form["username"]
        password = request.form["password"]

        with get_db() as db:
            user = db.execute("SELECT * FROM users WHERE username = ?", (username,)
                              ).fetchone()  # searches for username in database

        # if username and password aren't correct or don't match throws an error
        if user is None or not check_password_hash(user["hash"], password):
            error = "Nombre o contraseña incorrectos"
        else:
            session["user_id"] = user["id"]  # if they're correct saves user unique id in session
            return redirect("/")

    # if method is GET shows login form again but with error message
    return render_template("login.html", error=error)

# logout


@app.route("/logout")
def logout():
    session.clear()  # closes current session
    return redirect("/login")  # shows login page

# add a task


# GET shows info, POST receives form data and saves it
@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if "user_id" not in session:  # if there's no session, redirects to login page
        return redirect("/login")

    # if method is POST, takes the data of the form (title, descripcion and due date)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        due_date = request.form.get("due_date", None)

        if not title:  # if the title field is empty shows an error
            return "El título es obligatorio", 400

        db = get_db()
        db.execute(  # inserts task with the given information in logged user
            "INSERT INTO tasks (user_id, title, description, due_date, completed) VALUES (?, ?, ?, ?, 0)",
            (session["user_id"], title, description, due_date)
        )
        db.commit()  # save the changes in the database
        return redirect("/tasks/pending")  # once inserted, shows pending tasks

    return redirect("/tasks/pending")  # if method is GET shows pending tasks directly

# show pending tasks


@app.route("/tasks/pending")
def tasks_pending():
    if "user_id" not in session:  # if user is not logged of course redirect them to log page
        return redirect("/login")
    db = get_db()
    tasks = db.execute(  # order pending tasks (tasks with completed = 0) by due date
        "SELECT * FROM tasks WHERE user_id = ? AND completed = 0 ORDER BY due_date IS NULL, due_date ASC",
        (session["user_id"],)
    ).fetchall()
    return render_template("tasks.html", tasks=tasks, show_completed=False)  # shows ordered tasks

# show completed tasks


@app.route("/tasks/completed")
def tasks_completed():  # same but tasks with completed = 1
    if "user_id" not in session:
        return redirect("/login")
    db = get_db()
    tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? AND completed = 1 ORDER BY due_date DESC",
        (session["user_id"],)
    ).fetchall()
    return render_template("tasks.html", tasks=tasks, show_completed=True)

# mark task as completed


@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    if "user_id" not in session:
        return redirect("/login")
    db = get_db()  # task_id comes from the URL
    task = db.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?",
                      (task_id, session["user_id"])).fetchone()
    if task is None:
        return "Tarea no encontrada", 404

    # changes completed value depending on checkbox value
    completed = int(request.form.get("completed", 0))
    db.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    db.commit()
    referer = request.headers.get("Referer")  # redirect user where they were before
    return redirect(referer or "/tasks/pending")

# delete a task


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    if "user_id" not in session:
        return redirect("/login")
    db = get_db()
    # deletes task with id=task_id if belongs to logged user
    db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, session["user_id"]))
    db.commit()
    referer = request.headers.get("Referer")  # redirect user where they were before
    return redirect(referer or "/tasks/pending")
