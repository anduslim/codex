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

var poly;
var lines = [];
var endMark;
var infowindow = new google.maps.InfoWindow();
var latlng = new google.maps.LatLng(1.34374595,103.82404489999999);
var myOptions = {
    zoom: 11, // The initial zoom level when your map loads (0-20)
    minZoom: 6, // Minimum zoom level allowed (0-20)
    maxZoom: 20, // Maximum soom level allowed (0-20)
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

function initialize()
{

    geocoder = new google.maps.Geocoder();

    map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);


}

function plotGeoJson(jsontext) {
  console.log(jsontext.features.length); // assume all features as "Point"
  var firstObject = jsontext.features[0];
  var startCoords = firstObject.geometry.coordinates;
  var prevObject = firstObject;
  var currObject;

  var mymarker = new google.maps.Marker({
    position: {lat: startCoords[1], lng: startCoords[0]},
    icon: {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 4
    },
    map: map,
    title:"Start"
  });

/*  var latlng = new google.maps.LatLng(myJson['features'][0]['geometry']['coordinates'][0],
                myJson['features'][0]['geometry']['coordinates'][1]);
*/
  map.setCenter(mymarker.position);
  map.setZoom(18);


  //polyline for calculating total distance
  var linepath = poly.getPath();
  linepath.push(new google.maps.LatLng(startCoords[1], startCoords[0]));

  for(var i = 1; i < jsontext.features.length; i++) {
    currObject = jsontext.features[i];
    var coords = currObject.geometry.coordinates;
    createline(prevObject, currObject);
    linepath.push(new google.maps.LatLng(coords[1], coords[0]));
    prevObject = currObject;
  }//end for

  var endCoords = currObject.geometry.coordinates;
  linepath.push(new google.maps.LatLng(endCoords[1], endCoords[0]));
  endMark = new google.maps.Marker({
    position: {lat: endCoords[1], lng: endCoords[0]},
    map: map,
    title:"End"
  });

  google.maps.event.addListener(endMark, 'mouseover', function(){
    var dist = google.maps.geometry.spherical.computeLength(poly.getPath());
    infowindow.setContent('<p style="color:black;">Distance: '+ dist.toFixed(1) + 'metres <br>' + 'Start time: '+
        firstObject.properties.timestamp+'sec <br>'+'End time: '+ currObject.properties.timestamp + 'sec</p>');
    infowindow.open(map,endMark);
  });
  google.maps.event.addListener(endMark, 'mouseout', function(){
    infowindow.setMap(null);
  });

}//end plotGeoJson()


function createline(prevObject, currObject) {
    var startCoords = prevObject.geometry.coordinates;
    var coords = currObject.geometry.coordinates;
    var color, weight, opacity;
    console.log(currObject.properties.inclination );
    if(currObject.properties.inclination < 0.1 && currObject.properties.inclination > -0.1) {
      color = "green";
    } else if(currObject.properties.inclination <= -0.1) {
      color = "blue";
    } else {
      color = "red";
    }
    if(currObject.properties.bumpiness > 2) {
      weight = 8; opacity = 0.8;
    } else {
      weight = 4; opacity = 0.5;
    }
    var line = new google.maps.Polyline({
      map: map,
      path: [
              new google.maps.LatLng(startCoords[1], startCoords[0]),
              new google.maps.LatLng(coords[1], coords[0])
            ],
      geodesic: true,
      strokeColor: color,
      strokeOpacity: opacity,
      strokeWeight: weight,
      zIndex: 1,
      timestamp: currObject.properties.timestamp,
      inclination: currObject.properties.inclination,
      bumpiness: currObject.properties.bumpiness
    });

    google.maps.event.addListener(line, 'mouseover', function(){
      console.log(line.timestamp);
      var path = line.getPath();
      infowindow.open(map, new google.maps.Marker({
            position: path.getAt(0),
            map: null}));
    infowindow.setContent("<p style='color:black;'> Time: "+line.timestamp+" sec <br>"+
                "Inclination: "+line.inclination+"<br>"+
                "Bumpiness: "+line.bumpiness + "</p>");
    });
    google.maps.event.addListener(line, 'mouseout', function(){
      infowindow.close();
    });
    lines.push(line);
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

    var wps = [{ location: point1 }, { location: point2 }];

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
/*  $('.google-maps-iframe').width('50%');*/
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
    for (var i=0; i<lines.length; i++) {
        lines[i].setMap(null); //or line[i].setVisible(false);
    }
    map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);
}


google.maps.event.addDomListener(window, 'load', initialize);
