var map;
    function initialize() {

        var mapOptions = {
            center: new google.maps.LatLng(40.109329,-88.227392),
            zoom: 15
        };

        var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

    }

    function createPins(from_lat, from_lon, to_lat, to_lon){
        fromMarker = new google.maps.Marker({
                        map: map,
                        icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|FE7569"

                    });
        fromMarker.setPosition(new GLatLng(from_lat,from_lon));

        toMarker = new google.maps.Marker({
                        map: map,
                        icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|75FE69"

                    });
        toMarker.setPosition(new GLatLng(to_lat,to_lon));

        map.panTo(new GLatLng(to_lat,to_lon));

    }

    google.maps.event.addDomListener(window, 'load', initialize);//hi