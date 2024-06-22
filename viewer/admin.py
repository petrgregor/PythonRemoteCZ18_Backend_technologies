from django.contrib import admin
from django.contrib.admin import ModelAdmin

from viewer.models import Genre, Movie, Country, Creator, Image


class MovieAdmin(ModelAdmin):

    @staticmethod
    def released_year(obj):
        return obj.released.year

    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description=None)

    ordering = ['title']
    list_display = ['id', 'title', 'title_cz', 'released_year']
    list_display_links = ['id', 'title', 'title_cz']
    list_per_page = 10
    list_filter = ['genres', 'countries']
    search_fields = ['title', 'title_cz']
    actions = ['cleanup_description']

    fieldsets = [
        (
            'Movie',
            {
                'fields': ['title', 'created']
            }
        ),
        (
            'External Information',
            {
                'fields': ['genres', 'released'],
                'description': (
                    'These fields are going to be filled with data parsed '
                    'from external databases.'
                )
            }
        ),
        (
            'User Information',
            {
                'fields': ['rating', 'description'],
                'description': 'These fields are intended to be filled in by our users.'
            }
        )
    ]
    readonly_fields = ['created']


class CreatorAdmin(ModelAdmin):

    @staticmethod
    def capitalize_name_surname(modeladmin, request, queryset):
        for obj in queryset:
            obj.name = obj.name.capitalize()
            obj.surname = obj.surname.capitalize()
            obj.save()

    fieldsets = [
        (
            None,
            {
                'fields': ['name', 'surname', 'sex', 'country']
            }
        ),
        (
            "Birth",
            {
                'fields': ['birth_date', 'birth_place']
            }
        ),
        (
            "Death",
            {
                'fields': ['death_date']
            }
        ),
        (
            "Biography",
            {
                'fields': ['biography']
            }
        )
    ]

    ordering = ['surname', 'name']
    list_display = ['id', 'name', 'surname', 'birth_date', 'death_date', 'age']
    list_display_links = ['id', 'name', 'surname']
    list_per_page = 10
    list_filter = ['sex', 'country']
    search_fields = ['surname', 'name', 'biography']
    actions = ['capitalize_name_surname']


admin.site.register(Country)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Image)
