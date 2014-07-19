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

function initialize()
{
    var latlng = new google.maps.LatLng(1.34374595,103.82404489999999);
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

    var rendererOptions = { map: map };
    directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
    directionsDisplay.setPanel(document.getElementById('controls'));

    var point1 = new google.maps.LatLng(1.2932808787143,103.843016698);
    var point2 = new google.maps.LatLng(1.2950608152056,103.8415261232);
    var point3 = new google.maps.LatLng(1.294709709207,103.841169);

    var wps = [{ location: point1 }, { location: point2 }, {location: point3}];

    var org = new google.maps.LatLng ( 1.2926529505238,103.84402854424);
    var dest = new google.maps.LatLng ( 1.2935613938379,103.84069470168);

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

google.maps.event.addDomListener(window, 'load', initialize);
