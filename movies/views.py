from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from movies.models import Movie
from .forms import RegisterForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('movie_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('movie_list')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('movie_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})

@login_required
def dashboard_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    return render(request, 'dashboard/dashboard.html')
