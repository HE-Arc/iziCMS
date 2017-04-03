// http://mrcoles.com/bookmarklet/ pour générer le bookmarklet

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
