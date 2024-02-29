@app.route('/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session["name"] = str(request.form.get("name")).strip()
        session["uname"] = str(request.form.get("uname")).strip()
        session["pswd"] = str(request.form.get("pswd")).strip()
        existing_user = users.find_one({"uname": session["uname"]})
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('signup'))
        users.insert_one({"name": session["name"], "uname": session["uname"], "pswd": session["pswd"]})
        return redirect(url_for('index'))
    return render_template("login.html")