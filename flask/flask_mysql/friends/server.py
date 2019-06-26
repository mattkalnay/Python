from flask import Flask, render_template, request, redirect 
from mysqlconnection import connectToMySQL
app = Flask(__name__)

@app.route("/users/new")
def new_user():
    return render_template("new.html")

@app.route("/create", methods = ['POST'])
def create_user():
    mysql = connectToMySQL('friends')
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"
    data = {
        "fn": request.form['first_name'],
        "ln": request.form['last_name'],
        "em": request.form['email']
    }
    new_friend_id = mysql.query_db(query,data)
    return redirect(f"/user/{new_friend_id}")

    

@app.route("/user/<id>")
def user_info(id):
    mysql = connectToMySQL('friends')
    query = "SELECT * FROM friends WHERE id = %(id)s;"
    data = {'id' : id}
    friends = mysql.query_db(query, data)
    return render_template("userinfo.html", friends = friends, id = id)

@app.route("/user/<id>/edit")
def user_edit(id):
    mysql = connectToMySQL('friends')
    query = "SELECT * FROM friends WHERE id = %(id)s;"
    data = { "id" : id}
    friends = mysql.query_db(query, data)
    return render_template("edituser.html", edit_id = id, friends = friends)

@app.route("/update/<id>", methods=['POST'])
def edit(id):
    mysql = connectToMySQL('friends')
    query = "UPDATE friends SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s WHERE id = %(id)s;"
    data = {
        "fn": request.form["first_name"],
        "ln": request.form["last_name"],
        "em": request.form["email"],
        "id": id
    }
    mysql.query_db(query,data)
    return redirect(f"/user/{id}")


@app.route("/users")
def users():
    mysql = connectToMySQL('friends')
    friends = mysql.query_db('SELECT * FROM friends;')
    print(friends)
    return render_template('users.html', friends = friends)

@app.route("/users/<id>/destroy")
def delete(id):
    mysql = connectToMySQL('friends')
    # user_id = int(id)
    query = "DELETE FROM friends WHERE id = %(user_id)s;"
    data = {"user_id" : id}
    mysql.query_db(query, data)
    return redirect("/users")


if __name__ == '__main__':
    app.run(debug=True)