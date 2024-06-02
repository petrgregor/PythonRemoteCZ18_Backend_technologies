from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, IntegerField, DateField, TextField, \
    DateTimeField, ManyToManyField, TextChoices


class Genre(Model):
    name = CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Country(Model):
    name = CharField(max_length=64)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Sex(TextChoices):
    MAN = 'man'
    WOMAN = 'woman'
    NON_BINARY = 'non-binary'


class Creator(Model):
    name = CharField(max_length=32)
    surname = CharField(max_length=32)
    birth_date = DateField(null=True, blank=True)
    death_date = DateField(null=True, blank=True)
    birth_place = CharField(max_length=64, null=True, blank=True)
    country = ForeignKey(Country, null=True, blank=True, on_delete=DO_NOTHING)
    sex = CharField(max_length=10, choices=Sex.choices, null=True, blank=True)
    biography = TextField(null=True, blank=True)

    class Meta:
        ordering = ['surname', 'name', 'birth_date']

    def __str__(self):
        return f"{self.name} {self.surname} ({self.birth_date.year})"


class Movie(Model):
    title = CharField(max_length=64)
    title_cz = CharField(max_length=64, null=True, blank=True)
    # genre = ForeignKey(Genre, on_delete=DO_NOTHING)
    genres = ManyToManyField(Genre, blank=True, related_name='movies')
    countries = ManyToManyField(Country, blank=True, related_name='movies')
    directors = ManyToManyField(Creator, blank=True, related_name='directed_movies')
    actors = ManyToManyField(Creator, blank=True, related_name='acting_in_movies')
    rating = IntegerField()
    released = DateField()
    length = IntegerField(null=True, blank=True)
    description = TextField()
    created = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title', 'released']

    def __str__(self):
        return f'{self.title} ({self.released.year})'
