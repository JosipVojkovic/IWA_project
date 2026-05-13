from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from movies.models import Actor, Director, Movie

# Release dates use a Jan 1 placeholder to avoid guessing exact premiere dates.
MOVIES = [
    {
        "title": "The Shawshank Redemption",
        "genre_name": "Drama",
        "release_date": date(1994, 1, 1),
        "duration": None,
        "director": ("Frank", "Darabont"),
        "actors": [
            ("Tim", "Robbins"),
            ("Morgan", "Freeman"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/911USrdQtPL.jpg",
    },
    {
        "title": "The Godfather",
        "genre_name": "Crime",
        "release_date": date(1972, 1, 1),
        "duration": None,
        "director": ("Francis Ford", "Coppola"),
        "actors": [
            ("Marlon", "Brando"),
            ("Al", "Pacino"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/510L5ypQBdL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "The Dark Knight",
        "genre_name": "Action",
        "release_date": date(2008, 1, 1),
        "duration": None,
        "director": ("Christopher", "Nolan"),
        "actors": [
            ("Christian", "Bale"),
            ("Heath", "Ledger"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/5151N2hUPiL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "Pulp Fiction",
        "genre_name": "Crime",
        "release_date": date(1994, 1, 1),
        "duration": None,
        "director": ("Quentin", "Tarantino"),
        "actors": [
            ("John", "Travolta"),
            ("Samuel L.", "Jackson"),
        ],
        "poster_url": "https://image.tmdb.org/t/p/original/gSnbhR0vftfJ2U6KpGmR7WzZlVo.jpg",
    },
    {
        "title": "Fight Club",
        "genre_name": "Drama",
        "release_date": date(1999, 1, 1),
        "duration": None,
        "director": ("David", "Fincher"),
        "actors": [
            ("Brad", "Pitt"),
            ("Edward", "Norton"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/81D+KJkO4SL.jpg",
    },
    {
        "title": "Forrest Gump",
        "genre_name": "Drama",
        "release_date": date(1994, 1, 1),
        "duration": None,
        "director": ("Robert", "Zemeckis"),
        "actors": [
            ("Tom", "Hanks"),
            ("Robin", "Wright"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/61gJ0U3mAiL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "Gladiator",
        "genre_name": "Action",
        "release_date": date(2000, 1, 1),
        "duration": None,
        "director": ("Ridley", "Scott"),
        "actors": [
            ("Russell", "Crowe"),
            ("Joaquin", "Phoenix"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/71Emol9GByL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "Titanic",
        "genre_name": "Romance",
        "release_date": date(1997, 1, 1),
        "duration": None,
        "director": ("James", "Cameron"),
        "actors": [
            ("Leonardo", "DiCaprio"),
            ("Kate", "Winslet"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/71ps2xBoAuL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "The Silence of the Lambs",
        "genre_name": "Thriller",
        "release_date": date(1991, 1, 1),
        "duration": None,
        "director": ("Jonathan", "Demme"),
        "actors": [
            ("Jodie", "Foster"),
            ("Anthony", "Hopkins"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNDdhOGJhYzctYzYwZC00YmI2LWI0MjctYjg4ODdlMDExYjBlXkEyXkFqcGc@._V1_.jpg",
    },
    {
        "title": "Schindler's List",
        "genre_name": "Drama",
        "release_date": date(1993, 1, 1),
        "duration": None,
        "director": ("Steven", "Spielberg"),
        "actors": [
            ("Liam", "Neeson"),
            ("Ralph", "Fiennes"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/71vKAOMv8nL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "Jurassic Park",
        "genre_name": "Adventure",
        "release_date": date(1993, 1, 1),
        "duration": None,
        "director": ("Steven", "Spielberg"),
        "actors": [
            ("Sam", "Neill"),
            ("Laura", "Dern"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/61iF3RSsLsL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "Saving Private Ryan",
        "genre_name": "War",
        "release_date": date(1998, 1, 1),
        "duration": None,
        "director": ("Steven", "Spielberg"),
        "actors": [
            ("Tom", "Hanks"),
            ("Matt", "Damon"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZGZhZGQ1ZWUtZTZjYS00MDJhLWFkYjctN2ZlYjE5NWYwZDM2XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "The Departed",
        "genre_name": "Crime",
        "release_date": date(2006, 1, 1),
        "duration": None,
        "director": ("Martin", "Scorsese"),
        "actors": [
            ("Leonardo", "DiCaprio"),
            ("Matt", "Damon"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/51mjWgQocwL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "Goodfellas",
        "genre_name": "Crime",
        "release_date": date(1990, 1, 1),
        "duration": None,
        "director": ("Martin", "Scorsese"),
        "actors": [
            ("Robert", "De Niro"),
            ("Ray", "Liotta"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/61GgTIrIIUL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "The Wolf of Wall Street",
        "genre_name": "Comedy",
        "release_date": date(2013, 1, 1),
        "duration": None,
        "director": ("Martin", "Scorsese"),
        "actors": [
            ("Leonardo", "DiCaprio"),
            ("Jonah", "Hill"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_.jpg",
    },
    {
        "title": "The Social Network",
        "genre_name": "Drama",
        "release_date": date(2010, 1, 1),
        "duration": None,
        "director": ("David", "Fincher"),
        "actors": [
            ("Jesse", "Eisenberg"),
            ("Andrew", "Garfield"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjlkNTE5ZTUtNGEwNy00MGVhLThmZjMtZjU1NDE5Zjk1NDZkXkEyXkFqcGc@._V1_.jpg",
    },
    {
        "title": "Se7en",
        "genre_name": "Thriller",
        "release_date": date(1995, 1, 1),
        "duration": None,
        "director": ("David", "Fincher"),
        "actors": [
            ("Brad", "Pitt"),
            ("Morgan", "Freeman"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/71ivyTtPwoL.jpg",
    },
    {
        "title": "The Green Mile",
        "genre_name": "Drama",
        "release_date": date(1999, 1, 1),
        "duration": None,
        "director": ("Frank", "Darabont"),
        "actors": [
            ("Tom", "Hanks"),
            ("Michael Clarke", "Duncan"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/71+gLki+J8L._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "Parasite",
        "genre_name": "Thriller",
        "release_date": date(2019, 1, 1),
        "duration": None,
        "director": ("Bong", "Joon-ho"),
        "actors": [
            ("Song", "Kang-ho"),
            ("Lee", "Sun-kyun"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjk1Y2U4MjQtY2ZiNS00OWQyLWI3MmYtZWUwNmRjYWRiNWNhXkEyXkFqcGc@._V1_.jpg",
    },
    {
        "title": "Oldboy",
        "genre_name": "Thriller",
        "release_date": date(2003, 1, 1),
        "duration": None,
        "director": ("Park", "Chan-wook"),
        "actors": [
            ("Choi", "Min-sik"),
            ("Yoo", "Ji-tae"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTAwNzNjYWItZmI0Ni00ZTcyLWIwNWMtZjlmNGMxZTEyYTJmXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "The Grand Budapest Hotel",
        "genre_name": "Comedy",
        "release_date": date(2014, 1, 1),
        "duration": None,
        "director": ("Wes", "Anderson"),
        "actors": [
            ("Ralph", "Fiennes"),
            ("Tony", "Revolori"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/713kiC-8JhL.jpg",
    },
    {
        "title": "Whiplash",
        "genre_name": "Drama",
        "release_date": date(2014, 1, 1),
        "duration": None,
        "director": ("Damien", "Chazelle"),
        "actors": [
            ("Miles", "Teller"),
            ("J.K.", "Simmons"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/61H0xokzFQL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "La La Land",
        "genre_name": "Romance",
        "release_date": date(2016, 1, 1),
        "duration": None,
        "director": ("Damien", "Chazelle"),
        "actors": [
            ("Ryan", "Gosling"),
            ("Emma", "Stone"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/710e0in+tAL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "Mad Max: Fury Road",
        "genre_name": "Action",
        "release_date": date(2015, 1, 1),
        "duration": None,
        "director": ("George", "Miller"),
        "actors": [
            ("Tom", "Hardy"),
            ("Charlize", "Theron"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZDRkODJhOTgtOTc1OC00NTgzLTk4NjItNDgxZDY4YjlmNDY2XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "The Pianist",
        "genre_name": "Drama",
        "release_date": date(2002, 1, 1),
        "duration": None,
        "director": ("Roman", "Polanski"),
        "actors": [
            ("Adrien", "Brody"),
            ("Thomas", "Kretschmann"),
        ],
        "poster_url": "https://cdng.europosters.eu/pod_public/1300/263610.jpg",
    },
    {
        "title": "City of God",
        "genre_name": "Crime",
        "release_date": date(2002, 1, 1),
        "duration": None,
        "director": ("Fernando", "Meirelles"),
        "actors": [
            ("Alexandre", "Rodrigues"),
            ("Leandro", "Firmino"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjY4NGI5OTUtY2ZlZS00Zjk4LTk5N2MtN2JmYWVjNGNmMGRlXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "The Prestige",
        "genre_name": "Mystery",
        "release_date": date(2006, 1, 1),
        "duration": None,
        "director": ("Christopher", "Nolan"),
        "actors": [
            ("Hugh", "Jackman"),
            ("Christian", "Bale"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTM3MzQ5MjQ5OF5BMl5BanBnXkFtZTcwMTQ3NzMzMw@@._V1_QL75_UY281_CR0,0,190,281_.jpg",
    },
    {
        "title": "Memento",
        "genre_name": "Mystery",
        "release_date": date(2000, 1, 1),
        "duration": None,
        "director": ("Christopher", "Nolan"),
        "actors": [
            ("Guy", "Pearce"),
            ("Carrie-Anne", "Moss"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/51xPto5R6NL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "The Martian",
        "genre_name": "Sci-Fi",
        "release_date": date(2015, 1, 1),
        "duration": None,
        "director": ("Ridley", "Scott"),
        "actors": [
            ("Matt", "Damon"),
            ("Jessica", "Chastain"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTc2MTQ3MDA1Nl5BMl5BanBnXkFtZTgwODA3OTI4NjE@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "Blade Runner 2049",
        "genre_name": "Sci-Fi",
        "release_date": date(2017, 1, 1),
        "duration": None,
        "director": ("Denis", "Villeneuve"),
        "actors": [
            ("Ryan", "Gosling"),
            ("Harrison", "Ford"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/71NPmBOdq7L.jpg",
    },
    {
        "title": "Arrival",
        "genre_name": "Sci-Fi",
        "release_date": date(2016, 1, 1),
        "duration": None,
        "director": ("Denis", "Villeneuve"),
        "actors": [
            ("Amy", "Adams"),
            ("Jeremy", "Renner"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTExMzU0ODcxNDheQTJeQWpwZ15BbWU4MDE1OTI4MzAy._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "Dune",
        "genre_name": "Sci-Fi",
        "release_date": date(2021, 1, 1),
        "duration": None,
        "director": ("Denis", "Villeneuve"),
        "actors": [
            ("Timothee", "Chalamet"),
            ("Zendaya", "Coleman"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/61TNx4nsnpL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "Get Out",
        "genre_name": "Horror",
        "release_date": date(2017, 1, 1),
        "duration": None,
        "director": ("Jordan", "Peele"),
        "actors": [
            ("Daniel", "Kaluuya"),
            ("Allison", "Williams"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjUxMDQwNjcyNl5BMl5BanBnXkFtZTgwNzcwMzc0MTI@._V1_.jpg",
    },
    {
        "title": "Black Panther",
        "genre_name": "Action",
        "release_date": date(2018, 1, 1),
        "duration": None,
        "director": ("Ryan", "Coogler"),
        "actors": [
            ("Chadwick", "Boseman"),
            ("Michael B.", "Jordan"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTg1MTY2MjYzNV5BMl5BanBnXkFtZTgwMTc4NTMwNDI@._V1_.jpg",
    },
    {
        "title": "The Shape of Water",
        "genre_name": "Fantasy",
        "release_date": date(2017, 1, 1),
        "duration": None,
        "director": ("Guillermo", "del Toro"),
        "actors": [
            ("Sally", "Hawkins"),
            ("Michael", "Shannon"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOGFlMTM2MTgtZDdlMy00ZDZlLWFjOTUtZDMzMGEwNmNiMWY0XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "Pan's Labyrinth",
        "genre_name": "Fantasy",
        "release_date": date(2006, 1, 1),
        "duration": None,
        "director": ("Guillermo", "del Toro"),
        "actors": [
            ("Ivana", "Baquero"),
            ("Sergi", "Lopez"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/518uWnli4pL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "The Revenant",
        "genre_name": "Adventure",
        "release_date": date(2015, 1, 1),
        "duration": None,
        "director": ("Alejandro", "Gonzalez Inarritu"),
        "actors": [
            ("Leonardo", "DiCaprio"),
            ("Tom", "Hardy"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYTgwNmQzZDctMjNmOS00OTExLTkwM2UtNzJmOTJhODFjOTdlXkEyXkFqcGc@._V1_.jpg",
    },
    {
        "title": "Birdman",
        "genre_name": "Drama",
        "release_date": date(2014, 1, 1),
        "duration": None,
        "director": ("Alejandro", "Gonzalez Inarritu"),
        "actors": [
            ("Michael", "Keaton"),
            ("Edward", "Norton"),
        ],
        "poster_url": "https://upload.wikimedia.org/wikipedia/sh/a/a3/Birdman_poster.jpg",
    },
    {
        "title": "There Will Be Blood",
        "genre_name": "Drama",
        "release_date": date(2007, 1, 1),
        "duration": None,
        "director": ("Paul Thomas", "Anderson"),
        "actors": [
            ("Daniel", "Day-Lewis"),
            ("Paul", "Dano"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjAxODQ4MDU5NV5BMl5BanBnXkFtZTcwMDU4MjU1MQ@@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "Her",
        "genre_name": "Romance",
        "release_date": date(2013, 1, 1),
        "duration": None,
        "director": ("Spike", "Jonze"),
        "actors": [
            ("Joaquin", "Phoenix"),
            ("Scarlett", "Johansson"),
        ],
        "poster_url": "https://ih1.redbubble.net/image.3143898460.4368/flat,750x,075,f-pad,750x1000,f8f8f8.u1.jpg",
    },
    {
        "title": "Moonlight",
        "genre_name": "Drama",
        "release_date": date(2016, 1, 1),
        "duration": None,
        "director": ("Barry", "Jenkins"),
        "actors": [
            ("Trevante", "Rhodes"),
            ("Mahershala", "Ali"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/91Tu1WACkuL._AC_UF894,1000_QL80_.jpg",
    },
    {
        "title": "12 Years a Slave",
        "genre_name": "Drama",
        "release_date": date(2013, 1, 1),
        "duration": None,
        "director": ("Steve", "McQueen"),
        "actors": [
            ("Chiwetel", "Ejiofor"),
            ("Lupita", "Nyong'o"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/61QFAKXbb5L.jpg",
    },
    {
        "title": "The Imitation Game",
        "genre_name": "Drama",
        "release_date": date(2014, 1, 1),
        "duration": None,
        "director": ("Morten", "Tyldum"),
        "actors": [
            ("Benedict", "Cumberbatch"),
            ("Keira", "Knightley"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNjI3NjY1Mjg3MV5BMl5BanBnXkFtZTgwMzk5MDQ3MjE@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "The Truman Show",
        "genre_name": "Comedy",
        "release_date": date(1998, 1, 1),
        "duration": None,
        "director": ("Peter", "Weir"),
        "actors": [
            ("Jim", "Carrey"),
            ("Laura", "Linney"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzA3ZjZlNzYtMTdjMy00NjMzLTk5ZGYtMTkyYzNiOGM1YmM3XkEyXkFqcGc@._V1_.jpg",
    },
    {
        "title": "The Sixth Sense",
        "genre_name": "Mystery",
        "release_date": date(1999, 1, 1),
        "duration": None,
        "director": ("M. Night", "Shyamalan"),
        "actors": [
            ("Bruce", "Willis"),
            ("Haley Joel", "Osment"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZWQ2OTY0M2UtMTQxNC00MmIzLTllNDQtNDQ0MTQyYzI2M2ZiXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "A Beautiful Mind",
        "genre_name": "Drama",
        "release_date": date(2001, 1, 1),
        "duration": None,
        "director": ("Ron", "Howard"),
        "actors": [
            ("Russell", "Crowe"),
            ("Jennifer", "Connelly"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjgzNjFkMmItOGJhNi00NWM3LWJlYTUtNDExMGQ3ZTI3NjJkXkEyXkFqcGc@._V1_.jpg",
    },
    {
        "title": "The Hurt Locker",
        "genre_name": "War",
        "release_date": date(2008, 1, 1),
        "duration": None,
        "director": ("Kathryn", "Bigelow"),
        "actors": [
            ("Jeremy", "Renner"),
            ("Anthony", "Mackie"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzgyMGM2YTItYzY2Yi00NDQ0LWE0M2EtMGUzYjFlMDgyY2M3XkEyXkFqcGc@._V1_QL75_UX190_CR0,2,190,281_.jpg",
    },
    {
        "title": "Slumdog Millionaire",
        "genre_name": "Drama",
        "release_date": date(2008, 1, 1),
        "duration": None,
        "director": ("Danny", "Boyle"),
        "actors": [
            ("Dev", "Patel"),
            ("Freida", "Pinto"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTE5ZTRkYWEtZmU5MC00NDJjLTk3NmUtZGJlYTM2MmQ3NTJkXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    },
    {
        "title": "The King's Speech",
        "genre_name": "Drama",
        "release_date": date(2010, 1, 1),
        "duration": None,
        "director": ("Tom", "Hooper"),
        "actors": [
            ("Colin", "Firth"),
            ("Geoffrey", "Rush"),
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzU5MjEwMTg2Nl5BMl5BanBnXkFtZTcwNzM3MTYxNA@@._V1_.jpg",
    },
    {
        "title": "Argo",
        "genre_name": "Thriller",
        "release_date": date(2012, 1, 1),
        "duration": None,
        "director": ("Ben", "Affleck"),
        "actors": [
            ("Ben", "Affleck"),
            ("Bryan", "Cranston"),
        ],
        "poster_url": "https://m.media-amazon.com/images/I/913Cd3xOooL._AC_UF894,1000_QL80_.jpg",
    },
]


def get_or_create_person(model, first_name, last_name):
    person, _ = model.objects.get_or_create(
        first_name=first_name,
        last_name=last_name,
    )
    return person


class Command(BaseCommand):
    help = "Seed the database with sample directors, actors, and movies."

    def handle(self, *args, **options):
        with transaction.atomic():
            created_count = 0
            for data in MOVIES:
                director = get_or_create_person(Director, *data["director"])
                movie, created = Movie.objects.get_or_create(
                    title=data["title"],
                    defaults={
                        "description": "",
                        "release_date": data["release_date"],
                        "duration": data["duration"],
                        "poster_url": data["poster_url"],
                        "genre_name": data["genre_name"],
                        "director": director,
                    },
                )
                if not created:
                    movie.release_date = data["release_date"]
                    movie.genre_name = data["genre_name"]
                    movie.director = director
                    if data["duration"] is not None:
                        movie.duration = data["duration"]
                    if data["poster_url"] is not None:
                        movie.poster_url = data["poster_url"]
                    movie.save()

                actor_list = [
                    get_or_create_person(Actor, *actor)
                    for actor in data["actors"]
                ]
                movie.actors.set(actor_list)

                if created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created_count} movies, {Director.objects.count()} directors, "
                f"{Actor.objects.count()} actors."
            )
        )
