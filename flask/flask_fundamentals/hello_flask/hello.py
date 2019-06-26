from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/dojo')
def dojo():
    return 'Dojo!'
@app.route('/say/<name>')
def say_name(name):
    return f"Hi {name}!"
@app.route('/repeat/<num>/<word>')
def repeat_word(num, word):
    z = f"{str(word)}" 
    return z * int(num) 
if __name__=="__main__":
    app.run(debug=True)
