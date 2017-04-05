//document.getElementById('edition').style.visibility = 'visible'

var quill = new Quill('#iziCMSeditor', {
    theme: 'snow',
    modules: {
        toolbar: true
      }
    });


//document.getElementsByClassName('ql-toolbar ql-snow').style.visibility = 'visible'

document.querySelector("form").onsubmit = function(){
    //document.getElementById("edition").innerHTML  = document.querySelector(".ql-editor").innerHTML;
    //document.getElementById("pageContent").value = document.getElementById("iziCMSeditor").innerHTML;
    document.getElementById("editContent").value = document.querySelector(".ql-editor").innerHTML;
};
