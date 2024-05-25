from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, IntegerField, DateField, TextField, DateTimeField


# Create your models here.


class Genre(Model):
    name = CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Movie(Model):
    title = CharField(max_length=64)
    genre = ForeignKey(Genre, on_delete=DO_NOTHING)
    rating = IntegerField()
    released = DateField()
    description = TextField()
    created = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title', 'released']

    def __str__(self):
        return f'{self.title} ({self.released.year})'
