    var from_state=true;
    var from_lat, from_lon;
    var to_lat, to_lon;
    function initialize() {

        var mapOptions = {
            center: new google.maps.LatLng(40,-100),
            zoom: 4
        };

        var markerAdded = false;

        var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

        var latlng = new google.maps.LatLng(40, -100);


//        var lat = latlng.lat();
//        var lng = latlng.lng();
        var marker;

        var fromMarkerAdded=false;
        var toMarkerAdded=false;

        var fromMarker, toMarker;

        var latlong;


        google.maps.event.addListener(map, 'click', function(event) {
            from_state = $("#myonoffswitch").is(':checked')
            if(from_state)
            {
                if (!fromMarkerAdded) {
                    fromMarker = new google.maps.Marker({
                        map: map,
                        icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|FE7569"

                    });
                }

                fromMarker.setPosition(event.latLng);

                latlong = event.latLng;
                from_lat = latlong.lat();
                from_lon = latlong.lng();
                $("#ride-origin-lat").val(from_lat);
                $("#ride-origin-lon").val(from_lon);

                fromMarkerAdded=true;
            }
            else
            {
                if (!toMarkerAdded) {
                    toMarker = new google.maps.Marker({
                        map: map,
                        icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|75FE69"

                    });
                }
                toMarker.setPosition(event.latLng);
                latlong = event.latLng;

                to_lat = latlong.lat();
                to_lon = latlong.lng();
                toMarkerAdded=true;
                $("#ride-destination-lat").val(to_lat);
                $("#ride-destination-lon").val(to_lon);

            }
        });

    }

    google.maps.event.addDomListener(window, 'load', initialize);

    function getLocationData(){
        return {
            from_lat: from_lat,
            from_lon: from_lon,
            to_lat: to_lat,
            to_lon: to_lon
        }
    }