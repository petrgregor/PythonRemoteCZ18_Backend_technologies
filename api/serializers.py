from rest_framework import serializers

from viewer.models import Movie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        #fields = ['title', 'title_cz', 'description']
        fields = '__all__'

# TODO: CreatorSerializer
