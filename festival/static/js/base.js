/*----- Button for å vise konsertinfo ---------*/

function concert_button(h) {
    document.getElementById("modal_" + h).style.display = "block";
    document.getElementById("modal_" + h).style.visibility = "visible";
}

function close(){
    window.alert("sometext");
    document.getElementsByClassName(modal).style.display = "none";
}

function myFunction(h) {
    var m = document.getElementById("modal_" + h);

    m.style.display = 'none';
    m.style.visibility = "hidden";

}
/*----- Ferdig button ---------*/
