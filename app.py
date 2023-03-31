from flask import Flask, render_template, url_for

import quordle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/play')
def randomWords():
    return quordle.play(quordle.PickRandomWords(4))

@app.route('/pickWords/<words>')
def defineWords(words):
    res = words.split("+")
    print("Length: " + str(len(res)))
    return quordle.play(res)


if __name__ == "__main__":
    app.run(debug=False)