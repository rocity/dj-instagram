# TODO[10.6.2016]: Refactor code, remove unused imports
# Normal views

import json, itertools

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from instaapp.forms import LoginForm, PhotoForm, MemberPhotoForm
from instaapp.models import Follow, Photo, Member, Comment, Like

from annoying.functions import get_object_or_None

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/insta/feed')
    return render(request, 'instaapp/index.html', {})

def feed(request):
    """
    View that displays the uploaded photos of users that the
    `logged user` follows
    """
    user = request.user
    photos = []
    user_following = Follow.objects.filter(follower__id=user.id)

    for user_object in user_following:
        following_photos = Photo.objects.filter(owner__id=user_object.following.id)

        if following_photos is not None:
            photos.append(following_photos)

    # flatten list of photos
    chain = itertools.chain(*photos)
    photos = list(chain)

    return render(request, 'instaapp/feed.html', {
        'photos': photos
        })

def user_login(request):
    form = LoginForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/insta')
        else:
            return HttpResponse('Invalid Login')
    else:
        form = LoginForm()

    return render(request, 'instaapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/insta/login')

def upload_photo(request):
    """
    Method that lets user upload an image
    """
    uploader = request.user
    form = PhotoForm()

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = uploader
            obj.save()

            return HttpResponseRedirect('/insta/upload')
    else:
        form = PhotoForm()

    return render(request, 'instaapp/upload_photo.html', {'form': form})

def user_profile(request, username=None):
    """
    View to display the `logged user's` profile and uploaded photos
    """

    upload_prof_pic_form = MemberPhotoForm()

    if username is None:
        user = request.user

    else:
        user = User.objects.get(username=username)

    dp_obj = get_object_or_None(Member, user__pk=user.id)
    if dp_obj is None:
        user_dp = False
    else:
        user_dp = dp_obj

    user_photos = Photo.objects.filter(owner__pk=user.id)
    photos_count = user_photos.count()
    return render(request, 'instaapp/profile.html', {
        'user': user,
        'user_dp': user_dp,
        'photos': user_photos,
        'count': photos_count,
        'dp_form': upload_prof_pic_form
        })

def users(request):
    """
    View to display a list of all users registered to the app
    """
    userlist = []
    users = User.objects.all()[:10]

    for user in users:
        queryset = Follow.objects.filter(
                            follower__pk=request.user.id,
                            following__pk=user.pk
                            )
        follow_status = get_object_or_None(queryset)

        if follow_status is None:
            userlist.append(user)

    return render(request, 'instaapp/users.html', {'users': userlist})

@login_required
def user_following(request):
    """
    View to display a list of users that the `logged user` is following
    """
    user = request.user

    following = Follow.objects.filter(follower__pk=user.id)

    return render(request, 'instaapp/user_following.html', {
        'following': following
        })

@login_required
def user_followers(request):
    """
    View to display a list of users who follow the `logged user`
    """
    followers = Follow.objects.filter(following__pk=request.user.id)

    # Check if you follow the users who follow you
    for user in followers:
        queryset = Follow.objects.filter(
            follower__id=request.user.id,
            following__id=user.follower.id
            )
        user.is_followed = get_object_or_None(queryset)


    return render(request, 'instaapp/user_followers.html', {
        'followers': followers,
        })


