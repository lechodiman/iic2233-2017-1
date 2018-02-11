from datetime import datetime as dt


def set_id():
    i = 0
    while True:
        yield i
        i += 1


class Cast:
    def __init__(self, movie_title, name, character):
        self.name = name
        self.movie = movie_title
        self.character = character


class Movie:
    get_id = set_id()

    def __init__(self, title, rating, release, *args):
        self.id = next(Movie.get_id)
        self.title = title
        self.rating = float(rating)
        self.release = dt.strptime(release, '%Y-%m-%d')  # 2015-03-04
        self.genres = list(args)

    def __repr__(self):
        return str(self.title)

    def __lt__(self, other):
        return self.rating < other.rating


def popular(rating, movies_list):
    movies_filter = filter(lambda movie: movie.rating >= rating, movies_list)
    for movie in movies_filter:
        print(movie)


def with_genres(n, movies_list):
    movies_filter = filter(lambda movie: len(movie.genres) >= n, movies_list)
    for movie in movies_filter:
        print(movie)


def tops_of_genre(genre, movies_list):
    # Dado genre retorne las 10 peliculas con mejor rating ordenadas descendentemente
    movies_filter = (movie for movie in sorted(movies_list) if genre in movie.genres)
    for i in range(10):
        print(next(movies_filter))


def actor_rating(actor, cast_list, movies_list):
    names = [cast.movie for cast in cast_list if cast.name == actor]
    movies = [movie for movie in movies_list if movie.title in names]
    ratings = [movie.rating for movie in movies]
    avg = sum(ratings) / len(ratings) if len(ratings) != 0 else 0
    return avg


def compare_actors(actor1, actor2, cast_list, movies_list):
    # Retorna el actor con mejor valor de actor_rating
    if actor_rating(actor1, cast_list, movies_list) != actor_rating(actor2, cast_list, movies_list):
        if actor_rating(actor1, cast_list, movies_list) > actor_rating(actor2, cast_list, movies_list):
            print(actor1)
        else:
            print(actor2)
    else:
        print("Son iguales")


def movies_of(actor, cast_list):
    # Retorna lista con tuplas de forma (Pelicula, personaje) del actor
    movies = [(cast.movie, cast.character) for cast in cast_list if cast.name == actor]
    for tpl in movies:
        print(tpl)


def from_year(año, movies_list):
    # Retorna todas las peliculas estrenadas ese año
    movies_filtered = filter(lambda movie: movie.release.year == int(año), movies_list)
    for movie in movies_filtered:
        print(movie)


with open("movies.txt", "r") as rf:
    movies_list = []
    for line in rf:
        columns = line.strip().split(",")
        title = str(columns[1])
        rating = float(columns[2])
        date = columns[3]
        genres = columns[4:]
        movie = Movie(title, rating, date, *genres)
        movies_list.append(movie)


with open("cast.txt", "r") as rf:
    cast_list = []
    for line in rf:
        columns = line.strip().split(",")
        name = columns[1]
        movie = columns[0]
        character = columns[2]
        cast = Cast(movie, name, character)
        cast_list.append(cast)

# Consultas
popular(9, movies_list)
print("-" * 25)
with_genres(3, movies_list)
print("-" * 25)
tops_of_genre("Adventure", movies_list)
print("-" * 25)
actor_rating("Brad Garrett", cast_list, movies_list)
print("-" * 25)
compare_actors("Brad Garrett", "Allison Janney", cast_list, movies_list)
print("-" * 25)
movies_of("Brad Garrett", cast_list)
print("-" * 25)
from_year(2015, movies_list)
