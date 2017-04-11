//document.getElementById('edition').style.visibility = 'visible'

var quill = new Quill('#iziCMSeditor', {
    theme: 'snow',
    modules: {
        toolbar: [
            [{ 'header': [1, 2, 3, false] }],
            ['bold', 'italic', 'underline', 'strike'],
            ['link','image','video','formula'],
            [{ 'font': [] }],
            [{ 'align': [] }],
            [{ 'color': [] }, { 'background': [] }],
            ['blockquote', 'code-block'],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            [{ 'script': 'sub'}, { 'script': 'super' }],
            [{ 'indent': '-1'}, { 'indent': '+1' }],
            ['clean']
        ]
      }
    });

document.querySelector("form").onsubmit = function(){
    document.getElementById("editContent").value = document.querySelector(".ql-editor").innerHTML;
};
