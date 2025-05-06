let i = 0;

let timeSign = setInterval(function(){
    console.log(++i);
    if(i == 5)
        clearInterval(timeSign);
}, 2000);

console.log(100);