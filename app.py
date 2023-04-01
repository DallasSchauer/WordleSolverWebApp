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
        words = request.form['words'].split('\n')
        args = []

        for w in words:
            if len(w) == 6:
                print("ADDING " + w[:5])
                r = w[:5] 
                r += '\n'
                args.append(r)

        return quordle.play(args)

    else:
        words = request.args.get('words').split('\n')

        args = []

        for w in words:
            if len(w) == 6:
                print("ADDING " + w[:5])
                r = w[:5] 
                r += '\n'
                args.append(r)

        return quordle.play(args)
    


@app.route('/pickWords/<words>')
def defineWords(words):
    res = words.split("+")

    ret = []
    for n in res:
        if len(n) == 5:
            ret.append(n)

    return quordle.play(ret)


if __name__ == "__main__":
    app.run(debug=False)