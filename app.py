from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from flask_bcrypt import Bcrypt
from flask_session import Session
import datetime
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.flask_db
users = db.users

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "BADKEY"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
Session(app)

debug_login = False

def go_to_login():
    if debug_login:
        return False
    if "uname" not in session or not session.get("uname"):
        return True
    else:
        return False

@app.route('/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session["name"] = str(request.form.get("name")).strip()
        session["uname"] = str(request.form.get("uname")).strip()
        session["pswd"] = str(request.form.get("pswd")).strip()

        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(session["pswd"]).decode('utf-8')

        existing_user = users.find_one({"uname": session["uname"], "name": session["name"]})
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('signup'))

        users.insert_one({"name": session["name"], "uname": session["uname"], "pswd": hashed_password})
        return redirect(url_for('index'))

    return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["uname"] = str(request.form.get("uname")).strip()
        session["pswd"] = str(request.form.get("pswd")).strip()
        existing_user = users.find_one({"uname": session["uname"]})

        if not existing_user or not bcrypt.check_password_hash(existing_user["pswd"], session["pswd"]):
            flash('Incorrect username or password. Please try again.', 'error')
            return redirect(url_for('login'))

        session["name"] = existing_user.get("name")
        return render_template("index.html", name=session["name"])

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

    return render_template("quiztemp.html", questions=questions)

@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('login'))


# @app.route('/add_question', methods=["POST"])
# def add_question():
#     question_text = request.json.get('question')

#     existing_user = users.find_one({"uname": session["uname"]})

#     if existing_user:
  
#         users.update_one({"uname": session["uname"]}, {"$push": {"questions": question_text}})
#         return jsonify({"success": True})
#     else:
#         return jsonify({"success": False, "message": "User not found"})
@app.route('/add_question', methods=["POST"])
def add_question():
    topic = request.json.get('question')
    # print(topic)
    bard = BardGenerator()
    bard.generate_questions_from_text_single_word(topic=topic, difficulty="college")
    # print(bard.questions)
    existing_user = users.find_one({"uname": session["uname"], "name": session["name"]})
    if existing_user:
        users.update_one({"uname": session["uname"], "name": session["name"]}, {"$push": {"topic": topic}})
    else: return jsonify({"success": False})
    return jsonify({"success": True, "question":bard.questions["Question"], "answer":bard.questions["Answer"]})


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