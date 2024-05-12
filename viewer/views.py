from django.http import HttpResponse
from django.shortcuts import render

from viewer.models import Genre, Movie


# Create your views here.


# view defined as a function
def hello(request):
    return HttpResponse('Hello, world!')


# User data
# Regular expression
def hello2(request, s):
    return HttpResponse(f'Hello, {s} world!')


# User data
# URL encoding
def hello3(request):
    s = request.GET.get('s', '')
    return HttpResponse(f'Hello, {s} world!')


def hello4(request):
    adjectives = ['nice', 'beautiful', 'cruel', 'blue', 'sunny']
    context = {'adjectives': adjectives}
    return render(
        request,   # předáváme na další stránku request (obsahuje např. data o přihlášeném uživateli)
        template_name='hello.html',  # tato teplate to zobrazí
        context=context   # posíláme data (jako slovník)
    )


def hello5(request, s0):
    s1 = request.GET.get('s1', '')
    return render(
        request,
        template_name='hello.html',
        context={'adjectives': [s0, s1, 'beautiful', 'wonderful']}
    )


def home(request):
    return render(request, 'home.html', {'title': 'Welcome to HollyMovies'})


def genres(request):
    result = Genre.objects.all().order_by('name')
    return render(request, 'genres.html', {'title': 'List of genres', 'genres': result})


def movies(request):
    result = Movie.objects.all().order_by('title')
    return render(request, 'movies.html', {'title': 'List of movies', 'movies': result})
