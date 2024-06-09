import datetime

from django.test import TestCase

from viewer.models import *
from viewer.views import GenreModelForm, MovieModelForm


class GenreFormTest(TestCase):

    def test_genre_form_is_valid(self):
        form = GenreModelForm(
            data={'name': '  comedy   '}
        )
        print(f"test_genre_form_is_valid: {form.data}")
        self.assertTrue(form.is_valid())


class MovieFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name="Drama")
        Genre.objects.create(name="Comedy")
        country_cz = Country.objects.create(name="Czech")
        country_sk = Country.objects.create(name="Slovak")
        Creator.objects.create(
            name="Jan",
            surname="Juřička",
            birth_date=datetime.date(year=1950, month=6, day=10),
            birth_place="Místo narození",
            country=country_cz,
            sex=Sex.MAN,
            biography="Biografie prvního režiséra."
        )
        Creator.objects.create(
            name="Pavel",
            surname="Novák",
            birth_date=datetime.date(year=1978, month=12, day=29),
            birth_place="Praha",
            country=country_cz,
            sex=Sex.MAN,
            biography="Biografie druhého režiséra."
        )
        Creator.objects.create(
            name="Pavlína",
            surname="Svobodová",
            birth_date=datetime.date(year=1966, month=5, day=8),
            birth_place="Místo narození",
            country=country_cz,
            sex=Sex.WOMAN,
            biography="Biografie první herečky."
        )
        Creator.objects.create(
            name="Radek",
            surname="Novotný",
            birth_date=datetime.date(year=1985, month=9, day=5),
            birth_place="Bratislava",
            country=country_sk,
            sex=Sex.MAN,
            biography="Biografie druhého herce."
        )

    def test_movie_form_is_valid(self):
        form = MovieModelForm(
            data={
                'title': '   Název filmu   ',
                'title_cz': 'Český název filmu',
                'genres': ['1'],
                'countries': ['2'],
                'directors': ['1', '2'],
                'actors': ['3', '4'],
                'rating': '6',
                'released': '2020-05-08',
                'length': '123',
                'description': 'Popis filmu',
                'clicked': '2'
            }
        )
        print(f"\ntest_movie_form_is_valid: {form.data}")
        self.assertTrue(form.is_valid())

    def test_movie_form_is_not_valid_released_month(self):
        form = MovieModelForm(
            data={
                'title': '   Název filmu   ',
                'title_cz': 'Český název filmu',
                'genres': ['1'],
                'countries': ['2'],
                'directors': ['1', '2'],
                'actors': ['3', '4'],
                'rating': '6',
                'released': '2020-13-08',  # nevalidní datum
                'length': '123',
                'description': 'Popis filmu',
                'clicked': '2'
            }
        )
        print(f"\ntest_movie_form_is_not_valid_released_month: {form.data}")
        self.assertFalse(form.is_valid())

    def test_movie_form_is_not_valid_released_future(self):
        form = MovieModelForm(
            data={
                'title': '   Název filmu   ',
                'title_cz': 'Český název filmu',
                'genres': ['1'],
                'countries': ['2'],
                'directors': ['1', '2'],
                'actors': ['3', '4'],
                'rating': '6',
                'released': '2024-12-10',  # nevalidní datum
                'length': '123',
                'description': 'Popis filmu',
                'clicked': '2'
            }
        )
        print(f"\ntest_movie_form_is_not_valid_released_future: {form.data}")
        self.assertFalse(form.is_valid())

    def test_movie_form_is_not_valid_negative_length(self):
        form = MovieModelForm(
            data={
                'title': '   Název filmu   ',
                'title_cz': 'Český název filmu',
                'genres': ['1'],
                'countries': ['2'],
                'directors': ['1', '2'],
                'actors': ['3', '4'],
                'rating': '6',
                'released': '2024-02-10',
                'length': '-123',  # nevalidní délka
                'description': 'Popis filmu',
                'clicked': '2'
            }
        )
        print(f"\ntest_movie_form_is_not_valid_negative_length: {form.data}")
        self.assertFalse(form.is_valid())


# TODO test Creator form
# TODO test Country form
