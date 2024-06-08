from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CASCADE, TextField, DateField


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    birth_date = DateField(null=True, blank=True)
    biography = TextField(null=True, blank=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user}"
