from django.conf.urls import url

from . import views

app_name = 'instaapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^upload/$', views.upload_photo, name='upload_photo'),
    url(r'^users/$', views.users, name='users'),
]
