from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = 'secretsecret'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    mysql = connectToMySQL('email_reg')
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!")
        return redirect('/')    

    mysql = connectToMySQL('email_reg')

    query = "INSERT INTO user_emails (email, created_at, updated_at) VALUES (%(em)s, NOW(),NOW());" 

    data = {"em" : request.form["email"]}

    id = mysql.query_db(query,data)



    return redirect(f'/success/{id}')

@app.route('/success/<id>')
def success(id):
    mysql = connectToMySQL('email_reg')

    results = mysql.query_db("SELECT * FROM user_emails;")
    
    query = "SELECT * FROM user_emails WHERE id = %(id)s"

    data = {"id" : id}

    mysql = connectToMySQL('email_reg')

    email = mysql.query_db(query,data)
    return render_template('success.html', results = results, email = email)


if __name__ == '__main__':
    app.run(debug=True)