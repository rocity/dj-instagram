from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout

# Create your views here.

from .forms import LoginForm

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
