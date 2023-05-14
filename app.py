from flask import Flask, render_template, url_for, request, redirect

import quordle
import AI

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
    
@app.route('/multigame', methods = ['POST', 'GET'])
def playOriginal():
    answers = []
    with open('data/valid_answers.txt') as answersText:
        answers = answersText.readlines()
    res = quordle.PlayManyGames(100, answers, 4, AI.CommonLetterSpots)
    xValues = []
    yValues = []

    for n in res[4]:
        xValues.append(n[0])
        yValues.append(n[1])

    return render_template('multigame.html', gameResults = res, x = xValues, y = yValues)

@app.route('/multigameSimulation', methods = ['POST', 'GET'])
def multigameSim():
    numWords = int(request.form['numWords'])
    numGames = int(request.form['numGames'])
    strategy = int(request.form['strategy'])

    argStrat = AI.AI
    stratStr = "Random"
    match strategy:
        case 2:
            argStrat = AI.UniqueWords
            stratStr = "Unique Words"
        case 3:
            argStrat = AI.Scrabble
            stratStr = "Scrabble"
        case 4:
            argStrat = AI.CommonLetters
            stratStr = "Common Letters"
        case 5:
            argStrat = AI.CommonLetterSpots
            stratStr = "Common Letter Spots"
        case 6:
            argStrat = AI.Entropy
            stratStr = "Static Starters -to-> Entropy"
        case _:
            argStrat = AI.AI
            stratStr = "Random"
    
    with open('data/valid_answers.txt') as answersText:
        answers = answersText.readlines()
    res = quordle.PlayManyGames(numGames, answers, numWords, argStrat)

    xValues = []
    yValues = []

    for n in res[4]:
        xValues.append(n[0])
        yValues.append(n[1])

    return render_template('multigame.html', gameResults = res, x = xValues, y = yValues,
                           webNumWords = numWords, webNumGames = numGames, webStrategy = stratStr)

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