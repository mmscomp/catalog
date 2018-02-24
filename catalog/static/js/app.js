/** Neighborhood of Place that I like to visit */

var geocoder, map, infowindow, picture, article;


// Create a new blank array for all the listing markers.
var markers = [];
var placeMarkers = [];
function initMap() {

    // Constructor creates a new map - only center and zoom are required.
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 48.85661400000001,
            lng: 2.3522219
        },
        zoom: 12
    });
   //geocoder

        geocoder = new google.maps.Geocoder();


    //loadAllMarkers();
    infowindow = new google.maps.InfoWindow();

}

// Google map error handler
function googleError() {
    alert("Not loading!");
}

// KO observable
viewModel.selectedName = ko.observable();
// Location name from KO observable
viewModel.selectedText = ko.computed({
    read: function() {
        return viewModel.selectedName() &&
            viewModel.selectedName().name;
    },
    write: function() {
        viewModel.selectedName().name;
    },
    owner: viewModel
});
// LatLng from KO observable
viewModel.selectedValue = ko.computed({
    read: function() {
        return viewModel.selectedName() &&
            viewModel.selectedName().location;
    },
    write: function(click) {
        viewModel.selectedName().location;
    },
    owner: viewModel

});

console.log(1 + " " + viewModel.selectedText());

//Initializing KO array of places
viewModel.placeList = ko.observableArray([]);

// KO observable
viewModel.selectedPlace = ko.observable("");

// Location name from KO observable
viewModel.selectedPlaceText = ko.computed({
    read: function() {
        return viewModel.selectedPlace() && viewModel.selectedPlace().place;
    },
    write: function() {
        viewModel.selectedPlace().place;
    },
    owner: viewModel
});
console.log(12 + " " + viewModel.selectedPlaceText());

//KO for city

viewModel.city = ko.observable("Paris");
console.log(1 + viewModel.city());
viewModel.cityText = ko.computed({
    read: function() {
        return viewModel.city();
    },
    write: function(value) {
        var lsp = value.lastIndexOf(" ");
        if (lsp > 0) {
            viewModel.city(value.substring(0, lsp));
            console.log(3 + value);
        }
    },
    owner: viewModel
});
console.log(2 + viewModel.cityText());

// This function fires when the user selects a searchbox picklist item.
// It will do a nearby search using the selected query string or place.
function searchBoxPlaces(searchBox) {
    hideMarkers(placeMarkers);
    var places = searchBox.getPlaces();
    if (places.length == 0) {
        window.alert('We did not find any places matching that search!');
    } else {
        // For each place, get the icon, name and location.
        createMarkersForPlaces(places);
    }
}
var result;
// This function fires when the user select "go" on the places search.
// It will do a nearby search using the entered query string or place.
viewModel.searchPlaces = function textSearchPlaces(place) {
       //   placeMarkers = [];
        console.log("110 " + place + " " + placeMarkers );
        var bounds = map.getBounds();
        hideMarkers(placeMarkers);
        var loc;
        console.log(108 + place + " " + viewModel.cityText());
          geocoder.geocode({'address': viewModel.cityText()}, function(results, status) {
          if (status === google.maps.GeocoderStatus.OK) {
          //  resultsMap.setCenter(results[0].geometry.location);
             loc = results[0].geometry.location;
         }
})
        var placesService = new google.maps.places.PlacesService(map);
        placesService.textSearch({
            location: loc, //viewModel.cityText(),
            query: place,
            radius: '500',
            type: place,
            bounds: bounds
        }, function(results, status) {
            console.log("110 " + results); 
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                createMarkersForPlaces(results);
                result = results;
            }
        });
}

    
    // This function creates markers for each place found in either places search.
