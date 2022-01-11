class ScoreCalculator:
    # コンストラクタ 比較対象，比較元の画像のディレクトリのパスを設定
    # 引数
    ## targetImagePath  比較対象の画像が保存されているディレクトリのパス    デフォルトはクラスファイルと同じディレクトリ
    ## baseImagePath    比較元の画像が保存されているディレクトリのパス      デフォルトはクラスファイルと同じディレクトリ
    # 戻り値 None
    def __init__(self, targetImagePath = '', baseImagePath = ''):
        self.targetImagePath = targetImagePath
        self.baseImagePath= baseImagePath

    # スコアを返すメソッド
    # 引数
    ## targetImageName  比較対象の画像のファイル名  self.targetImagePathが示すディレクトリに配置されている
    ## baseImageName    比較元の画像のファイル名    self.baseImagePathが示すディレクトリに配置されている
    # 戻り値
    ## このメソッド内の変数retを確認してください
    def getScore(self, targetImageName, baseImageName):
        # スコアを計算する処理

        # 戻り値 辞書型
        ## 'score'と'error'のどちらかが定義されている
        # スコア計算ができた場合
        if (True):
            ret = {
                # 'score' 辞書型 スコア計算ができた場合のみ定義される
                'score' : {
                    # 'sum' 整数型 全体のスコア スコアが高いほど一致度が高い 最小値(完全一致の場合)は0 最大値は1100
                    'sum' : 1100,
                    # 'detail 辞書型 各部位ごとのスコア それぞれ整数型で0から100 全部足すと'sum'になる 多分使わない
                    'detail' : {
                        # 首
                        'neck' : 100,
                        # 右肩
                        'rightShoulder' : 100,
                        # 右腕
                        'rightArm' : 100,
                        # 右肘
                        'rightElbow' : 100,
                        # 左肩
                        'leftShoulder' : 100,
                        # 左腕
                        'leftArm' : 100,
                        # 左肘
                        'leftElbow' : 100,
                        # 右足
                        'rightLeg' : 100,
                        # 右膝
                        'rightKnee' : 100,
                        # 左足
                        'leftLeg' : 100,
                        # 左膝
                        'leftKnee' : 100
                    }
                }
            }
        # スコア計算ができなかった場合
        else:
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

    # 比較対象の画像にエラーがないか判定
    # 引数
    ## targetImageName  比較対象の画像のファイル名  self.targetImagePathが示すディレクトリに配置されている
    # 戻り値
    ## checkImage内の変数retを確認してください
    def checkTarget(self, targetImageName):
        return self.checkImage(self.targetImagePath, targetImageName)

    # 比較元の画像にエラーがないか判定
    # 引数
    ## baseImageName    比較元の画像のファイル名    self.baseImagePathが示すディレクトリに配置されている
    # 戻り値
    ## checkImage内の変数retを確認してください
    def checkBase(self, baseImageName):
        return self.checkImage(self.baseImagePath, baseImageName)
    
if __name__ == '__main__':
    # デバッグ用
    print('Hello, World!')