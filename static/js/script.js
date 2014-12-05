$(function() {
	var currDate = new Date();

    date = currDate.toISOString().match(/(\d{4}\-\d{2}\-\d{2})/);
    $('input[name=date]').val(date[1]);
    console.log(date)

    var hr = currDate.getHours() < 10? "0" + currDate.getHours(): currDate.getHours();
    var min = currDate.getMinutes() < 10? "0" + currDate.getMinutes(): currDate.getMinutes();
    var sec = currDate.getSeconds() < 10? "0" + currDate.getSeconds(): currDate.getSeconds();
    startTime = hr + ":" + min + ":" + sec;
    endTime = (hr+1) + ":" + min + ":" + sec;
    $('ride-start-time').val(startTime);
    console.log($('ride-start-time').val());
    console.log(startTime);
    console.log(endTime);

    
});

$(document).ready(function(){
  $('#feedback').click(function(){
    $(this).fadeOut();
  });
});
