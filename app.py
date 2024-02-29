from flask import Flask, render_template, redirect, url_for, request, session,jsonify,flash
from officialmodel import BardGenerator
from flask_session import Session
from flask_bcrypt import Bcrypt
import datetime
import requests
import json
from pymongo import MongoClient


client = MongoClient('localhost', 27017)

db = client.flask_db
users = db.users


app = Flask(__name__)
app.secret_key = "BADKEY"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
Session(app)
bcrypt = Bcrypt(app)


def go_to_login():
    # return False
    if "uname" not in session or not session.get("uname"):
        return True
    else:
        return False

@app.route('/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session["name"] = str(request.form.get("name")).strip()
        session["uname"] = str(request.form.get("uname")).strip()
        raw_password = str(request.form.get("pswd")).strip()  # Get the raw password
        hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')  # Hash the password
        session["pswd"] = hashed_password

        existing_user = users.find_one({"uname": session["uname"]})
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('signup'))

        users.insert_one({"name": session["name"], "uname": session["uname"], "pswd": session["pswd"]})
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["uname"] = str(request.form.get("uname")).strip()
        raw_password = str(request.form.get("pswd")).strip()  # Get the raw password
        existing_user = users.find_one({"uname": session["uname"]})

        if existing_user and bcrypt.check_password_hash(existing_user["pswd"], raw_password):
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password. Please try again.', 'error')
            return redirect(url_for('login'))

    return render_template("login.html")


@app.route("/index")
def index():
    if go_to_login():
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/timer")
def timer():
    if go_to_login():
        return redirect(url_for('login'))
    return render_template("pomo.html")

@app.route("/flash_page")
def flash_page():
    if go_to_login():
        return redirect(url_for('login'))
    return render_template("quiz.html")

@app.route("/quizform")
def quizform():
    if go_to_login():
        return redirect(url_for('login'))
    return render_template("quizform.html")

@app.route('/generate_quiz', methods=["POST"])
def generate_quiz():
    topic = request.form.get("topic")
    difficulty = request.form.get("difficulty")

    bard = BardGenerator()
    bard.generate_questions_from_text_mcq(topic, difficulty)
    questions = bard.questions

    return jsonify(questions)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if go_to_login():
        return redirect(url_for('login'))

    if request.method == "POST":
        return redirect(url_for('quiztemp', topic=request.form.get("topic"), difficulty=request.form.get("difficulty")))

    return render_template("quizform.html")


@app.route("/quiztemp")
def quiztemp():
    if go_to_login():
        return redirect(url_for('login'))

    topic = request.args.get("topic")
    difficulty = request.args.get("difficulty")
    response = requests.post('http://127.0.0.1:5000/generate_quiz', data={"topic": topic, "difficulty": difficulty})
    print(response)
    questions = response.json()
    print(questions)
    return render_template("quiztemp.html", questions=questions)

@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/add_question', methods=["POST"])
def add_question():
    question_text = request.json.get('question')

    existing_user = users.find_one({"uname": session["uname"]})

    if existing_user:
  
        users.update_one({"uname": session["uname"]}, {"$push": {"questions": question_text}})
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "User not found"})


@app.route('/get_questions')
def get_questions():
    existing_user = users.find_one({"uname": session["uname"]})

    if existing_user:
        questions = existing_user.get("questions", [])
        return jsonify({"questions": questions})
    else:
        return jsonify({"questions": []})


if __name__ == '__main__':
    app.run(debug=True)