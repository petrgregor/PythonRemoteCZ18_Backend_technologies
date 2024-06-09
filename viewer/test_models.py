import datetime

from django.test import TestCase

from viewer.models import *


class MovieModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        movie = Movie.objects.create(
            title="Originální název",
            title_cz="Český název",
            rating=8,
            released=datetime.date(year=2010, month=5, day=6),
            length=123,
            description="Popis filmu"
        )
        genre_drama = Genre.objects.create(name="Drama")
        genre_comedy = Genre.objects.create(name="Comedy")
        movie.genres.add(genre_drama)
        movie.genres.add(genre_comedy)
        country_cz = Country.objects.create(name="Czech")
        country_sk = Country.objects.create(name="Slovak")
        movie.countries.add(country_cz)
        movie.countries.add(country_sk)
        director1 = Creator.objects.create(
            name="Jan",
            surname="Juřička",
            birth_date=datetime.date(year=1950, month=6, day=10),
            birth_place="Místo narození",
            country=country_cz,
            sex=Sex.MAN,
            biography="Biografie prvního režiséra."
        )
        director2 = Creator.objects.create(
            name="Pavel",
            surname="Novák",
            birth_date=datetime.date(year=1978, month=12, day=29),
            birth_place="Praha",
            country=country_cz,
            sex=Sex.MAN,
            biography="Biografie druhého režiséra."
        )
        movie.directors.add(director1)
        movie.directors.add(director2)
        actor1 = Creator.objects.create(
            name="Pavlína",
            surname="Svobodová",
            birth_date=datetime.date(year=1966, month=5, day=8),
            birth_place="Místo narození",
            country=country_cz,
            sex=Sex.WOMAN,
            biography="Biografie první herečky."
        )
        actor2 = Creator.objects.create(
            name="Radek",
            surname="Novotný",
            birth_date=datetime.date(year=1985, month=9, day=5),
            birth_place="Bratislava",
            country=country_sk,
            sex=Sex.MAN,
            biography="Biografie druhého herce."
        )
        movie.actors.add(actor1)
        movie.actors.add(actor2)
        movie.save()

    def setUp(self):
        print('-'*80)

    def test_movie_str(self):
        movie = Movie.objects.get(id=1)
        print(f"test_movie_str: {movie}")
        self.assertEqual(movie.__str__(), "Originální název (2010)")

    def test_title(self):
        movie = Movie.objects.get(id=1)
        print(f"test_title: {movie.title}")
        self.assertEqual(movie.title, "Originální název")

    def test_movie_genres(self):
        movie = Movie.objects.get(id=1)
        number_of_genres = movie.genres.count()
        print(f"test_movie_genres: {number_of_genres}")
        self.assertEqual(number_of_genres, 2)

    def test_movie_countries(self):
        movie = Movie.objects.get(id=1)
        number_of_countries = movie.countries.count()
        print(f"test_movie_countries: {number_of_countries}")
        self.assertEqual(number_of_countries, 2)

    def test_movie_directors(self):
        movie = Movie.objects.get(id=1)
        number_of_directors = movie.directors.count()
        print(f"test_movie_directors: {number_of_directors}")
        self.assertEqual(number_of_directors, 2)

    def test_movie_actors(self):
        movie = Movie.objects.get(id=1)
        number_of_actors = movie.actors.count()
        print(f"test_movie_actors: {number_of_actors}")
        self.assertEqual(number_of_actors, 2)


# TODO: test Creator
# TODO: test Genre
# TODO: test Country
