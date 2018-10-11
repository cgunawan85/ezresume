$(document).on('click', '.confirm-delete', function(){
    return confirm('Are you sure you want to delete this resume?');
});

setTimeout(function(){
  $('.messages').remove();
}, 4000);

$(document).on('focus', '.date-picker',function(){
    $(this).datepicker({
        todayHighlight:true,
        format:'yyyy-mm-dd',
        autoclose:true
    })
});

