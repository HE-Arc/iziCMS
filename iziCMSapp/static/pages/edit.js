var quill = new Quill('#iziCMSeditor', {theme: 'snow'});

document.querySelector("form").onsubmit = function(){
  document.getElementById("pageContent").value = document.querySelector(".ql-editor").innerHTML;
};