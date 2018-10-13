tinymce.init({
  selector: 'textarea',
  height: 350,
  width: 500,
  menubar: false,
  plugins: [
      'advlist lists' ],
  toolbar: 'undo redo | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
  content_css: [
    '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    '//www.tinymce.com/css/codepen.min.css']
});