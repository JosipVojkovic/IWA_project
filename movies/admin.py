from django.contrib import admin

from movies.models import Actor, Director, Genre, Movie

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Actor)

# USER DATA
# ---------------------
# username: josip
# password: Jopa@Jopa123
# email: josip.vojkovic0@gmail.com