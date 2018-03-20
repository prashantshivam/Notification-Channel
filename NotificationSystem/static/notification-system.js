function read_notification (id) {
    alert("fsdf")
    id = id;
    $.ajax({
        type: 'POST',
        url: '/read-notification/',
        data: {
            'id' : id,
            'csrfmiddlewaretoken': $('input[name=csrf]').val(),
        },
        success: function(data) {
            alert("prashant")
            $('#notification-'+id+']').style('background-color : blue');
        },
        error: function(data, err) {
            alert("na bhava");
        }
    });
};
