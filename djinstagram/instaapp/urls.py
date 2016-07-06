from django.conf.urls import url

from . import views

app_name = 'instaapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^upload/$', views.upload_photo, name='upload_photo'),
    url(r'^users/$', views.users, name='users'),
    url(r'^u/(?P<username>[\w-]+)$', views.user_profile, name='user_view'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^following/$', views.user_following, name='user_following'),
    url(r'^followers/$', views.user_followers, name='user_followers'),
    url(r'^feed/$', views.feed, name='feed'),

    # AJAX methods
    url(r'^upload_dp/$', views.upload_user_profile_pic,
        name='upload_user_profile_pic'),
    url(r'^follow/$', views.follow_user, name='follow_user'),
    url(r'^post_comment/$', views.post_photo_comment, name='post_photo_comment'),
    url(r'^like_comment/$', views.like_photo, name='like_photo'),
]
