from flask import Flask, render_template, request, redirect, session, flash 
from mysqlconnection import connectToMySQL
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('first_flask')
    friends = mysql.query_db('SELECT * FROM friends;')
    print(friends)
    return render_template("index.html", all_friends = friends)

@app.route("/process", methods=["POST"])
def add_friend_to_db():
    print(request.form)
    mysql = connectToMySQL("first_flask")
    is_valid = True
    if len(request.form['fname']) < 1:
        is_valid = False
        flash("Please enter a first name.")
    if len(request.form['lname']) < 1:
        is_valid = False
        flash("Please enter a last name.")
    if len(request.form['occ']) < 2:
        is_valid = False
        flash("Please enter more than 3 characters")
    
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(occup)s, NOW(), NOW());"
    data= {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "occup": request.form["occ"]
    }
    new_friend_id = mysql.query_db(query,data)
    flash(Success!)
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)

