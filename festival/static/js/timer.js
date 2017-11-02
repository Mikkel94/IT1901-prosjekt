window.document.body.addEventListener('load', x);
var seconds = 6;
var x = setInterval(function () {
    seconds--;
    document.getElementById("timer").innerHTML = seconds + "s";
    if (seconds <= 0) {
        clearInterval(x);
        document.getElementById("timer").innerHTML = "REDIRECTING";
    }
}, 1000);