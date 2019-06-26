from flask import Flask, render_template, request, redirect, session
import random 
app = Flask(__name__)
app.secret_key = 'shh_secret'


@app.route('/')
def index():
    def rand():
        if rng not in session:
            session['rng'] = random.randint(1,100)
    print("The answer is:", session['rng'])
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def guess():
    guess = int(request.form['guess'])
    print("Your guess is:", guess) 
    def rere(num1, num2):
        if (int(num1) < int(num2)):
            return "Too Low!"
        if (int(num1) > int(num2)):
            return "Too High!"
        if (int(num1) == int(num2)):
            return "Just Right!"
    x = rere(guess, session['rng'])
    print(guess, session['rng'], x)
    return render_template('result.html', x_template = x)

@app.route('/restart', methods=['POST'])
def restart():
    session['rng'] = random.randint(1,100) 
    return render_template('index.html')



app.run(debug=True)