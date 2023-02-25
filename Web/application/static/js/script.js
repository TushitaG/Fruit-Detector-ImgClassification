var stop = function() {
    var stream = video.srcObject;
    var tracks = stream.getTracks();

    for (var i = 0; i < tracks.length; i++) {
        var track = tracks[i];
        track.stop();
    }

    video.srcObject = null;
}

var start = function() {
    var video = document.getElementById('video'),
        vendorUrl = window.URL || window.webkitURL;
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
            }).catch(function(error) {
                console.log("Something went wrong!");
            });
    }
}
$(function() {
    start();
});

var canvas = document.querySelector("#snapShot");
// SHOW THE SNAPSHOT.
var takeSnapShot = function() {
    var video = document.getElementById('video');
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    
}

window.addEventListener('load', function() {
    document.querySelector('input[type="file"]').addEventListener('change', function() {
        if (this.files && this.files[0]) {
            // var canvas = document.querySelector("#snapShot");
            var img = new Image;
            img.onload = () => {
                canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
            }
            img.src = URL.createObjectURL(this.files[0]); // set src to blob url
            
        }
    });
});
$("#clearButton").on("click", function() {
    var canvas = document.querySelector("#snapShot");
    var context = canvas.getContext("2d");
    context.clearRect(0, 0, 244, 244);
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
});