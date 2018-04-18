
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

            },
        });
}

/*for downloading */
function download(element)
{
  var name = $(element).attr('name');
  console.log(name)
  $.ajax({
            type: 'GET',
            url: '/filedownload',
            data: { filename: name },
            async: true,
            success:function(data){
            //console.log(data)
            downloadFile(name,data)

            }


        });



}

/*testing*/
function downloadFile(filename,text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

