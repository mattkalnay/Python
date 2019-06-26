def wall():
    print(session['user'][0]['id'])
    mysql = connectToMySQL('wall')
    query = ("SELECT * FROM users JOIN messages ON messages.rec_id = users.id WHERE messages.rec_id = %(user)s;")
    data = {
        "user" : session['user'][0]['id']
    }
    rec_messes = mysql.query_db(query)
    print(rec_messes)