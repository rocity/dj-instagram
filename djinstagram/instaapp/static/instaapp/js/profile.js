$(document).ready(function() {
    "use strict";

    var opts = {
        beforeSubmit: beforesub,
        success: successcall
    }

    $('#uploadDp').on('submit', function(e) {
        e.preventDefault();

        $(this).ajaxSubmit(opts);

    });

    function beforesub(formData, jqForm, options) {
        console.log("submitting")
    }

    function successcall(responseText, statusText, xhr, $form) {
        console.log(responseText);
        console.log(xhr);
    }
});