function createMarkersForPlaces(places) {
        viewModel.placeList([]);
        console.log("129 " + places[0].rating);
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < places.length; i++) {
        var place = places[i];
        console.log(120 + " " + place.name);
        viewModel.placeList.push({name:place.name});
        console.log(121 + " " + viewModel.placeList[0]);

        var icon = {
            url: place.icon,
            size: new google.maps.Size(35, 35),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(15, 34),
            scaledSize: new google.maps.Size(15, 15)
        };
        // Create a marker for each place.
        var marker = new google.maps.Marker({
            map: map,
          //  icon: icon,
            title: place.name,
            position: place.geometry.location,
            id: place.place_id
        });
        // Create a single infowindow to be used with the place details information
        // so that only one is open at once.
        var placeInfoWindow = new google.maps.InfoWindow();
        // If a marker is clicked, do a place details search on it in the next function.
        marker.addListener('click', function() {
            if (placeInfoWindow.marker == this) {
                console.log("This infowindow already is on this marker!");
            } else {
                getPlacesDetails(this, placeInfoWindow);
            }
        });
        placeMarkers.push(marker);
        if (place.geometry.viewport) {
            // Only geocodes have viewport.
            bounds.union(place.geometry.viewport);
        } else {
            bounds.extend(place.geometry.location);
        }
    }
    map.fitBounds(bounds);
}

// This is the PLACE DETAILS search - it's the most detailed so it's only
// executed when a marker is selected, indicating the user wants more
// details about that place.
function getPlacesDetails(marker, infowindow) {
    var service = new google.maps.places.PlacesService(map);
    service.getDetails({
        placeId: marker.id
    }, function(place, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            // Set the marker property on this infowindow so it isn't created again.
            infowindow.marker = marker;
            var innerHTML = '<div>';
            if (place.name) {
                innerHTML += '<strong>' + place.name + '</strong>';
            }
            if (place.formatted_address) {
                innerHTML += '<br>' + place.formatted_address;
            }
            if (place.formatted_phone_number) {
                innerHTML += '<br>' + place.formatted_phone_number;
            }
            if (place.opening_hours) {
                innerHTML += '<br><br><strong>Hours:</strong><br>' +
                    place.opening_hours.weekday_text[0] + '<br>' +
                    place.opening_hours.weekday_text[1] + '<br>' +
                    place.opening_hours.weekday_text[2] + '<br>' +
                    place.opening_hours.weekday_text[3] + '<br>' +
                    place.opening_hours.weekday_text[4] + '<br>' +
                    place.opening_hours.weekday_text[5] + '<br>' +
                    place.opening_hours.weekday_text[6];
            }
            if (place.photos) {
                innerHTML += '<br><br><img src="' + place.photos[0].getUrl({
                    maxHeight: 100,
                    maxWidth: 200
                }) + '">';
            if (place.rating) {
                innerHTML += '<br><br><strong>Rating:</strong><br>' +
                place.rating;
              }}
            innerHTML += '</div>';
            infowindow.setContent(innerHTML);
            infowindow.open(map, marker);

            // Make sure the marker property is cleared if the infowindow is closed.
            infowindow.addListener('closeclick', function() {
                infowindow.marker = null;
            });
        }
    });
}

// This function will loop through the listings and hide them all.
function hideMarkers(markers) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
}
// Load  marker for input city
function loadInputMarker() {

    var largeInfoWindow = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();

    // Markers corresponding to locations
    //  for (var i = 0; i < viewModel.locations.length; i++) {
    var sURL = "http://maps.googleapis.com/maps/api/geocode/json?address=" + viewModel.city();
    $.ajax({
        url: sURL,
        dataType: 'json'
    }).done(function(response) {
        var position = response.results[0].geometry.location;


        // var position = viewModel.locations[i].location;
        var title = viewModel.city();
        console.log(9999, " ", title, position);
        map = new google.maps.Map(document.getElementById('map'), {
            center: {
                lat: position.lat,
                lng: position.lng
            },
            zoom: 15
        });

        // Create a marker
        var marker = new google.maps.Marker({
            map: map,
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            //    id: i
        });

        // Build markers list
        markers.push(marker);
        viewModel.clickMarkers(marker.title);
        //        viewModel.clickMarkers(markers[i].title);
    })
}

