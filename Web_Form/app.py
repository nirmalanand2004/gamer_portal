from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "gamerportal"

# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect("gamer.db")
    conn.row_factory = sqlite3.Row
    return conn


# CREATE TABLES
def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS gamers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dob TEXT,
        phone TEXT,
        interested_games TEXT,
        level TEXT
    )
    """)

    conn.commit()
    conn.close()


create_tables()


# LOGIN PAGE
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        ).fetchone()

        if user:
            session["user"] = username
            return redirect(url_for("step1"))

    return render_template("login.html")


# REGISTER PAGE
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        conn.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )
        conn.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# STEP 1
@app.route("/step1", methods=["GET","POST"])
def step1():

    if request.method == "POST":

        session["name"] = request.form["name"]
        session["dob"] = request.form["dob"]
        session["phone"] = request.form["phone"]

        return redirect(url_for("step2"))

    return render_template("step1.html")


# STEP 2
@app.route("/step2", methods=["GET","POST"])
def step2():

    if request.method == "POST":

        games = request.form["interested_games"]
        level = request.form["level"]

        conn = get_db()

        conn.execute("""
        INSERT INTO gamers(name,dob,phone,interested_games,level)
        VALUES(?,?,?,?,?)
        """,(
            session["name"],
            session["dob"],
            session["phone"],
            games,
            level
        ))

        conn.commit()

        return redirect(url_for("success"))

    return render_template("step2.html")


# SUCCESS PAGE
@app.route("/success")
def success():

    gamer = {
        "name":session["name"],
        "dob":session["dob"],
        "phone":session["phone"],
        "interested_games":"Saved",
        "level":"Saved"
    }

    return render_template("success.html",gamer=gamer)


# GAMERS DATABASE PAGE
@app.route("/gamers")
def gamers():

    conn = get_db()
    gamers = conn.execute("SELECT * FROM gamers").fetchall()

    return render_template("gamers.html",gamers=gamers)


if __name__ == "__main__":
    app.run(debug=True)