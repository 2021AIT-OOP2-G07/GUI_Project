# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from datetime import datetime
from ScoreCalculator import ScoreCalculator

app = Flask(__name__)
# 1. ゲームトップ


@app.route('/')
def Home():
    return render_template('home.html')

# 2.名前入力・モード選択画面(指定1枚orランダム3枚)


@app.route('/selct')
def Select():
    return render_template('select.html')


@app.route('/practice')
def Practice():
    return render_template('practice.html')


@app.route('/random')
def Random():
    return render_template('random.html')


@app.route('/dictionary')
def Dictionary():
    return render_template('dictionary.html')


@app.route('/pResult')
def ResultP():
    SC = ScoreCalculator()
    ret = SC.getScore("a", "b")
    score = ret['score']['sum']
    return render_template('ran-count.html',
                           score
                           )


@app.route('/rResult')
def ResultR():
    return render_template('rResult.html')


@app.route('/ranking')
def Ranking():
    return render_template('ranking.html')


if __name__ == '__main__':
    app.run()
