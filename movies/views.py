from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    return render(request, 'admin-panel/dashboard.html')

@login_required
def admin_users_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    User = get_user_model()
    search_query = request.GET.get('q', '').strip()

    users = User.objects.all().order_by('-date_joined')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query)
        )

    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'staff_users': User.objects.filter(is_staff=True).count(),
        'superusers': User.objects.filter(is_superuser=True).count(),
    }

    return render(
        request,
        'admin-panel/users.html',
        {
            'users': users,
            'stats': stats,
            'search_query': search_query,
        },
    )

@login_required
def admin_movies_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    search_query = request.GET.get('q', '').strip()

    movies = Movie.objects.select_related('genre', 'director').prefetch_related(
        'actors'
    ).order_by('-release_date', 'title')
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query)
            | Q(genre__name__icontains=search_query)
            | Q(director__first_name__icontains=search_query)
            | Q(director__last_name__icontains=search_query)
        )

    stats = {
        'total_movies': Movie.objects.count(),
        'with_posters': Movie.objects.exclude(poster='').exclude(
            poster__isnull=True
        ).count(),
        'with_release_date': Movie.objects.filter(release_date__isnull=False).count(),
    }

    return render(
        request,
        'admin-panel/movies.html',
        {
            'movies': movies,
            'stats': stats,
            'search_query': search_query,
        },
    )
