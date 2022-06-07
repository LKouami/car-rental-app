$(document).ready(function() {
    $(document).on('submit', '#search-form', function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: 'ajaxContact',
            data: {
                query: $('#query').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken').val(),
            },
            success: function() {
                location.reload();
                $('#search-form')[0].reset();
            }
        });
    });
});