import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import LoginForm, PhotoForm
from .models import Follow

# Create your views here.

def index(request):
    return render(request, 'instaapp/index.html', {})

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

def upload_photo(request):
    form = PhotoForm()

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/insta/upload')
    else:
        form = PhotoForm()

    return render(request, 'instaapp/upload_photo.html', {'form': form})

def users(request):
    users = User.objects.all()
    return render(request, 'instaapp/users.html', {'users': users})

def follow_user(request):
    data = {
        'status': 1,
        'follower': request.user.id,
        'to_follow': request.POST['uid']
    }
    if request.method == 'POST':
        follower = User.objects.get(pk=request.user.id)
        following = User.objects.get(pk=request.POST['uid'])

        follow = Follow(follower=follower, following=following)
        follow.save()

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
