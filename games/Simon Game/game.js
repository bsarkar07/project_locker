var buttonColors = ["red","blue","green","yellow"];
var gamePattern = [];
var userPattern = [];
var soundPath = "sounds/";
var level = 0;
var count = -1;
var gameOver = 0;
var clickTime = 0;

function randNum(){
    var rand = Math.floor(Math.random()*10)%4;
    return rand;
}


function flash(element){
    element.fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100);  
}


function playAudio(file){
    let audio = new Audio(file);
    audio.play();
}


function handleClick(){

    let btn = $(this).attr("id");
    let file = '';
    let title = $("#level-title");
    count++;
    
    if(count >= gamePattern.length || gameOver)
        return;
    
    if (gamePattern[count] === btn){
        file = soundPath+btn+".mp3";
    }
    else{
        file = soundPath+"wrong"+".mp3";
        title.text("Game Over! Reload to start New Game!");
        gameOver = 1;
        playAudio(file);
        flash($(this));
        return;
    }

    playAudio(file);

    flash($(this));

    if(count == gamePattern.length-1){
        title = $("#level-title");
        title.text("Correct! Press any key to start Level: "+ (level+1));
        clickTime = 0;
    }
}


function handleKeyDown(){
    if (gameOver || clickTime)
        return;

    count = -1;
    let title = $("#level-title");
    title.text("Level: "+ (++level));
    let i = 0;
    gamePattern = [];

    let timeSign = setInterval(function(){
        if(i >= level-1)
            clearInterval(timeSign);

        gamePattern.push(buttonColors[randNum()]);

        file = "sounds/"+gamePattern[i]+".mp3";
        playAudio(file);
        
        let btn = $("#"+gamePattern[i]);
        flash(btn);
        i++;

    }, 1000);

    clickTime = 1;
}


$(".btn").on("click", handleClick);
$(document).on("keydown", handleKeyDown)
