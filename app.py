from flask import Flask, render_template, url_for

import quordle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<words>')
def defineWords(words):
    res = words.split("+")

    ret = ""
    for n in res:
        ret += n
        ret += ", "

    return quordle.play()


if __name__ == "__main__":
    app.run(debug=True)