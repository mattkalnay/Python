from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'secretsecret'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/register', methods=['POST'])
def register():
    if len(request.form['password']) > 1:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)

    is_valid = True

    mysql = connectToMySQL('login_reg')
    emailz = mysql.query_db("SELECT email FROM users;")
    for email in emailz:
        if email['email'] == request.form['email']:
            is_valid = False
            flash('Email Is Already In Use', 'eerror')


    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!", 'eerror')



    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("First Name Must Be At Least 2 Characters", 'ferror')
    
    if (request.form['first_name']).isalpha() == False:
        is_valid = False
        flash('First Name Must Contain Only Letters', 'ferror')

    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Last Name Must Be At Least 2 Characters", 'lerror')

    if (request.form['last_name']).isalpha() == False:
        is_valid = False
        flash('Last Name Must Contain Only Letters', 'lerror')


    if len(request.form['password']) < 8:
        is_valid = False
        flash("Password Must Be At Least 8 Characters", 'perror')

    if (request.form['password']) != (request.form['password_con']):
        is_valid = False
        flash(u"Password and Password Confirmation Does Not Match", 'perror')


    
    if not is_valid:
        return redirect('/')

    
    mysql = connectToMySQL('login_reg')
    query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s, NOW(), NOW());" 
    data = {
        "fn" : request.form['first_name'],
        "ln" : request.form['last_name'],
        "em" : request.form['email'],
        "pw" : pw_hash
    }

    registered_id = mysql.query_db(query, data)
    print(registered_id)
    mysql = connectToMySQL('login_reg')
    query = "SELECT * FROM users WHERE id = %(registered_id)s;"
    data = {
        "registered_id" : registered_id 
    }
    log = mysql.query_db(query, data)
    if len(log) > 0:
        session['user'] = log
        print(session['user'])
        return redirect('/success')
    else: 
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL('login_reg')
    query = "SELECT * FROM users WHERE email = %(em)s;"
    data = {
        "em" : request.form['e_log'],
    }
    log = mysql.query_db(query, data)
    if len(log) > 0:
        if bcrypt.check_password_hash(log[0]['password'], request.form['p_log']):
            session['user'] = log
            print(session['user'])
            return redirect('/success')
    else: 
        flash("Incorrect Login", 'loerror')
        return redirect('/')


@app.route('/logout')
def logout():
    if 'user' in session:
        session['user'] = None
    print(session['user']) 
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True) 