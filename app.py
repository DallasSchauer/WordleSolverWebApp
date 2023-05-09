from flask import Flask, render_template, url_for, request, redirect

import quordle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))


@app.route('/play')
def randomWords():
    return quordle.play(quordle.PickRandomWords(4))

@app.route('/pick', methods = ['POST', 'GET'])
def defineSubmit():
    if request.method == 'POST':
        answers = []
        with open('data/valid_answers.txt') as answersText:
            answers = answersText.readlines()

        words = request.form['words'].split('\n')
        args = []

        for w in words:
            if len(w) == 6 :
                r = w[:5].lower()
                r += '\n'
                print("ADDING " + r)
                if r in answers:
                    print(r + " in answers")
                    args.append(r)
                else:
                    print(r + " NOT in answers")
            else:
                print(w + " NOT 5 letters.")

        res = quordle.play(args)
        return render_template('game.html', results = res, numGuesses = len(res[0]), 
                               hiddenWords = args)

    else:
        answers = []
        with open('data/valid_answers.txt') as answersText:
            answers = answersText.readlines()

        words = request.form['words'].split('\n')
        args = []

        for w in words:
            if len(w) == 6 and w in answers:
                print("ADDING " + w[:5])
                r = w[:5].lower()
                r += '\n'
                args.append(r)

        res = quordle.play(args)
        return render_template('game.html', results = res, numGuesses = len(res[0]), 
                               hiddenWords = args)
    
@app.route('/multigame')
def playOriginal():
    res = quordle.playOriginal()
    return render_template('multigame.html', gameResults = res)

@app.route('/pickWords/<words>')
def defineWords(words):
    res = words.split("+")

    ret = []
    for n in res:
        if len(n) == 5:
            ret.append(n)

    return quordle.play(ret)


if __name__ == "__main__":
    print("HELLO")
    app.run(debug=True)