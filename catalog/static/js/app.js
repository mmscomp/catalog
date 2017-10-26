/** Neighborhood of Place that I like to visit */

var map, infowindow, picture, article;


// Create a new blank array for all the listing markers.
var markers = [];

function initMap() {

    // Constructor creates a new map - only center and zoom are required.
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 48.85661400000001,
            lng: 2.3522219
        },
        zoom: 12
    });

   // loaidAllMarkers();
  //  loadMarker();
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
//ko for city

viewModel.city = ko.observable("");
console.log(1 + viewModel.city());
viewModel.cityText = ko.computed({
    read: function() {
        return viewModel.city();
    },
    write: function(value) {
        var lsp = value.lastIndexOf(" ");
        if(lsp > 0) {
        viewModel.city(value.substring(0,lsp));
       console.log(3 + value);
     }
    },
    owner: viewModel
});
console.log(2 + viewModel.cityText());
// Load  marker for input city
function loadInputMarker() {

    var largeInfoWindow = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();

    // Markers corresponding to locations
  //  for (var i = 0; i < viewModel.locations.length; i++) {
      var sURL = "http://maps.googleapis.com/maps/api/geocode/json?address="+viewModel.city();
$.ajax({
        url: sURL,
        dataType:'json'}).done(function(response){
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
     //   viewModel.clickMarkers(marker.title);
        //
        viewModel.clickMarker(marker.title);
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

// Load a  marker
function loadMarker() {

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
  //  console.log(98+ name);
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
    console.log(158 + " " + name);
    for (var i = 0; i < markers.length; i++) {
        if (markers[i].title != name) {
            if (markers[i].getAnimation() !== null) {
                markers[i].setAnimation(null);
            }
        } else {

            console.log(158 + " " + name);
            markers[i].setVisible(true);

            markers[i].animation = google.maps.Animation.BOUNCE;
            viewModel.info(markers[i]);
        }

    }
};

//Find a city
viewModel.findCity = function findCity(city){
     console.log(88 + " " + city());
     loadInputMarker();
}
// This function populates the infowindow when the marker is clicked. We'll only allow
// one infowindow which will open at the marker that is clicked, and populate based
// on that markers position.

viewModel.info = function populateInfoWindow(marker) {
    // Check to make sure the infowindow is not already opened on this marker.
    //  var infowindow = new google.maps.InfoWindow();
    //   var bounds = new google.maps.LatLngBounds();
    console.log(148 + " " + marker.title);
    var lt = "https://pixabay.com/api/?key=6400784-6502739bfc92fac659c45670a&q=" + marker.title + "&paris,france&image=photo"; // eiffel%20tower,paris&image=photo";

    var wikiUrl = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + marker.title + '&paris,france&limit=1&format=json&callback=wikiCallback';

    var lt1 = "https://pixabay.com/api/videos/?key=6400784-6502739bfc92fac659c45670a&q=" + marker.title + "&video_type=all"; 

    var wikiUrl1 = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + marker.title + '&limit=1&format=json&callback=wikiCallback';



    /*   $.ajax({
            url: wikiUrl,
            dataType: "jsonp",
            jsonp: "callback"
        }).done(function(response) {
            var pic = response.hits[0] ? response.hits[0].webformatURL : " data not available!";
            picture = pic;
            $.ajax({
                url: wikiUrl,
                dataType: "jsonp",
                jsonp: "callback"
            }).done(function(data) {
                var art = data[2] ? data[2] : " data not available!";
                article = art;

            }).fail(function(jqXHR, textStatus) {
                alert("Wikipedia link not found!");
            });
        }).fail(function(jqXHR, textStatus) {
            alert("A picture could not be loaded.");
        });


        if (infowindow.marker != marker) {
            infowindow.marker = marker;
            infowindow.setContent('<div><img src="' + picture + '"> <span>' + article + '</span></div>');
            infowindow.open(map, marker);

            // Make sure the marker property is cleared if the infowindow is closed.
            infowindow.addListener('closeclick', function() {
                infowindow.setMarker = null;
            });
        }
    }*/

    // Open an infoWindow
    infowindow.open(map, marker);
    $.when(ajax1(), ajax2()).done(function(a1, a2) {
        console.log(216 + " " + a1[0].hits.length + " " + a2[2].status);
        if (a1[0].hits.length === 0 && a2[0] === null) {
            infowindow.setContent('<div><span>Image not found </span></br><span>' + 'Also, no info found in wokipedia' + '</span></div');
        } else if (a1[0].hits.length === 0 && a2[0] !== null) {
            infowindow.setContent('<div><span>No image located! </span></br><span>' + a2[0] + '</span></div');
        } else if (a1[0].hits.length > 0 && a2[0] === null) {
            infowindow.setContent('<div><img src="' + a1[0].hits[0].webformatURL + '"> <span>' + 'No info found!' + '</span></div');
        } else if (a1[0].hits.length > 0 && a2[0] !== null) {
            infowindow.setContent('<div><img src="' + a1[0].hits[0].webformatURL + '"> <span>' + a2[0] + '</span></div');
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
            infowindow.setContent('<div><span>Image not found </span></br><span>' + 'Also, no info found in wokipedia' + '</span></div');
        } else if (a1[0].hits.length === 0 && a2[0] !== null) {
            infowindow.setContent('<div><span>No image located! </span></br><span>' + a2[0] + '</span></div');
        } else if (a1[0].hits.length > 0 && a2[0] === null) {
            infowindow.setContent('<div><iframe src="' + a1[0].hits[0].videos.large.url + '"></iframe> <span>' + 'No info found!' + '</span></div');
        } else if (a1[0].hits.length > 0 && a2[0] !== null) {
            infowindow.setContent('<div><iframe src="' + a1[0].hits[0].videos.large.url + '"></iframe> <span>' + a2[0] + '</span></div');
        }
    });

    // Ajax call for an image from pixabay
    function ajax3() {
        return $.ajax({
            url: lt1,
            dataType: "jsonp",
            jsonp: "callback"
        }).done(function(response) {
            var pic = response.hits[0] ? response.hits[0].videos.large.url : " data not available!";
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
