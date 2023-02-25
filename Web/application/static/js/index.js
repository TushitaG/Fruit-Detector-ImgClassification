var canvas = document.querySelector("#snapShot");
$("#predictButton").click(function() {
        $('#result').text(' Predicting...');
    var img = canvas.toDataURL('image/png');
    $.ajax({
        type: "POST",
        url: "https://ca2-2b02-jumanatushita-web.herokuapp.com/predict",
        data: img,
        success: function(data) {
            $('#result').text('Predicted Output: ' + data);

        }
    });
});