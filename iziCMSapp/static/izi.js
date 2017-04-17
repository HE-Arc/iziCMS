/*
    C'est le script qui sera éxécuté directement sur la page à éditer en utilisant le bookmarklet
*/
function izi(){
    // pour l'instant, simple redirection sur iziCMS
    window.location = "http://127.0.0.1:8000/izi_edit/" + location.hostname + "/" + location.pathname
}