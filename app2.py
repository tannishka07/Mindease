from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mindease"]
users_collection = db["users"]

print("✅ Mongo connected")
import pandas as pd

df = pd.read_csv("data.csv")

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)
@app.route("/check")
def check():
    return "SERVER WORKING"

# ---------------- TEMP STORAGE ----------------
moods = []
journals = []

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("app.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print("🔥 Signup route triggered")

        username = request.form.get("username")
        password = request.form.get("password")
        print("Username:", username)
        print("Password:", password)

        try:
            existing = users_collection.find_one({"username": username})
            print("Existing user:", existing)

            result = users_collection.insert_one({
                "username": username,
                "password": password
            })

            print("✅ Inserted ID:", result.inserted_id)

        except Exception as e:
            print("❌ ERROR:", e)

        return "Signup attempted"

    return render_template("signup.html")
# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users_collection.find_one({
            "username": username,
            "password": password
        })

        if user:
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials ❌"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    return redirect(url_for("home"))


# ---------------- MOOD PAGE ----------------
@app.route("/mood")
def mood():
    return render_template("mood.html")


# ---------------- SAVE MOOD ----------------
@app.route("/save_mood", methods=["POST"])
def save_mood():
    data = request.json

    mood = {
        "mood": data.get("mood"),
        "time": str(datetime.now())
    }

    moods.append(mood)

    return jsonify({"message": "Mood saved successfully"})


# ---------------- GET MOODS (OPTIONAL DASHBOARD) ----------------
@app.route("/get_moods")
def get_moods():
    return jsonify(moods)


# ---------------- JOURNAL PAGE ----------------
@app.route("/journal")
def journal():
    return render_template("journal.html")


# ---------------- SAVE JOURNAL ----------------
@app.route("/save_journal", methods=["POST"])
def save_journal():
    data = request.json

    journal = {
        "text": data.get("text"),
        "time": str(datetime.now())
    }

    journals.append(journal)

    return jsonify({"message": "Journal saved successfully"})


# ---------------- GET JOURNALS ----------------
@app.route("/get_journals")
def get_journals():
    return jsonify(journals)


# ---------------- MUSIC PAGE ----------------
@app.route("/music")
def music():
    data = df.to_dict(orient="records")   # 👈 use CSV here
    return render_template("music.html", data=data)

# ---------------- MUSIC RECOMMENDATION ----------------
@app.route("/get_music", methods=["POST"])
def get_music():
    mood = request.json.get("mood")

    music_map = {
        "happy": ["Happy Song 🎉", "On Top of the World"],
        "sad": ["Fix You", "Let Her Go"],
        "stressed": ["Lo-fi Beats 🎧", "Calm Piano"],
        "angry": ["Relaxing Nature Sounds 🌿"]
    }

    return jsonify({"songs": music_map.get(mood, [])})


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

