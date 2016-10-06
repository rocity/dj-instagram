# TODO[10.6.2016]: Refactor code, remove unused imports
# Views for AJAX Requests

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

def post_photo_comment(request):
    data = {
        'status': 0
    }

    if request.user.is_authenticated() and request.method == 'POST':
        post_data = request.POST

        photo = get_object_or_None(Photo, pk=post_data['photo_id'])
        comment = Comment(
            owner=request.user.member,
            photo=photo,
            text=post_data['comment_text']
            )
        resp = comment.save()
        if resp:
            data['status'] = 1

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

def like_photo(request):
    data = {
        'status': 0
    }

    # TODO: Check if like already exists
    if request.user.is_authenticated() and request.method == 'POST':
        post_data = request.POST

        photo = get_object_or_None(Photo, pk=post_data['photo_id'])
        like = Like(
            owner=request.user.member,
            photo=photo,
            )
        resp = like.save()
        if resp:
            data['status'] = 1

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
