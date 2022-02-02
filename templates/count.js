var PassSec=10;   // 秒数カウント用変数
 
    // 繰り返し処理の中身
    function showPassage() {
        PassSec--;   // カウントアップ
        var msg = "撮影開始まで残り " + PassSec + "秒！。";   // 表示文作成
        document.getElementById("timer").innerHTML = msg;   // 表示更新
    }
    // 繰り返し処理の開始
    function startShowing() {
        PassageID = setInterval('showPassage()',1000);
    }
    startShowing();

