function addEditor(num){
    var quill = new Quill('#iziCMSeditor'+num, {
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
        for(var i = 0; i <= num; i++){
            document.getElementById("editContent"+i).value = document.querySelectorAll(".ql-editor")[i].innerHTML;
        }
    };
}
