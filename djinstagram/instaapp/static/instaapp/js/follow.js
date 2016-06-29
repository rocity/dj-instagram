/******************
* follow.js
* File where every script that is related to the model `Follow` will be here
******************/
$(document).ready(function() {
  $('.btn-follow').on('click', function(e) {
    e.preventDefault();

    var t = $(this),
        user_to_follow = t.data('user');

    $.ajax({
      url: '/insta/follow/',
      data: {uid: user_to_follow},
      dataType: 'json',
      type: 'post',
      success: function(data) {
        window.location.reload();
      }
    });
  });
});
