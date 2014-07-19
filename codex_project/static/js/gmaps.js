/*function initialize()
{
    var directionsService = new google.maps.DirectionsService();
    var directionsDisplay = new google.maps.DirectionsRenderer();

    var map = new google.maps.Map(document.getElementById('map-canvas'), {
        zoom:7,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById('controls'));

    var request = {
        origin: 'Chicago',
        destination: 'New York',
        travelMode: google.maps.DirectionsTravelMode.DRIVING
    };

    directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    });
}*/

var geocoder;
var map;
var marker;
var org;
var dest;

function initialize()
{
    var latlng = new google.maps.LatLng(1.34374595,103.82404489999999);
    geocoder = new google.maps.Geocoder();
    var myOptions = {
        zoom: 11, // The initial zoom level when your map loads (0-20)
        minZoom: 6, // Minimum zoom level allowed (0-20)
        maxZoom: 17, // Maximum soom level allowed (0-20)
        zoomControl:true, // Set to true if using zoomControlOptions below, or false to remove all zoom controls.
        zoomControlOptions: {
            style:google.maps.ZoomControlStyle.DEFAULT // Change to SMALL to force just the + and - buttons.
        },
        center: latlng, // Centre the Map to our coordinates variable
        mapTypeId: google.maps.MapTypeId.ROADMAP, // Set the type of Map
        scrollwheel: false, // Disable Mouse Scroll zooming (Essential for responsive sites!)
        // All of the below are set to true by default, so simply remove if set to true:
        panControl:false, // Set to false to disable
        mapTypeControl:false, // Disable Map/Satellite switch
        scaleControl:false, // Set to false to hide scale
        streetViewControl:false, // Set to disable to hide street view
        overviewMapControl:false, // Set to false to remove overview control
        rotateControl:false // Set to false to disable rotate control
    };
    map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);

}

function codeSrcAddress() {
    var address = $('#fromAddress').val();
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
      });
      console.log("location:" + results[0].geometry.location);
      return results[0].geometry.location;
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

function codeDestAddress() {
    var address = $('#toAddress').val();
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
      });
      console.log("location:" + results[0].geometry.location);
      return results[0].geometry.location;
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

function plotRoute() {
    var rendererOptions = { map: map };
    directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
    directionsDisplay.setPanel(document.getElementById('controls'));

    var point1 = new google.maps.LatLng(1.2948948, 103.8510814);
    var point2 = new google.maps.LatLng(1.298593, 103.845909);

    var wps = [{ location: point1 }, { location: point2 }, {location: point3}];

    org = new google.maps.LatLng ( 1.2968599, 103.852202);
    dest = new google.maps.LatLng ( 1.2974042, 103.8542797);

    var request = {
            origin: org,
            destination: dest,
            waypoints: wps,
            travelMode: google.maps.DirectionsTravelMode.WALKING
            };

    directionsService = new google.maps.DirectionsService();
    directionsService.route(request, function(response, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                    directionsDisplay.setDirections(response);
                }
                else
                    alert ('failed to get directions');
            });

}


var eventHandler = function(data) {

    console.log("success: readings:" + data.readings);
    var readings = data.readings;
};

var errorHandler = function(xhr) {
    console.log("xhr.status:" + xhr.status);
    switch (xhr.status) {
      case 404:
      console.log("API error: inside xhr:" + xhr.status + " " + xhr.responseText);
      $('#error_msg').text("Error! Route does not exist!");
    break;


  }
};

function getReadings(){
  var source = codeSrcAddress();
  var destination = codeDestAddress();

/*  org = new google.maps.LatLng (source);
  dest = new google.maps.LatLng ( destination);*/
  plotRoute();
/*  $.ajax("./api/reading", {
    data: {
      source: source,
      destination: destination,
    },
    success: eventHandler,
    error: errorHandler
  });*/
  console.log("Inside function getReadings");
}

function clearReadings(){

    $('#error_msg').text("");
    map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);
}


google.maps.event.addDomListener(window, 'load', initialize);
