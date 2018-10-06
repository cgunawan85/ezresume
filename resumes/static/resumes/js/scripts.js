$(document).on('click', '.confirm-delete', function(){
    return confirm('Are you sure you want to delete this resume?');
});

setTimeout(function(){
  $('.messages').remove();
}, 4000);

$(function() {
    $('.date-picker').datepicker()
});

function overlay() {
	el = document.getElementById("overlay");
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}