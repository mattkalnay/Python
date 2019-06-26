from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)

@app.route('/')
def index():
    if not in session:
        session['gold'] = 0

    return render_template('index.html')

@app.route('/process_money', methods=['POST'])
def process_money():


    redirect ('/')







if __name__ == '__main__':
    app.run(debug=True)