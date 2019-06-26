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



@app.route('/register', methods=['POST'])
def register():
    if len(request.form['password']) > 1:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)

    is_valid = True

    mysql = connectToMySQL('wall')
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

    
    mysql = connectToMySQL('wall')
    query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s);" 
    data = {
        "fn" : request.form['first_name'],
        "ln" : request.form['last_name'],
        "em" : request.form['email'],
        "pw" : pw_hash
    }

    registered_id = mysql.query_db(query, data)
    print(registered_id)
    mysql = connectToMySQL('wall')
    query = "SELECT * FROM users WHERE id = %(registered_id)s;"
    data = {
        "registered_id" : registered_id 
    }
    log = mysql.query_db(query, data)
    if len(log) > 0:
        session['user'] = log
        print(session['user'])
        return redirect('/wall')
    else: 
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL('wall')
    query = "SELECT * FROM users WHERE email = %(em)s;"
    data = {
        "em" : request.form['e_log'],
    }
    log = mysql.query_db(query, data)
    if len(log) > 0:
        if bcrypt.check_password_hash(log[0]['password'], request.form['p_log']):
            session['user'] = log
            print(session['user'])
            return redirect('/wall')
        else: 
            flash("Incorrect Login", 'loerror')
            return redirect('/')


@app.route('/logout')
def logout():
    if 'user' in session:
        session['user'] = None
    print(session['user']) 
    return redirect('/')


@app.route('/wall')
def wall():
    print(session['user'][0]['id'])
    mysql = connectToMySQL('wall')
    query = ("SELECT messages.id, messages.message, messages.rec_id, messages.sender_id, users.first_name, TIMESTAMPDIFF(HOUR, messages.created_at , NOW()) AS TIMESTAMP FROM messages JOIN users ON messages.sender_id = users.id WHERE messages.rec_id = %(user)s;")
    data = {
        "user" : session['user'][0]['id']
    }
    rec_messes = mysql.query_db(query, data)
    print(rec_messes)

    mysql2 = connectToMySQL('wall')
    query = ('SELECT * FROM users WHERE id != %(user)s;')
    data = {
        "user" : session['user'][0]['id']
    }   
    buddies = mysql2.query_db(query,data)

    mysql3 = connectToMySQL('wall')
    query = ('SELECT messages.rec_id, IFNULL(COUNT(*), 0) AS count1 FROM messages LEFT JOIN users ON users.id = messages.rec_id WHERE messages.rec_id = %(user)s;')
    data = {
        "user" : session['user'][0]['id']
    }
    sent_mess = mysql3.query_db(query,data)

    mysql4 = connectToMySQL('wall')
    query = ('SELECT messages.sender_id, IFNULL(COUNT(*), 0) AS count FROM messages LEFT JOIN users ON users.id = messages.sender_id WHERE messages.sender_id = %(user)s;')
    data = {
        "user" : session['user'][0]['id']
    }
    count = mysql4.query_db(query,data)



    return render_template('wall.html', rec_messes = rec_messes, buddies = buddies, sent_mess = sent_mess, count = count)


@app.route('/message', methods=['POST'])
def message():
    mysql = connectToMySQL('wall')
    query = "INSERT INTO messages (rec_id, message, sender_id) VALUES (%(rec_id)s, %(message)s,%(sender_id)s);"
    data = {
        "sender_id" : session['user'][0]['id'],
        "rec_id" : request.form['rec_id'],
        "message" : request.form['message']
    }
    mess = mysql.query_db(query, data)
    return redirect('/wall')


@app.route('/trash/<id>')
def trash(id):
    mysql = connectToMySQL('wall')
    query = "DELETE FROM messages WHERE messages.id = %(id)s"
    data = {
        "id" : id
    }
    mysql.query_db(query,data)
    return redirect('/wall')



if __name__ == '__main__':
    app.run(debug=True) 
