import cv2
import sys
import numpy as np
from numpy import linalg as LA
import os
import warnings

class ScoreCalculator:
    # コンストラクタ 比較対象・比較元の画像のディレクトリのパスを設定 ライブラリのインポート
    # 引数
    ## targetImageDirPath  比較対象の画像が保存されているディレクトリのパス    デフォルトはクラスファイルと同じディレクトリ
    ## baseImageDirPath    比較元の画像が保存されているディレクトリのパス      デフォルトはクラスファイルと同じディレクトリ
    # 戻り値 None
    def __init__(self, targetImageDirPath = '', baseImageDirPath = ''):
        self.targetImageDirPath = targetImageDirPath
        self.baseImageDirPath = baseImageDirPath

        # 正しいパスが指定されたか確認
        ## 比較対象のディレクトリを確認
        if self.targetImageDirPath and not os.path.isdir(self.targetImageDirPath):
            print('比較対象のディレクトリが存在しません')
            raise ValueError('targetImageDirPath does not exist: targetImageDirPath is ' + str(self.targetImageDirPath))
        ## 比較元のディレクトリを確認
        if self.baseImageDirPath and not os.path.isdir(self.baseImageDirPath):
            print('比較元のディレクトリが存在しません')
            raise ValueError('baseImageDirPath does not exist: baseImageDirPath is ' + str(self.baseImageDirPath))

        # OpenPoseのインポート
        try:
            # OpenPoseのPythonライブラリを指定(openpose/build/python)
            sys.path.append('../openpose/build/python')
            from openpose import pyopenpose as op
            self.op = op
        except ImportError as e:
            print('Error: OpenPose library could not be found.')
            raise e

    # スコアを返すメソッド
    # 引数
    ## targetImageName  比較対象の画像のファイル名  self.targetImageDirPathが示すディレクトリに配置されている
    ## baseImageName    比較元の画像のファイル名    self.baseImageDirPathが示すディレクトリに配置されている
    # 戻り値
    ## dict型 詳細はこのファイルの一番下のデバッグコードをみてください
    def getScore(self, targetImageName, baseImageName):
        # 戻り値を定義
        ret = dict()

        # 画像のファイルパスを取り出す
        targetPath = self.targetImageDirPath + targetImageName
        basePath = self.baseImageDirPath + baseImageName

        # ファイルが存在しているか確認
        if not os.path.isfile(targetPath):
            print('比較対象のファイルが存在しません')
            raise ValueError('targetImage does not exist: targetPath is ' + str(targetPath))
        if not os.path.isfile(targetPath):
            print('比較元のファイルが存在しません')
            raise ValueError('baseImageDirPath does not exist: basePath is ' + str(basePath))

        # ファイルが画像か確認(拡張子のみで判断)
        root, targetExtention = os.path.splitext(targetPath)
        root, baseExtention = os.path.splitext(targetPath)
        approvedExtention = ['.jpg', '.JPG', '.png', '.PNG', '.bmp', '.BMP']

        if not targetExtention in approvedExtention:
            print('比較対象のファイルの拡張子が許可されていません ')
            raise ValueError('targetExtention is not approved: targetExtention is ' + str(targetExtention))
        if not baseExtention in approvedExtention:
            print('比較元のファイルの拡張子が許可されていません ')
            raise ValueError('baseExtention is not approved: baseExtention is ' + str(baseExtention))

        # 関節の位置をOpenPoseで推定
        targetDatum = self.getDatum(targetPath)
        baseDatum = self.getDatum(basePath)

        # 正常に骨格推定ができたか確認
        targetErrors = self.checkDatum(targetDatum)
        baseErrors = self.checkDatum(baseDatum)

        # 比較対象の画像にエラーがあった場合
        if targetErrors is not None:
            # 戻り値に比較対象の画像のエラーを追加
            ret = {'error':{'targetErrors':targetErrors}}

        # 比較元の画像にエラーがあった場合
        if baseErrors is not None:
            # 戻り値に比較元の画像のエラーを追加
            if 'error' in ret:
                ret = {'error':{'targetErrors':targetErrors, 'baseErrors':baseErrors}}
            else:
                ret = {'error':{'baseErrors':baseErrors}}

        # いずれかにエラーがあった場合
        if 'error' in ret:
            # エラーを返す
            return  ret

        # 関節の角度を求める
        targetAngles = self.calcAngles(targetDatum.poseKeypoints)
        baseAngles = self.calcAngles(baseDatum.poseKeypoints)

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
            score = 100
            if targetAngles[key] >= 0 and baseAngles[key] >= 0:
                score -= round(abs(targetAngles[key] - baseAngles[key]))
            elif targetAngles[key] >= 0 and baseAngles[key] < 0:
                score -= 180 - round(abs((targetAngles[key] - 180) - baseAngles[key]))
            elif targetAngles[key] < 0 and baseAngles[key] >= 0:
                score -= 180 - round(abs((baseAngles[key] - 180) - targetAngles[key]))
            elif targetAngles[key] < 0 and baseAngles[key] < 0:
                score -= round(abs(abs(targetAngles[key]) - abs(baseAngles[key])))
            else:
                print('Something about score calculation is wrong!')

            ret['score']['detail'][key] = score if score >= 0 else 0
            ret['score']['sum'] += ret['score']['detail'][key]

        return ret

    # 画像を問題なく骨格推定できたか判定
    # 引数 画像の骨格推定の結果 Datum型
    # 戻り値
    ## エラーなし None
    ## エラーあり エラーのリスト list(str)
    def checkDatum(self, datum):
        # 推定の信用度の閾値(これ以下であれば，推定できなかったとする)
        threshold = 0.2

        # 推定結果の，各関節の位置を取り出す
        keypoints = datum.poseKeypoints

        # エラーを格納するリスト 最後まで空であればエラーなし
        errors = []

        # 以下，エラー判定
        if keypoints is None or len(keypoints) <= 0:
            errors.append('人間を検出できませんでした')
        elif len(keypoints) > 1:
            errors.append('人間を複数人検出しました')
        else:
            if keypoints[0][0][2] < threshold:
                errors.append('顔の位置を検出できませんでした')
            if keypoints[0][1][2] < threshold:
                errors.append('胸の位置を検出できませんでした')
            if keypoints[0][2][2] < threshold:
                errors.append('右肩の位置を検出できませんでした')
            if keypoints[0][3][2] < threshold:
                errors.append('右肘の位置を検出できませんでした')
            if keypoints[0][4][2] < threshold:
                errors.append('右手の位置を検出できませんでした')
            if keypoints[0][5][2] < threshold:
                errors.append('左肩の位置を検出できませんでした')
            if keypoints[0][6][2] < threshold:
                errors.append('左肘の位置を検出できませんでした')
            if keypoints[0][7][2] < threshold:
                errors.append('左手の位置を検出できませんでした')
            if keypoints[0][8][2] < threshold:
                errors.append('右腿関節の位置を検出できませんでした')
            if keypoints[0][9][2] < threshold:
                errors.append('右膝の位置を検出できませんでした')
            if keypoints[0][10][2] < threshold:
                errors.append('右足の位置を検出できませんでした')
            if keypoints[0][11][2] < threshold:
                errors.append('左腿関節の位置を検出できませんでした')
            if keypoints[0][12][2] < threshold:
                errors.append('左膝の位置を検出できませんでした')
            if keypoints[0][13][2] < threshold:
                errors.append('左足の位置を検出できませんでした')

        # エラーが1つ以上存在した場合
        if len(errors) > 0:
            # エラーを返す
            return errors

        return None
    
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
    # v1が真上に向かっているとみて，v2が右側に向かっていればプラス，左側に向かっていればマイナスになる
    def vectorToAngle(self, v1, v2):
        # ベクトルのなす角を求める
        i = np.inner(v1, v2)
        n = LA.norm(v1) * LA.norm(v2)
        c = i / n
        a = np.rad2deg(np.arccos(np.clip(c, -1.0, 1.0)))

        # 2ベクトルを直線と見たときの傾きを求める
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            try:
                v1Slope = v1[1]/v1[0]
            except ZeroDivisionError:
                v1Slope = float('inf') if v1[1] > 0 else -float('inf')
            
            try :
                v2Slope = v2[1]/v2[0]
            except ZeroDivisionError:
                v2Slope = float('inf') if v2[1] > 0 else -float('inf')

        # 角度を，v1に対してv2が右を向いているならばプラス，左を向いているならばマイナスとする
        if v1[0] >= 0 and v1[1] >= 0:
            if v2[0] >= 0 and v2[1] >= 0:
                if v1Slope > v2Slope:
                    a = a
                else:
                    a = -a
            elif v2[0] >= 0 and v2[1] < 0:
                a = a
            elif v2[0] < 0 and v2[1] >= 0:
                a = -a
            elif v2[0] < 0 and v2[0] < 0:
                if v1Slope > v2Slope:
                    a = -a
                else:
                    a = a
            else:
                print('Something about v is wrong!')
        elif v1[0] >= 0 and v1[1] < 0:
            if v2[0] >= 0 and v2[1] >= 0:
                a = -a
            elif v2[0] >= 0 and v2[1] < 0:
                if v1Slope > v2Slope:
                    a = a
                else:
                    a = -a
            elif v2[0] < 0 and v2[1] >= 0:
                if v1Slope > v2Slope:
                    a = -a
                else:
                    a = a
            elif v2[0] < 0 and v2[0] < 0:
                a = a
            else:
                print('Something about v is wrong!')
        elif v1[0] < 0 and v1[1] >= 0:
            if v2[0] >= 0 and v2[1] >= 0:
                a = a
            elif v2[0] >= 0 and v2[1] < 0:
                if v1Slope > v2Slope:
                    a = -a
                else:
                    a = a
            elif v2[0] < 0 and v2[1] >= 0:
                if v1Slope > v2Slope:
                    a = a
                else:
                    a = -a
            elif v2[0] < 0 and v2[0] < 0:
                a = -a
            else:
                print('Something about v is wrong!')
        elif v1[0] < 0 and v1[1] < 0:
            if v2[0] >= 0 and v2[1] >= 0:
                if v1Slope > v2Slope:
                    a = -a
                else:
                    a = a
            elif v2[0] >= 0 and v2[1] < 0:
                a = -a
            elif v2[0] < 0 and v2[1] >= 0:
                a = a
            elif v2[0] < 0 and v2[0] < 0:
                if v1Slope > v2Slope:
                    a = a
                else:
                    a = -a
            else:
                print('Something about v is wrong!')
        else:
            print('Something about u is wrong!')

        return a


