from flask import Flask, redirect, render_template, request, flash, session
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = "secrete3434"


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Table ya BOOKERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        number TEXT,
        rooms INTEGER,
        day_to_spend INTEGER,
        address TEXT,
        date TEXT
    )
    """)

    # Table ya USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        number TEXT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()  # ← moja tu mwishoni
    conn.close()   # ← moja tu mwishoni

init_db()

# ROUTES
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rooms")
def rooms():
    return render_template("rooms.html")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        name = request.form["name"]
        number = request.form["number"]
        rooms = request.form["rooms"]        # ← rooms siyo room
        day_to_spend = request.form["day_to_spend"]
        address = request.form["address"]
        date = datetime.now().strftime("%d/%m/%Y %H:%M")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO bookers(name, number, rooms, day_to_spend, address, date)
        VALUES(?,?,?,?,?,?)
        """, (name, number, rooms, day_to_spend, address, date))
        conn.commit()
        conn.close()

        flash("Booking imefanikiwa!", "success")
        return redirect("/booking")

    return render_template("booking.html")

@app.route("/confirm")
def confirm():
    return render_template("confirm.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        number = request.form["number"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords not matched!", "error")
            return redirect("/register")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users(name, email, number, username, password)
        VALUES(?,?,?,?,?)
        """, (name, email, number, username, password))
        conn.commit()
        conn.close()

        flash("Account registered successfully!", "success")
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            flash("Umeingia!", "success")
            return redirect("/booking")
        else:
            flash("Username au password si sahihi!", "error")
            return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Umetoka!", "success")
    return redirect("/login")

@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookers")
    bookers = cursor.fetchall()
    conn.close()
    return render_template("admin.html", bookers=bookers)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Booking imefutwa!", "success")
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)  # ← debug nje ya quotes!