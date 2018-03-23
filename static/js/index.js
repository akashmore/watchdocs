$(function() {
    $('#uploadSubmit').click(function(event) {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function(data) {
                $('#result').text(data.result);
                console.log(data.result);
            },
        });
        event.preventDefault();
    });
});