if __name__ == '__main__':
    # デバッグ用
    # 例外:存在しないディレクトを指定
    #scoreCalculator = ScoreCalculator('test_doggy/', 'test_kitty/')

    # 正常なディレクトリ指定
    scoreCalculator = ScoreCalculator('test_img/', 'test_img/')

    # 例外:存在しないファイルを指定
    #res = scoreCalculator.getScore('yogaDoggy.jpg', 'yogaKitty.jpg')

    # 例外:txtファイルを指定
    #res = scoreCalculator.getScore('yoga.txt', 'yogaFemale.jpg')
    
    # 正常な画像を指定
    res1 = scoreCalculator.getScore('yogaMale.jpg','yogaFemale.jpg')
    # エラーありの画像を指定
    #res2 = scoreCalculator.getScore('yogaIrust.jpg','upperBody.jpg')

    def checkResult(result):
        # 正常に推定できたか判定
        ## 正常に推定できた場合
        if 'score' in result:
            print('エラーなし')
            print("result['score']['sum']" + str(result['score']['sum']))
            print("result['score']['detail']" + str(result['score']['detail']))
        ## エラーがある場合
        elif 'error' in result:
            print('エラーあり')
            print("result['error']" + str(result['error']))
        else:
            print('プログラムにバグがあります')

        return None

    print('---')
    print('res1')
    checkResult(res1)
    print('---')
    #print('res2')
    #checkResult(res2)
    print('---')

