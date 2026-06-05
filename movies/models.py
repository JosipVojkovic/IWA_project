from django.db import models

GENRE_CHOICES = [
    ("Action", "Action"),
    ("Adventure", "Adventure"),
    ("Animation", "Animation"),
    ("Comedy", "Comedy"),
    ("Crime", "Crime"),
    ("Documentary", "Documentary"),
    ("Drama", "Drama"),
    ("Family", "Family"),
    ("Fantasy", "Fantasy"),
    ("Horror", "Horror"),
    ("Mystery", "Mystery"),
    ("Romance", "Romance"),
    ("Sci-Fi", "Sci-Fi"),
    ("Thriller", "Thriller"),
    ("War", "War"),
]

class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, blank=True, default='')
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor, blank=True)

    def __str__(self):
        return self.title
