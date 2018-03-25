
/* for showing search in detail */
function display(el){
 var name = $(el).attr('name');
  $.ajax({
            type: 'GET',
            url: '/fileread',
            data: { filename: name },
            async: true,
            success: function(data) {
                $('#fileContent').text(data);
                console.log(data);
            },
        });
}