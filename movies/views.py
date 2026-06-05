from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count

from movies.models import Movie, Director, Actor, GENRE_CHOICES
from .forms import (
    RegisterForm,
    AdminUserCreationForm,
    AdminUserUpdateForm,
    AdminMovieForm,
    AdminDirectorForm,
    AdminActorForm,
)


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
    title_query = request.GET.get('title', '').strip()
    genre_query = request.GET.get('genre', '').strip()

    movies = Movie.objects.order_by('-release_date', 'title')

    if title_query:
        movies = movies.filter(title__icontains=title_query)
    if genre_query:
        movies = movies.filter(genre=genre_query)

    return render(request, 'movies.html', {
        'movies': movies,
        'title_query': title_query,
        'genre_query': genre_query,
        'genres': [g[0] for g in GENRE_CHOICES],
    })


@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    total_movies = Movie.objects.count()
    latest_release = (
        Movie.objects.filter(release_date__isnull=False)
        .order_by('-release_date', 'title')
        .first()
    )
    movies = Movie.objects.order_by('-release_date', 'title')
    return render(
        request,
        'admin-panel/dashboard.html',
        {
            'movies': movies[:6],
            'total_movies': total_movies,
            'latest_release': latest_release,
        },
    )


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
    return render(request, 'admin-panel/users.html', {
        'users': users,
        'stats': stats,
        'search_query': search_query,
    })


@login_required
def admin_user_create_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data['is_staff']
            user.is_superuser = form.cleaned_data['is_superuser']
            user.is_active = form.cleaned_data['is_active']
            if user.is_superuser:
                user.is_staff = True
            user.save()
            return redirect('admin_users')
    else:
        form = AdminUserCreationForm()
    return render(request, 'admin-panel/user_form.html', {'form': form, 'title': 'Add user', 'is_edit': False})


@login_required
def admin_user_edit_view(request, user_id):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    User = get_user_model()
    user_instance = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user_instance)
        if form.is_valid():
            user = form.save(commit=False)
            if user.is_superuser:
                user.is_staff = True
            user.save()
            return redirect('admin_users')
    else:
        form = AdminUserUpdateForm(instance=user_instance)
    return render(request, 'admin-panel/user_form.html', {'form': form, 'title': 'Edit user', 'is_edit': True})


@login_required
def admin_movies_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        movie = Movie.objects.filter(id=request.POST.get('movie_id')).first()
        if movie:
            movie.delete()
        return redirect('admin_movies')
    search_query = request.GET.get('q', '').strip()
    movies = Movie.objects.select_related('director').prefetch_related('actors').order_by('-release_date', 'title')
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query)
            | Q(director__first_name__icontains=search_query)
            | Q(director__last_name__icontains=search_query)
        )
    stats = {
        'total_movies': Movie.objects.count(),
        'with_posters': Movie.objects.filter(
            Q(poster_url__isnull=False) & ~Q(poster_url='')
        ).count(),
        'with_release_date': Movie.objects.filter(release_date__isnull=False).count(),
    }
    return render(request, 'admin-panel/movies.html', {
        'movies': movies,
        'stats': stats,
        'search_query': search_query,
    })


@login_required
def admin_movie_create_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = AdminMovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_movies')
    else:
        form = AdminMovieForm()
    return render(request, 'admin-panel/movie_form.html', {'form': form, 'title': 'Add movie'})


@login_required
def admin_movie_edit_view(request, movie_id):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = AdminMovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('admin_movies')
    else:
        form = AdminMovieForm(instance=movie)
    return render(request, 'admin-panel/movie_form.html', {'form': form, 'title': 'Edit movie'})


@login_required
def admin_directors_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        director = Director.objects.filter(id=request.POST.get('director_id')).first()
        if director:
            director.delete()
        return redirect('admin_directors')
    search_query = request.GET.get('q', '').strip()
    directors = Director.objects.annotate(movie_count=Count('movie')).order_by('last_name', 'first_name')
    if search_query:
        directors = directors.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
        )
    stats = {
        'total_directors': Director.objects.count(),
        'with_birth_date': Director.objects.filter(birth_date__isnull=False).count(),
        'with_movies': Director.objects.filter(movie__isnull=False).distinct().count(),
    }
    return render(request, 'admin-panel/directors.html', {
        'directors': directors,
        'stats': stats,
        'search_query': search_query,
    })


@login_required
def admin_director_create_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = AdminDirectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_directors')
    else:
        form = AdminDirectorForm()
    return render(request, 'admin-panel/director_form.html', {'form': form, 'title': 'Add director'})


@login_required
def admin_director_edit_view(request, director_id):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    director = get_object_or_404(Director, id=director_id)
    if request.method == 'POST':
        form = AdminDirectorForm(request.POST, instance=director)
        if form.is_valid():
            form.save()
            return redirect('admin_directors')
    else:
        form = AdminDirectorForm(instance=director)
    return render(request, 'admin-panel/director_form.html', {'form': form, 'title': 'Edit director'})


@login_required
def admin_actors_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        actor = Actor.objects.filter(id=request.POST.get('actor_id')).first()
        if actor:
            actor.delete()
        return redirect('admin_actors')
    search_query = request.GET.get('q', '').strip()
    actors = Actor.objects.annotate(movie_count=Count('movie', distinct=True)).order_by('last_name', 'first_name')
    if search_query:
        actors = actors.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
        )
    stats = {
        'total_actors': Actor.objects.count(),
        'with_birth_date': Actor.objects.filter(birth_date__isnull=False).count(),
        'with_movies': Actor.objects.filter(movie__isnull=False).distinct().count(),
    }
    return render(request, 'admin-panel/actors.html', {
        'actors': actors,
        'stats': stats,
        'search_query': search_query,
    })


@login_required
def admin_actor_create_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = AdminActorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_actors')
    else:
        form = AdminActorForm()
    return render(request, 'admin-panel/actor_form.html', {'form': form, 'title': 'Add actor'})


@login_required
def admin_actor_edit_view(request, actor_id):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    actor = get_object_or_404(Actor, id=actor_id)
    if request.method == 'POST':
        form = AdminActorForm(request.POST, instance=actor)
        if form.is_valid():
            form.save()
            return redirect('admin_actors')
    else:
        form = AdminActorForm(instance=actor)
    return render(request, 'admin-panel/actor_form.html', {'form': form, 'title': 'Edit actor'})
