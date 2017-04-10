// Ceci est le code éxécuté par le bookmarklet
// Il ne fait que charger le "vrai" code sur iziCMS
// Comme ça on n'a pas besoin de changer le bookmarklet à chaque modif

(function() {
    function callback() {
        izi();
    }
    var s = document.createElement("script");
    s.src = "http://127.0.0.1:8000/static/izi.js";
    if (s.addEventListener) {
        s.addEventListener("load", callback, false)
    } else if (s.readyState) {
        s.onreadystatechange = callback
    }
    document.head.appendChild(s);
})()

// en une ligne :
/*
javascript:(function()%7B(function()%20%7Bfunction%20callback()%20%7Bizi()%3B%7Dvar%20s%20%3D%20document.createElement(%22script%22)%3Bs.src%20%3D%20%22http%3A%2F%2F127.0.0.1%3A8000%2Fstatic%2Fizi.js%22%3Bif%20(s.addEventListener)%20%7Bs.addEventListener(%22load%22%2C%20callback%2C%20false)%7D%20else%20if%20(s.readyState)%20%7Bs.onreadystatechange%20%3D%20callback%7Ddocument.head.appendChild(s)%3B%7D)()%7D)()
 */
// http://mrcoles.com/bookmarklet/ pour générer le bookmarklet