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
    function comment_response(responseText, statusText, xhr, $form) {
        document.location.reload(true);
    }
});
