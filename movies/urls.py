from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users_view, name='admin_users'),
    path('admin-panel/users/create/', views.admin_user_create_view, name='admin_user_create'),
    path('admin-panel/users/<int:user_id>/edit/', views.admin_user_edit_view, name='admin_user_edit'),
    path('admin-panel/movies/', views.admin_movies_view, name='admin_movies'),
    path('admin-panel/movies/create/', views.admin_movie_create_view, name='admin_movie_create'),
    path('admin-panel/movies/<int:movie_id>/edit/', views.admin_movie_edit_view, name='admin_movie_edit'),
    path('admin-panel/directors/', views.admin_directors_view, name='admin_directors'),
    path('admin-panel/directors/create/', views.admin_director_create_view, name='admin_director_create'),
    path('admin-panel/directors/<int:director_id>/edit/', views.admin_director_edit_view, name='admin_director_edit'),
    path('admin-panel/actors/', views.admin_actors_view, name='admin_actors'),
    path('admin-panel/actors/create/', views.admin_actor_create_view, name='admin_actor_create'),
    path('admin-panel/actors/<int:actor_id>/edit/', views.admin_actor_edit_view, name='admin_actor_edit'),
]
