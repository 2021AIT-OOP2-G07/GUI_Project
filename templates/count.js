var count = 3;
    var countdown = function(){
        document.getElementById('timer').testContent = count.toString();
        console.log(count--);
        var id = setTimeout(countdown, 1000);
        if(count < 0){
            clearTimeout(id);
        }
    }
    countdown();

