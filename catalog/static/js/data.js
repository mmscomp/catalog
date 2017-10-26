var Place = function(name, location) {
    this.name = name;
    this.location = location;
};

var viewModel = {};

//
viewModel.locations = [new Place(
    'Eiffel Tower', {
        lat: 48.8537009999999,
        lng: 2.2944813
    }
), new Place(
    'Notre Dame Catheral', {
        lat: 48.85296820000001,
        lng: 2.3499021
    }
), new Place(
    'Louvre', {
        lat: 48.8606111,
        lng: 2.337644
    }
), new Place(
    'Arc of Triumph', {
        lat: 48.8737917,
        lng: 2.2950275
    }
), new Place(
    'Seine', {
        lat: 48.8573797,
        lng: 2.3408735
    }
), new Place(
    'Montmartre', {
        lat: 48.8861929,
        lng: 2.3430895
    }
), new Place(
    'Musee Picasso', {
        lat: 48.8598775,
        lng: 2.362285
    }
), new Place(
    'Place de la Concorde', {
        lat: 48.8656331,
        lng: 2.3212357
    }
), new Place(
    'Place de la Bastille', {
        lat: 48.8531827,
        lng: 2.3691443
    }
), new Place(
    'Musee Grevin', {
        lat: 48.87183779999999,
        lng: 2.3422204
    }
), new Place('Luxembourg Park', {
    lat: 48.8462217,
    lng: 2.3371605
}), new Place('Moulin Rougue', {
    lat: 48.8841232,
    lng: 2.3322519
}), new Place('Musee Maillol', {
    lat: 48.85477419999999,
    lng: 2.3249052
}), new Place('Pont de Arts', {
    lat: 48.85834240000001,
    lng: 2.3375084
}), new Place('Pont des Invalides', {
    lat: 48.8635992,
    lng: 2.3103844
}), new Place('Musee Curie', {
        lat: 48.8608889,
        lng: 2.297894
    }
    /*, new Place('Disneyland Resort', {
            lat: 48.8722344,
            lng: 2.7758079
        }
    */
)];