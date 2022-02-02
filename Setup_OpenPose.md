OpenPoseリポジトリ
https://github.com/CMU-Perceptual-Computing-Lab/openpose

インストール手順
https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md#problems-and-errors-installing-openpose

インストール手順和訳
https://qiita.com/westtail/items/06f11bbc9c73b186badf

<<<<<<< Updated upstream
ScoreSalculatorでは以下のディレクトリ構成を想定しています
GitHub  -   GUI_PROJECT -   ScoreCalculator.py
        -   openpose
=======
その後の手順---
ターミナルにて
brew install wget を実行
openpose/models に移動
sudo bash models/getModels.sh を実行

ファインダーにて
openpose/build/pose/coco 配下の pose_iter_440000.caffemodel を
openpose/models/pose/coco 配下にコピー

ScoreCalculator.pyを実行
実行結果にエラーがなければ成功

---
ScoreCalculatorでは以下のディレクトリ構成を想定しています
<p>
GitHub  -   GUI_PROJECT -   ScoreCalculator.py<br>
&nbsp;　　　　-   openpose

>>>>>>> Stashed changes
