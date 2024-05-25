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


def movies_by_rating(request):
    result = Movie.objects.all().order_by('-rating', 'title')
    return render(request,
                  'movies_by_rating.html',
                  {'title': 'List of movies by rating', 'movies': result})


# DONE: detailní informace o jednom konkrétním filmu (id zadané v adrese)
# DONE: template
# DONE: view
# DONE: url
# DONE: odkaz z názvu filmu v seznamu filmů (movies)
def movie(request, pk):
    if Movie.objects.filter(id=pk).exists():  # otestujeme, zda film existuje
        result = Movie.objects.get(id=pk)
        return render(request, 'movie.html', {'title': result.title, 'movie': result})

    # pokud daný film neexistuje, vypíšeme seznam všech filmů
    # TODO: lepší by bylo vypsat chybovou hlášku
    result = Movie.objects.all().order_by('title')
    return render(request, 'movies.html', {'title': 'Movies', 'movies': result})


def genre(request, pk):
    if Genre.objects.filter(id=pk).exists():
        genre = Genre.objects.get(id=pk)
        items = Movie.objects.filter(genre=genre)
        return render(request, "genre.html", {'movies': items, 'genre': genre})

    return genres(request)
