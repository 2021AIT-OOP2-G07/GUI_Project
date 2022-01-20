# -*- coding: utf-8 -*-
import imp
from flask import Flask, request, render_template
from datetime import datetime
from ScoreCalculator import ScoreCalculator
from pymongo import MongoClient
from DetaBase import Mdb

app = Flask(__name__)
# 1. ゲームトップ


@app.route('/')
def Home():
    return render_template('home.html')

# 2.名前入力・モード選択画面(指定1枚orランダム3枚)


@app.route('/selct')
def Select():
    return render_template('select.html')

# 練習モードトップ画面


@app.route('/selct/practice', methods=["POST"])
def Practice():
    return render_template('practice.html')

# ランダムモードトップ画面


@app.route('/selct/random', methods=["POST"])
def Random():
    return render_template('random.html')

# 図鑑


@app.route('/dictionary')
def Dictionary():
    return render_template('dictionary.html')

# テスト用


def testD():
    ranking = Mdb.P_ranking(3000)
    print(ranking)

# 練習モードリアルと画面


@app.route('/selct/practice/confirm', methods=["POST"])
def P_cnf():
    return render_template('prac-confirm.html')


@app.route('/selct/practice/pResult', methods=["POST"])
# targetImage:比較対象の画像
# baseImage:比較元の画像
# name:使用者の名前
# score：スコア
# ranking：このスコアのランキング
def ResultP():
    targetImage = request.form.get("targetpng", None)
    baseImage = request.form.get("basepng", None)
    name = request.form.get("name", None)
    SC = ScoreCalculator()
    ret = SC.getScore('targetImage', "baaseImage")
    score = ret['score']['sum']
    Mdb.P_reg(name, score)
    ranking = Mdb.P_ranking(score)
    return render_template('pResult.html',
                           targetImage=targetImage,
                           baseImage=baseImage,
                           name=name,
                           score=score,
                           ranking=ranking
                           )

# ランダムモードリザルト画面


@app.route('/selct/practice/rResult')
def ResultR():
    return render_template('rResult.html')

# ランキング画面


@app.route('/ranking')
def Ranking():
    return render_template('ranking.html')


if __name__ == '__main__':
    app.run()
