from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = 'secretsecret'
@app.route('/')
def index():
    mysql = connectToMySQL('dojo_survey')
    return render_template('index.html')

@app.route('/survey', methods=['POST'])
def submit_survey():
    mysql = connectToMySQL('dojo_survey')

    query = "INSERT INTO survies (name, location, language, comment) VALUES (%(name)s, %(loc)s, %(lang)s, %(comm)s);"

    data = { 
        "name": request.form["name"],
        "loc" : request.form["location"],
        "lang" : request.form["language"],
        "comm" : request.form["comment"]
    }

    is_valid=True
    if len(request.form['name']) < 1:
        is_valid = False
        flash("Please enter a name")
    if len(request.form['location']) < 1:
        is_valid=False
        flash("Please enter a location")
    if len(request.form['language']) < 1:
        is_valid=False
        flash("Please enter a language")
    if len(request.form['comment']) < 1:
        is_valid=False
        flash("Please enter a comment")

    id = mysql.query_db(query, data)
    return redirect(f'/results/{id}')

@app.route('/results/<id>')
def results(id):
    mysql = connectToMySQL('dojo_survey')

    query = "SELECT * FROM survies WHERE id = %(id)s"

    data = { "id" : id}
    results = mysql.query_db(query, data)
    return render_template('result.html', results = results)


if __name__ == '__main__':
    app.run(debug=True)