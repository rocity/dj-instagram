/******************
* photo-comment.js
* Handles ajax requests to submit a comment on a photo
******************/
$(document).ready(function() {
    var comment_form_opts = {
        success: comment_response,
        clearForm: true
    }
    $('.comment-form').on('submit', function(e) {
        $(this).ajaxSubmit(comment_form_opts);
        return false;
    });

    $('.like-button').on('click', function(e) {
        var t = $(this),
            pid = t.data('pid'),
            req_url = t.data('url');
        t.addClass('liked_photo');

        $.ajax({
            data: {
                photo_id: pid
            },
            url: req_url,
            dataType: 'json',
            type: 'post',
            success: function(data) {
                console.log(data);
            }
        });
    });

    function comment_response(responseText, statusText, xhr, $form) {
        document.location.reload(true);
    }
});
