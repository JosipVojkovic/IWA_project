from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count

from movies.models import Movie, Director, Actor
from .forms import (
    RegisterForm,
    AdminUserCreationForm,
    AdminMovieForm,
    AdminDirectorForm,
    AdminActorForm,
    GENRE_CHOICES,
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
    create_form = AdminUserCreationForm()

    if request.method == 'POST':
        create_form = AdminUserCreationForm(request.POST)
        if create_form.is_valid():
            user = create_form.save(commit=False)
            user.is_staff = create_form.cleaned_data['is_staff']
            user.is_superuser = create_form.cleaned_data['is_superuser']
            user.is_active = create_form.cleaned_data['is_active']
            if user.is_superuser:
                user.is_staff = True
            user.save()
            return redirect('admin_users')

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
            'create_form': create_form,
        },
    )

@login_required
def admin_movies_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    search_query = request.GET.get('q', '').strip()
    create_form = AdminMovieForm()
    selected_actor_ids = []
    selected_director_id = ""

    if request.method == 'POST':
        create_form = AdminMovieForm(request.POST)
        selected_actor_ids = request.POST.getlist('actors')
        selected_director_id = request.POST.get('director', '')
        if create_form.is_valid():
            genre_name = create_form.cleaned_data['genre'] or None
            director = create_form.cleaned_data['director']
            poster_url = create_form.cleaned_data['poster_url']
            poster_url = poster_url.strip() if poster_url else None
            actors = create_form.cleaned_data['actors']

            movie = Movie.objects.create(
                title=create_form.cleaned_data['title'].strip(),
                description=(
                    create_form.cleaned_data['description'].strip()
                    if create_form.cleaned_data['description']
                    else None
                ),
                release_date=create_form.cleaned_data['release_date'],
                duration=create_form.cleaned_data['duration'],
                poster_url=poster_url,
                genre_name=genre_name,
                director=director,
            )

            if actors:
                movie.actors.set(actors)

            return redirect('admin_movies')

    movies = Movie.objects.select_related('genre', 'director').prefetch_related(
        'actors'
    ).order_by('-release_date', 'title')
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query)
            | Q(genre_name__icontains=search_query)
            | Q(genre__name__icontains=search_query)
            | Q(director__first_name__icontains=search_query)
            | Q(director__last_name__icontains=search_query)
        )

    stats = {
        'total_movies': Movie.objects.count(),
        'with_posters': Movie.objects.filter(
            (Q(poster__isnull=False) & ~Q(poster=''))
            | (Q(poster_url__isnull=False) & ~Q(poster_url=''))
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
            'create_form': create_form,
            'genres': GENRE_CHOICES,
            'actors': Actor.objects.order_by('last_name', 'first_name'),
            'selected_actor_ids': selected_actor_ids,
            'directors': Director.objects.order_by('last_name', 'first_name'),
            'selected_director_id': selected_director_id,
        },
    )

@login_required
def admin_directors_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    search_query = request.GET.get('q', '').strip()
    create_form = AdminDirectorForm()

    if request.method == 'POST':
        create_form = AdminDirectorForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('admin_directors')

    directors = Director.objects.annotate(movie_count=Count('movie')).order_by(
        'last_name',
        'first_name',
    )
    if search_query:
        directors = directors.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
        )

    stats = {
        'total_directors': Director.objects.count(),
        'with_birth_date': Director.objects.filter(birth_date__isnull=False).count(),
        'with_movies': Director.objects.filter(movie__isnull=False).distinct().count(),
    }

    return render(
        request,
        'admin-panel/directors.html',
        {
            'directors': directors,
            'stats': stats,
            'search_query': search_query,
            'create_form': create_form,
        },
    )

@login_required
def admin_actors_view(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)

    search_query = request.GET.get('q', '').strip()
    create_form = AdminActorForm()

    if request.method == 'POST':
        create_form = AdminActorForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('admin_actors')

    actors = Actor.objects.annotate(movie_count=Count('movie', distinct=True)).order_by(
        'last_name',
        'first_name',
    )
    if search_query:
        actors = actors.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
        )

    stats = {
        'total_actors': Actor.objects.count(),
        'with_birth_date': Actor.objects.filter(birth_date__isnull=False).count(),
        'with_movies': Actor.objects.filter(movie__isnull=False).distinct().count(),
    }

    return render(
        request,
        'admin-panel/actors.html',
        {
            'actors': actors,
            'stats': stats,
            'search_query': search_query,
            'create_form': create_form,
        },
    )