// Load all markers
function loadAllMarkers() {

    var largeInfoWindow = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();

    // Markers corresponding to locations
    for (var i = 0; i < viewModel.locations.length; i++) {
        var position = viewModel.locations[i].location;
        var title = viewModel.locations[i].name;
        // Create a marker
        var marker = new google.maps.Marker({
            map: map,
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            id: i
        });

        // Build markers list
        markers.push(marker);
        //
        viewModel.clickMarkers(markers[i].title);
    }
}

// Filter the selection
viewModel.filterMe = function filterMarker(name) {
    infowindow.close();
    for (var i = 0; i < markers.length; i++) {
        if (markers[i].title === name) {
            markers[i].setVisible(true);
            markers[i].animation = google.maps.Animation.BOUNCE;
        } else {
            markers[i].setVisible(false);
        }
    }
};

// Show all markers
viewModel.allMarkers = function showAll(name) {
      console.log(98+ name);
    if (infowindow) {
        infowindow.close();
    }
    for (var i = 0; i < markers.length; i++) {
        if (markers[i].title === name) {
            markers[i].setVisible(true);
            markers[i].setAnimation(null);
        }
    }
};

// Response to a click on a marker
viewModel.clickMarkers = function clickMarker(name) {

    for (var i = 0; i < markers.length; i++) {
        if (markers[i].title === name) {
            infoOpen(markers[i]);
        }
    }
};

// Infowindow activation
function infoOpen(marker) {
    marker.addListener('click', function() {
        for (var i = 0; i < markers.length; i++) {
            if (markers[i] != marker) {
                if (markers[i].getAnimation() !== null) {
                    console.log(119 + markers[i].title);
                    markers[i].setAnimation(null);
                }
            }
        }

        marker.setVisible(true);

        marker.animation = google.maps.Animation.BOUNCE;

        viewModel.info(this);
    });

}

// Response to a click on the listview
viewModel.clickMeDOM = function clickMarkerDOM(name) {
    console.log(158 + " " + name + " " + placeMarkers[0].title);
    for (var i = 0; i < placeMarkers.length; i++) {
        if (placeMarkers[i].title != name) {
            if (placeMarkers[i].getAnimation() !== null) {
                placeMarkers[i].setAnimation(null);
            }
        } else {

            console.log(158 + " " + name);
            placeMarkers[i].setVisible(true);

            placeMarkers[i].animation = google.maps.Animation.BOUNCE;
            viewModel.info(placeMarkers[i]);
        }

    }
};

//Find a city
viewModel.findCity = function findCity(city) {
        //      console.log(88 + " " + city());
        loadInputMarker();
    }
    // This function populates the infowindow when the marker is clicked. We'll only allow
    // one infowindow which will open at the marker that is clicked, and populate based
    // on that markers position.

