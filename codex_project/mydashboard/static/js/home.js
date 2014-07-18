function myCommand(component){
  var myselect = document.getElementById(component);

  switch (myselect.selectedIndex) {
  	case 1:
  		$("#Key_Command").show();
  		$("#Node_Command").hide();
      $("#genkeyBtn").show();
  		$('#submitBtn').removeClass('disabled');
  		break;

  	case 2:
  		$("#Node_Command").show();
   		$("#Key_Command").hide();
      $("#genkeyBtn").hide();
  		$('#submitBtn').removeClass('disabled');
  		break;

  	default:
  		$("#Key_Command").hide();
  		$("#Node_Command").hide();
  		$('#submitBtn').addClass('disabled');
  		break;
  }
}

var eventHandler = function(data) {

    console.log("success: content(AK) for node:" + data.node_id + " AK:" + data.authentication_key);
    var node_id = data.node_id;
    $("#" + "authentication_key-" + node_id).val(data.authentication_key);
    $("#" + "encryption_key-" + node_id).val(data.encryption_key);
    $("#" + "group_key-" + node_id).val(data.group_key);
    $("#" + "ota_key-" + node_id).val(data.ota_key);

};

var errorHandler = function(xhr) {
    switch (xhr.status) {
      //Shipping rate api error
      case 400:
      console.log("API error: inside xhr:" + xhr.status + " " + $.parseJSON(xhr.responseText)["error_msg"]);

    break;


  }
};

function generateKeys(){
  $.ajax("./get_node_keys", {
    data: {
      node_id: $('#node_ID').val(),
      node_deployment: $('#node_deployment').val(),
    },
    success: eventHandler,
    error: errorHandler
  });
  console.log("Inside function generateKeys");
}

function MQTTSubscribe() {
  var mqtt = require('mqtt')

  client = mqtt.createClient(1883, 'localhost');

  client.subscribe('presence');
  client.publish('presence', 'Hello mqtt');

  client.on('message', function (topic, message) {
    console.log(message);
  });

  client.end(); 
}

// document ready function
$(document).ready(function() {

	//Initialize the position of keys
    $('ul.nav').find('a:first').tab('show');
    $("#myDropdown").prop("selectedIndex", -1);
    $("input[name='interval_type']").change(
    	function() {
	        if ($("input[name='interval_type']:checked").val() == 'send') {
	        	$("#Send_Command").show();
	        	$("#Sense_Command").hide();
	        }
	        else if ($("input[name='interval_type']:checked").val() == 'sense') {
	        	$("#Send_Command").hide();
	        	$("#Sense_Command").show();
	    	}
    	}
	);          


});

