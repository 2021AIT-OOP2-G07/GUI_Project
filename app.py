# -*- coding: utf-8 -*-
import imp
from flask import Flask, request, render_template
from ScoreCalculator import ScoreCalculator
from pymongo import MongoClient
from DetaBase import Mdb
from flask import Flask, request, render_template, url_for
from flask import url_for, \
    abort, render_template, flash
from flask import Flask, request, url_for, \
    abort, render_template, flash
from werkzeug.utils import secure_filename

import os


app = Flask(__name__)
UPLOAD_FOLDER = './static/image/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 1. ゲームトップ


@app.route('/')
def Home():
    return render_template('home.html')

# 2.名前入力・モード選択画面(指定1枚orランダム3枚)


@app.route('/select')
def Select():
    return render_template('select.html')

# 練習モードトップ画面


@app.route('/select/practice', methods=["POST"])
def Practice():
    return render_template('practice.html')

# ランダムモードトップ画面


@app.route('/select/random', methods=["POST"])
def Random():
    return render_template('random.html')

# 図鑑


@app.route('/dictionary')
def Dictionary():
    return render_template('dictionary.html')

# 練習モードリザルト画面


@app.route('/select/practice/confirm', methods=["POST"])
def P_cnf():
    return render_template('prac-confirm.html')


@app.route('/select/practice/pResult', methods=["POST"])
# targetImage:比較対象の画像
# baseImage:比較元の画像
# name:使用者の名前
# score：スコア
# ranking：このスコアのランキング
def ResultP():
    baseImage = request.form.get("basepng", None)
    name = request.form.get("name", None)
    SC = ScoreCalculator()
    ret = SC.getScore('targetImage', "baaseImage")
    score = ret['score']['sum']
    Mdb.P_reg(name, score)
    ranking = Mdb.P_result(score)
    if request.method == 'POST':
        # ファイルを読み込む
        img_file = request.files['img_file']

        # ファイル名を取得する
        filename = secure_filename(img_file.filename)

        # 画像のアップロード先URLを生成する
        img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 画像をアップロード先に保存する
        img_file.save(img_url)
    return render_template('pResult.html',
                           targetImage=img_url,
                           baseImage=baseImage,
                           name=name,
                           score=score,
                           ranking=ranking
                           )

# ランダムモードリザルト画面


@app.route('/selct/random/rResult')
def ResultR():
    targetImage1 = request.form.get("targetpng1", None)
    baseImage1 = request.form.get("basepng1", None)
    targetImage2 = request.form.get("targetpng2", None)
    baseImage2 = request.form.get("basepng2", None)
    targetImage3 = request.form.get("targetpng3", None)
    baseImage3 = request.form.get("basepng3", None)
    name = request.form.get("name", None)
    SC = ScoreCalculator()
    ret1 = SC.getScore(targetImage1, baseImage1)
    ret2 = SC.getScore(targetImage2, baseImage2)
    ret3 = SC.getScore(targetImage3, baseImage3)

    score = ret1['score']['sum'] + ret2['score']['sum'] + ret3['score']['sum']

    Mdb.R_reg(name, score)
    ranking = Mdb.R_result(score)
    return render_template('rResult.html',
                           targetImage1=targetImage1,
                           baseImage1=baseImage1,
                           argetImage2=targetImage2,
                           baseImage2=baseImage2,
                           argetImage3=targetImage3,
                           baseImage3=baseImage3,
                           name=name,
                           score=score,
                           ranking=ranking)


# ランキング画面

#  practice_ranking = list型の配列

@app.route('/ranking')
def Ranking():
    practice_ranking = Mdb.P_ranking()
    return render_template('ranking.html',
                           practice_ranking=practice_ranking)

# 画像アップロード画面


@app.route('/upload', methods=['POST'])
def upload():

    # 画像をWEBページに表示する
    return render_template('Presult.html', result_img=img_url)


if __name__ == '__main__':
    app.run()
