from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, IntegerField, DateField, TextField, DateTimeField


# Create your models here.


class Genre(Model):
    name = CharField(max_length=20)


class Movie(Model):
    title = CharField(max_length=64)
    genre = ForeignKey(Genre, on_delete=DO_NOTHING)
    rating = IntegerField()
    released = DateField()
    description = TextField()
    created = DateTimeField(auto_now_add=True)
