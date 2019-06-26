from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def root():
    return render_template("root.html", times=4)
@app.route('/checker/<x>')
def manyrows(x):
    return render_template("manyrows.html", times= int(int(x)/2))


if __name__=="__main__":
    app.run(debug=True)