from flask import Flask, request, render_template
from datetime import datetime
import datetime
import random  # ランダムデータ作成のためのライブラリ

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
    return render_template('practice')


@app.route('/random')
def Random():
    return render_template('random.html')


@app.route('/dictionary')
def Dictionary():
    return render_template('dictionary.html')


@app.route('/result')
def Result():
    return render_template('result.html')


@app.route('/ranking')
def Ranking():
    return render_template('ranking.html')


# 3.ヨガ図鑑(各ポーズの説明画面)
if __name__ == '__main__':
    app.run()