viewModel.info = function populateInfoWindow(marker) {
    // Check to make sure the infowindow is not already opened on this marker.
    console.log(148 + " " + marker.title);
    var lt = "https://pixabay.com/api/?key=6400784-6502739bfc92fac659c45670a&q=" + marker.title + "&paris,france&image=photo"; /

    var wikiUrl = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + marker.title + '&paris,france&limit=1&format=json&callback=wikiCallback';

    var lt1 = "https://pixabay.com/api/videos/?key=6400784-6502739bfc92fac659c45670a&q=" + marker.title + "&video_type=all";

    var wikiUrl1 = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + marker.title + '&limit=1&format=json&callback=wikiCallback';




    // Open an infoWindow

    infowindow.open(map, marker);
    $.when(ajax1(), ajax2()).done(function(a1, a2) {
        console.log(216 + " " + a1[0].hits.length + " " + a2[2].status);
        if (a1[0].hits.length === 0 && a2[0] === null) {
            infowindow.setContent('<div><span>Image not found </span></br><span>' + 'Also, no info found in wokipedia' + '&emsp;<h4>more..Click the marker!</h4>' + '</span></div');
        } else if (a1[0].hits.length === 0 && a2[0] !== null) {
            infowindow.setContent('<div><span>No image located! </span></br><span>' + a2[0] + '&emsp;<h4>more..Click the marker!</h4>'+ '</span></div');
        } else if (a1[0].hits.length > 0 && a2[0] === null) {
            infowindow.setContent('<div><img src="' + a1[0].hits[0].webformatURL + '"> <span>' + 'No info found!' + '&emsp;<h4>more..Click the marker!</h4>' + '</span></div');
        } else if (a1[0].hits.length > 0 && a2[0] !== null) {
            infowindow.setContent('<div><img src="' + a1[0].hits[0].webformatURL + '"> <span>' + a2[0] + '&emsp;<h4>more..Click the marker!</h4>' + '</span></div');
        }
    });

    // Ajax call for an image from pixabay
    function ajax1() {
        return $.ajax({
            url: lt,
            dataType: "jsonp",
            jsonp: "callback"
        }).done(function(response) {
            var pic = response.hits[0] ? response.hits[0].webformatURL : " data not available!";
            picture = pic;
        }).fail(function(jqXHR, textStatus) {
            alert("A picture could not be loaded.");
        });
    }

    // Ajax call for a wikipedia intro
    function ajax2() {
        return $.ajax({
            url: wikiUrl,
            dataType: "jsonp",
            jsonp: "callback"
        }).done(function(data) {
            var art = data[2] ? data[2] : " data not available!";
            article = art;

        }).fail(function(jqXHR, textStatus) {
            alert("Wikipedia link not found!");
        });
    }

    // Open an infoWindow
    infowindow.open(map, marker);
    $.when(ajax3(), ajax4()).done(function(a1, a2) {
        console.log(216 + " " + a1[0].hits.length + " " + a2[2].status);
        if (a1[0].hits.length === 0 && a2[0] === null) {
            infowindow.setContent('<div><span>Image not found </span></br><span>' + 'Also, no info found in wokipedia' + '&emsp;<h4>more..Click the marker!</h4>' + '</span></div');
        } else if (a1[0].hits.length === 0 && a2[0] !== null) {
            infowindow.setContent('<div><span>No image located! </span></br><span>' + a2[0] + '&emsp;<h4>more..Click the marker!</h4>' +'</span></div');
        } else if (a1[0].hits.length > 0 && a2[0] === null) {
            infowindow.setContent('<div><iframe src="' + a1[0].hits[0].videos.medium.url + '"></iframe> <span>' + 'No info found!' + '&emsp;<h4>more..Click the marker!</h4>' + '</span></div');
        } else if (a1[0].hits.length > 0 && a2[0] !== null) {
            infowindow.setContent('<div><iframe src="' + a1[0].hits[0].videos.medium.url + '"></iframe> <span>' + a2[0] + '&emsp;<h4>more..Click the marker!</h4>' +'</span></div');
        }
    });

    // Ajax call for an image from pixabay
    function ajax3() {
        return $.ajax({
            url: lt1,
            dataType: "jsonp",
            jsonp: "callback"
        }).done(function(response) {
            var pic = response.hits[0] ? response.hits[0].videos.medium.url : " data not available!";
            picture = pic;
        }).fail(function(jqXHR, textStatus) {
            alert("A picture could not be loaded.");
        });
    }

    // Ajax call for a wikipedia intro
    function ajax4() {
        return $.ajax({
            url: wikiUrl1,
            dataType: "jsonp",
            jsonp: "callback"
        }).done(function(data) {
            var art = data[2] ? data[2] : " data not available!";
            article = art;

        }).fail(function(jqXHR, textStatus) {
            alert("Wikipedia link not found!");
        });
    }

};
ko.applyBindings(viewModel);
