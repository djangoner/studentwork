function showAlert(msg, cls='info', timeout=5000){
  $('.alerts-container').append('<div id="alertdiv" class="alert alert-lg alert-' +  cls + '"><a class="close" data-dismiss="alert">×</a><span>'+msg+'</span></div>')
  setTimeout(function() { // this will automatically close the alert and remove this if the users doesnt close it in 5 secs
    $("#alertdiv").remove();
  }, timeout);
}