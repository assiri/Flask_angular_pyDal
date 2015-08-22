var app = angular.module("app", []);

app.controller("AppCtrl", function ($http) {
    var app = this;

    $http.get("/api/pin").success(function(data) {
        app.pins = data.objects;
    });

    app.randomPin = function () {
        $http.post("/api/pin", {
            "title":"new",
            "image":"http://placekitten.com/250/250/?image=" + app.pins.length
        })
            .success(function(data) {
                app.pins.push(data);
            })
    };

    app.deletePin = function (pin) {
        $http.delete("/api/pin/" + pin.id)
            .success(function(response) {
                app.pins.splice(app.pins.indexOf(pin), 1); //this code to remove 1 item from array
            })
    };

    app.updatePin = function (pin) {
        $http.put("/api/pin/" + pin.id, pin);
    };

});

