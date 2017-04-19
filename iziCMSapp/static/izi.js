/*
    C'est le script qui sera éxécuté directement sur la page à éditer en utilisant le bookmarklet
*/
function izi(){
    // pour l'instant, simple redirection sur iziCMS
    window.location = "https://izicms.srvz-webapp.he-arc.ch/izi_edit/" + location.hostname + "/" + location.pathname
}
