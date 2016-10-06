/******************
* follow.js
* File where every script that is related to the model `Follow` will be here
******************/
$(document).ready(function() {
  $('.btn-follow').on('click', function (e) {
    e.preventDefault();

    var t = $(this),
        user_to_follow = t.data('user');

    $.ajax({
      url: '/insta/follow/',
      data: {uid: user_to_follow},
      dataType: 'json',
      type: 'post',
      success: function(data) {
        if (data.status == 1) {
          window.location.reload();
        } else {
          $('#notLoggedInModal').modal('show');
        }
      }
    });
  });

  /*
  * .btn-following Events
  * This button is found in the page where the logged user can view
  * the list of users he/she is following.
  * If the user hovers on this button, it should turn "red" and show a text
  * that says "Unfollow"
  */
  function followingHoverIn(e) {
    var t = $(this),
        span = t.find('span.glyphicon'),
        text = t.find('span.text');

    if (t.hasClass('btn-primary') && span.hasClass('glyphicon-ok')) {
      t.removeClass('btn-primary').addClass('btn-danger');
      span.removeClass('glyphicon-ok').addClass('glyphicon-remove');
      text.text('Unfollow');
    }
  }

  function followingHoverOut(e) {
    var t = $(this),
        span = t.find('span.glyphicon'),
        text = t.find('span.text');

    if (t.hasClass('btn-danger') && span.hasClass('glyphicon-remove')) {
      t.addClass('btn-primary').removeClass('btn-danger');
      span.removeClass('glyphicon-remove').addClass('glyphicon-ok');
      text.text('Following');
    }
  }

  function followingClick(e) {
    e.preventDefault();

    var t = $(this),
    user_to_unfollow = t.data('user');

    $.ajax({
      url: '/insta/unfollow/',
      data: {uid: user_to_unfollow},
      dataType: 'json',
      type: 'post',
      success: function(data) {
        if (data.status == 1) {
          window.location.reload();
        } else {
          $('#notLoggedInModal').modal('show');
        }
      }
    });
  }

  $('.btn-following')
                    .hover(followingHoverIn, followingHoverOut)
                    .click(followingClick);


}); // document ready
