import cv2
import sys
import numpy as np
from numpy import linalg as LA

class ScoreCalculator:
    # コンストラクタ 比較対象・比較元の画像のディレクトリのパスを設定 ライブラリのインポート
    # 引数
    ## targetImagePath  比較対象の画像が保存されているディレクトリのパス    デフォルトはクラスファイルと同じディレクトリ
    ## baseImagePath    比較元の画像が保存されているディレクトリのパス      デフォルトはクラスファイルと同じディレクトリ
    # 戻り値 None
    def __init__(self, targetImagePath = '', baseImagePath = ''):
        self.targetImagePath = targetImagePath
        self.baseImagePath = baseImagePath

        # OpenPoseのインポート
        try:
            # OpenPoseのPythonライブラリを指定(openpose/build/python)
            sys.path.append('../openpose/build/python')
            from openpose import pyopenpose as op
            self.op = op
        except ImportError as e:
            print('Error: OpenPose library could not be found.')


    # 未完成    (正しい引数，正しい画像を指定すれば動きます)
    # スコアを返すメソッド
    # 引数
    ## targetImageName  比較対象の画像のファイル名  self.targetImagePathが示すディレクトリに配置されている
    ## baseImageName    比較元の画像のファイル名    self.baseImagePathが示すディレクトリに配置されている
    # 戻り値
    ## このメソッド内の変数retを確認してください
    def getScore(self, targetImageName, baseImageName):
        # スコアを計算する処理

        # 関節の位置をOpenPoseで推定
        targetDatum = self.getDatum(self.targetImagePath + targetImageName)
        baseDatum = self.getDatum(self.baseImagePath + baseImageName)

        # 関節の角度を求める
        targetAngles = self.calcAngles(targetDatum.poseKeypoints)
        baseAngles = self.calcAngles(baseDatum.poseKeypoints)

        ret = dict()
        ret['score'] = {'sum': 0, 'detail' : {
            # 首
            'neck' : 0,
            # 右肩
            'rightShoulder' : 0,
            # 右腕
            'rightArm' : 0,
            # 右肘
            'rightElbow' : 0,
            # 左肩
            'leftShoulder' : 0,
            # 左腕
            'leftArm' : 0,
            # 左肘
            'leftElbow' : 0,
            # 右足
            'rightLeg' : 0,
            # 右膝
            'rightKnee' : 0,
            # 左足
            'leftLeg' : 0,
            # 左膝
            'leftKnee' : 0
        }}
        
        for key in ret['score']['detail'].keys():
            score = 100 - round(abs(targetAngles[key] - baseAngles[key]))
            ret['score']['detail'][key] = score if score >= 0 else 0
            ret['score']['sum'] += ret['score']['detail'][key]

        # スコア計算ができなかった場合
        if (False):
            ret = {
                # 'error' 比較対象，比較元の画像に関するエラー スコア計算ができなかった場合のみ定義される
                ## 'error'が定義されていれば，'targetErrors'と'baseErrors'のどちらかは必ず定義される(両方定義されることもある)
                'error' : {
                    # 'targetErrors' 比較対象の画像に関するエラー 比較対象の画像に関するエラーがあったときのみ定義される
                    'targetErrors' : [
                        '右肩が認識できません', '左膝が認識できません'
                    ],
                    # 'baseErrors' 比較元の画像に関するエラー 比較元の画像に関するエラーがあったときのみ定義される
                    'baseErrors' : [
                        '複数人写り込んでいます'
                    ]
                }
            }

        return ret

    # 未実装
    # 画像を問題なく骨格推定できるか判定
    # 引数
    ## imagePath  画像のパス名
    ## imageName  画像のファイル名  imagePathが示すディレクトリに配置されている
    # 戻り値
    ## このメソッド内の変数retを確認してください
    def checkImage(self, imagePath, ImageName):
        if (True) : 
            ret = {
                'isFine' : True
            }
        else :
            ret = {
                'isFine' : False,
                'errors' : [
                    '右肩が認識できません'
                ]
            }
        return ret

    # 未実装
    # 比較対象の画像にエラーがないか判定
    # 引数
    ## targetImageName  比較対象の画像のファイル名  self.targetImagePathが示すディレクトリに配置されている
    # 戻り値
    ## checkImage内の変数retを確認してください
    def checkTarget(self, targetImageName):
        return self.checkImage(self.targetImagePath, targetImageName)

    # 未実装
    # 比較元の画像にエラーがないか判定
    # 引数
    ## baseImageName    比較元の画像のファイル名    self.baseImagePathが示すディレクトリに配置されている
    # 戻り値
    ## checkImage内の変数retを確認してください
    def checkBase(self, baseImageName):
        return self.checkImage(self.baseImagePath, baseImageName)
    
    # 画像から関節の座標を取得する
    # 引数
    ## imagePath 対象画像の完全パス
    # 戻り値
    ## Datum型 https://cmu-perceptual-computing-lab.github.io/openpose/web/html/doc/structop_1_1_datum.html
    def getDatum(self, imagePath):
        params = dict()
        params['model_folder'] = '../openpose/models/'
        params['model_pose'] = 'COCO'

        op = self.op
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        datum = op.Datum()
        imageToProcess = cv2.imread(imagePath)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        return datum

    # 関節ごとの角度を求める
    def calcAngles(self, keypoints):
        # 各部位をベクトルとして取り出す
        vector = {
            # 首
            'neck' : np.array([keypoints[0][0][0] - keypoints[0][1][0], keypoints[0][0][1] - keypoints[0][1][1]]),
            # 右肩
            'rightShoulder' : np.array([keypoints[0][1][0] - keypoints[0][2][0], keypoints[0][1][1] - keypoints[0][2][1]]),
            # 右上腕
            'rightUpperArm' : np.array([keypoints[0][2][0] - keypoints[0][3][0], keypoints[0][2][1] - keypoints[0][3][1]]),
            # 右前腕
            'rightForearm' : np.array([keypoints[0][3][0] - keypoints[0][4][0], keypoints[0][3][1] - keypoints[0][4][1]]),
            # 左肩
            'leftShoulder' : np.array([keypoints[0][1][0] - keypoints[0][5][0], keypoints[0][1][1] - keypoints[0][5][1]]),
            # 左上腕
            'leftUpperArm' : np.array([keypoints[0][5][0] - keypoints[0][6][0], keypoints[0][5][1] - keypoints[0][6][1]]),
            # 左前腕
            'leftForearm' : np.array([keypoints[0][6][0] - keypoints[0][7][0], keypoints[0][6][1] - keypoints[0][7][1]]),
            # 胸から右腿付け根
            'chestToRightLeg' : np.array([keypoints[0][1][0] - keypoints[0][8][0], keypoints[0][1][1] - keypoints[0][8][1]]),
            # 右上腿
            'rightUpperLeg' : np.array([keypoints[0][8][0] - keypoints[0][9][0], keypoints[0][8][1] - keypoints[0][9][1]]),
            # 右下腿
            'rightLowerLeg' : np.array([keypoints[0][9][0] - keypoints[0][10][0], keypoints[0][9][1] - keypoints[0][10][1]]),
            # 胸から左腿付け根
            'chestToLeftLeg' : np.array([keypoints[0][1][0] - keypoints[0][11][0], keypoints[0][1][1] - keypoints[0][11][1]]),
            # 左上腿
            'leftUpperLeg' : np.array([keypoints[0][11][0] - keypoints[0][12][0], keypoints[0][11][1] - keypoints[0][12][1]]),
            # 左下腿
            'leftLowerLeg' : np.array([keypoints[0][12][0] - keypoints[0][13][0], keypoints[0][12][1] - keypoints[0][13][1]])
        }
        
        # ベクトルから角度をとる
        angle = {
            # 首
            'neck' : self.vectorToAngle(np.array([1, 0]), vector['neck']),
            # 右肩
            'rightShoulder' : self.vectorToAngle(np.array([1, 0]), vector['rightShoulder']),
            # 右腕
            'rightArm' : self.vectorToAngle(vector['rightShoulder'], vector['rightUpperArm']),
            # 右肘
            'rightElbow' : self.vectorToAngle(vector['rightUpperArm'], vector['rightForearm']),
            # 左肩
            'leftShoulder' : self.vectorToAngle(np.array([1, 0]), vector['leftShoulder']),
            # 左腕
            'leftArm' : self.vectorToAngle(vector['leftShoulder'], vector['leftUpperArm']),
            # 左肘
            'leftElbow' : self.vectorToAngle(vector['leftUpperArm'], vector['leftForearm']),
            # 右足
            'rightLeg' : self.vectorToAngle(vector['chestToRightLeg'], vector['rightUpperLeg']),
            # 右膝
            'rightKnee' : self.vectorToAngle(vector['rightUpperLeg'], vector['rightLowerLeg']),
            # 左足
            'leftLeg' : self.vectorToAngle(vector['chestToLeftLeg'], vector['leftUpperLeg']),
            # 左膝
            'leftKnee' : self.vectorToAngle(vector['leftUpperLeg'], vector['leftLowerLeg'])
        }

        return angle

    # 2つのベクトルから角度を求める
    def vectorToAngle(self, v1, v2):
        i = np.inner(v1, v2)
        n = LA.norm(v1) * LA.norm(v2)
        c = i / n
        a = np.rad2deg(np.arccos(np.clip(c, -1.0, 1.0)))
        return a


if __name__ == '__main__':
    # デバッグ用
    scoreCalculator = ScoreCalculator('test_img/', 'test_img/')
    print(scoreCalculator.getScore('yogaMale.jpg','yogaFemale.jpg')['score'])
    