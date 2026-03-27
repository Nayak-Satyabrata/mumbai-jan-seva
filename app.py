from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3, os, uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "jansevakey2025"
DB = "database.db"

# ── DB SETUP ──────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            ward TEXT
        );
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            name TEXT,
            category TEXT,
            description TEXT,
            location TEXT,
            ward TEXT,
            lat REAL,
            lng REAL,
            status TEXT DEFAULT 'Submitted',
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)
        # Seed demo complaints
        count = db.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
        if count == 0:
            seeds = [
                ("TKT-0001", 1, "Rahul Sharma",   "Road Damage",       "Large pothole near Kharghar station entrance causing accidents.", "Kharghar, Sector 7",  "Ward 12", 19.0477, 73.0694, "In Progress",  "2025-02-10", "2025-02-13"),
                ("TKT-0002", 2, "Priya Desai",    "Water Supply",      "No water supply for 3 days in our building.",                    "Vashi, Sector 17",    "Ward 5",  19.0748, 73.0107, "Resolved",     "2025-02-08", "2025-02-12"),
                ("TKT-0003", 3, "Amit Patil",     "Garbage Collection","Garbage not collected for over a week, causing health hazard.",   "Panvel, New Panvel",  "Ward 3",  18.9894, 73.1175, "Submitted",    "2025-02-15", "2025-02-15"),
                ("TKT-0004", 4, "Sneha More",     "Street Lighting",   "6 streetlights non-functional on the main road.",                "Belapur, Sector 11",  "Ward 8",  19.0228, 73.0389, "Under Review", "2025-02-14", "2025-02-14"),
                ("TKT-0005", 5, "Vikram Nair",    "Drainage/Sewage",   "Sewage overflow near the market area.",                          "Nerul, Sector 20",    "Ward 6",  19.0387, 73.0164, "In Progress",  "2025-02-11", "2025-02-13"),
            ]
            db.executemany("INSERT INTO complaints (ticket,user_id,name,category,description,location,ward,lat,lng,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", seeds)
            db.commit()

# ── AUTH ──────────────────────────────────────────────────
@app.route("/", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        pw    = request.form["password"]
        # Admin shortcut
        if email == "admin@janseva.gov.in" and pw == "admin123":
            session["user"] = {"id": 0, "name": "Admin", "email": email, "role": "admin"}
            return redirect(url_for("admin"))
        db   = get_db()
        user = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email, pw)).fetchone()
        if user:
            session["user"] = {"id": user["id"], "name": user["name"], "email": user["email"], "role": "citizen"}
            return redirect(url_for("dashboard"))
        error = "Invalid email or password."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET","POST"])
def register():
    error = None
    if request.method == "POST":
        try:
            db = get_db()
            db.execute("INSERT INTO users (name,email,password,phone,ward) VALUES (?,?,?,?,?)",
                (request.form["name"], request.form["email"], request.form["password"],
                 request.form.get("phone",""), request.form.get("ward","")))
            db.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            error = "Email already registered."
    return render_template("register.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ── CITIZEN ───────────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    if "user" not in session: return redirect(url_for("login"))
    db  = get_db()
    uid = session["user"]["id"]
    complaints = db.execute("SELECT * FROM complaints WHERE user_id=? ORDER BY created_at DESC", (uid,)).fetchall()
    return render_template("dashboard.html", user=session["user"], complaints=complaints)

@app.route("/submit", methods=["GET","POST"])
def submit():
    if "user" not in session: return redirect(url_for("login"))
    if request.method == "POST":
        ticket = "TKT-" + str(uuid.uuid4())[:6].upper()
        db = get_db()
        db.execute("""INSERT INTO complaints
            (ticket,user_id,name,category,description,location,ward,lat,lng,status,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (ticket, session["user"]["id"], session["user"]["name"],
             request.form["category"], request.form["description"],
             request.form["location"], request.form["ward"],
             float(request.form.get("lat") or 19.076), float(request.form.get("lng") or 72.877),
             "Submitted", datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d")))
        db.commit()
        return redirect(url_for("track", ticket=ticket))
    return render_template("submit.html", user=session["user"])

@app.route("/track", methods=["GET","POST"])
def track():
    complaint = None
    ticket    = request.args.get("ticket","")
    if request.method == "POST":
        ticket = request.form["ticket"].strip().upper()
    if ticket:
        complaint = get_db().execute("SELECT * FROM complaints WHERE ticket=?", (ticket,)).fetchone()
    return render_template("track.html", user=session.get("user"), complaint=complaint, ticket=ticket)

@app.route("/map")
def map_view():
    complaints = get_db().execute("SELECT * FROM complaints").fetchall()
    data = [{"ticket":c["ticket"],"category":c["category"],"location":c["location"],
             "status":c["status"],"lat":c["lat"],"lng":c["lng"]} for c in complaints]
    return render_template("map.html", user=session.get("user"), complaints_json=data)

# ── ADMIN ─────────────────────────────────────────────────
@app.route("/admin")
def admin():
    if "user" not in session or session["user"].get("role") != "admin":
        return redirect(url_for("login"))
    db = get_db()
    complaints = db.execute("SELECT * FROM complaints ORDER BY created_at DESC").fetchall()
    stats = {
        "total":       db.execute("SELECT COUNT(*) FROM complaints").fetchone()[0],
        "submitted":   db.execute("SELECT COUNT(*) FROM complaints WHERE status='Submitted'").fetchone()[0],
        "in_progress": db.execute("SELECT COUNT(*) FROM complaints WHERE status='In Progress'").fetchone()[0],
        "resolved":    db.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'").fetchone()[0],
    }
    return render_template("admin.html", user=session["user"], complaints=complaints, stats=stats)

@app.route("/admin/update/<ticket>", methods=["POST"])
def update_status(ticket):
    if "user" not in session or session["user"].get("role") != "admin":
        return redirect(url_for("login"))
    new_status = request.form["status"]
    db = get_db()
    db.execute("UPDATE complaints SET status=?, updated_at=? WHERE ticket=?",
               (new_status, datetime.now().strftime("%Y-%m-%d"), ticket))
    db.commit()
    return redirect(url_for("admin"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
