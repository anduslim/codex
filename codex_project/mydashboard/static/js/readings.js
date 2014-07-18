

// document ready function
$(document).ready(function() {

  var socket = io.connect('10.217.138.166', {port: 4000});
  
  socket.on('connect', function(){
    console.log("connect");
  });
  
  var entry_el = $('#comment');
           
  socket.on('message', function(message) {
    //Escape HTML characters
    var data = message.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    	
    //Append message to the bottom of the list
    $('#comments').append('<li>'  + data + '</li>');
    window.scrollBy(0, 10000000000);
    entry_el.focus();
  });

	socket.on('reading', function (time, reading, nodeID, modality) {

		console.log("Message:" + time + ": " + reading + ", nodeID:" + nodeID + ", modality:" + modality);
	    //Append message to the bottom of the list
	    var nameOfReading = "#row_" + nodeID + "_" + modality;
      var nameOfTime = "#node_active_" + nodeID;
	    console.log("nameOfCol:" + nameOfReading);
      $(nameOfReading).toggleClass('text-glow');


	    setTimeout(function(){
	        $(nameOfReading).toggleClass('text-glow');
          $(nameOfReading + " td:nth-child(2)").text(reading);
          $(nameOfTime).text(time);
	    }, 400);
	});
                 
  entry_el.keypress(function(event){
    //When enter is pressed send input value to node server
    if(event.keyCode != 13) return;
    var modality = entry_el.val();
    var msg = entry_el.val();

    console.log("modality:" + modality);
    if(msg){
       socket.emit('send_message', modality, msg, function(data){
            console.log(data);
       });
    
    //Clear input value   
    entry_el.val('');
   }
  });


});
