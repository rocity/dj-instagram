import json, itertools

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import LoginForm, PhotoForm, MemberPhotoForm
from .models import Follow, Photo, Member

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
    users = User.objects.all()[:10]

    for user in users:
        queryset = Follow.objects.filter(
                            follower__pk=request.user.id,
                            following__pk=user.pk
                            )
        user.is_followed = get_object_or_None(queryset)

    return render(request, 'instaapp/users.html', {'users': users})

def user_following(request):
    """
    View to display a list of users that the `logged user` is following
    """
    user = request.user

    following = Follow.objects.filter(follower__pk=user.id)

    return render(request, 'instaapp/user_following.html', {
        'following': following
        })

def user_followers(request):
    """
    View to display a list of users who follow the `logged user`
    """
    user = request.user

    followers = Follow.objects.filter(following__pk=user.id)

    # Check if you follow the users who follow you
    for follow in followers:
        following = Follow.objects.filter(
            follower__pk=user.id,
            following__pk=follow.pk)

        if following:
            follow.mutual_follow = True
        else:
            follow.mutual_follow = False

    return render(request, 'instaapp/user_followers.html', {
        'followers': followers,
        })

def follow_user(request):
    """
    Method (AJAX) that makes the `logged user` follow the selected user
    """
    data = {
            'status': 0,
        }
    if request.user.is_authenticated():
        if request.method == 'POST':
            follower = User.objects.get(pk=request.user.id)
            following = User.objects.get(pk=request.POST['uid'])

            follow = Follow(follower=follower, following=following)
            follow.save()

            # data to be returned as json
            data = {
                'status': 1,
                'follower': request.user.id,
                'to_follow': request.POST['uid']
            }

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

def upload_user_profile_pic(request):
    """
    Method (AJAX) that allows the `logged user` to upload a profile pic
    """
    uploader = request.user
    form = MemberPhotoForm()
    data = {
        'status': 1,
    }

    if request.method == 'POST':
        form = MemberPhotoForm(request.POST, request.FILES)
        if form.is_valid():

            # check if user has already uploaded a profile picture
            existing_dp = get_object_or_None(Member, user__pk=uploader.id)

            obj = form.save(commit=False)
            obj.user = uploader

            if existing_dp is not None:
                obj.id = existing_dp.id

            obj.save()

            data['status'] = 1

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
