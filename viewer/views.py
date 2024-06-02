import re
from concurrent.futures._base import LOGGER
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, IntegerField, DateField, ModelChoiceField, Textarea, ModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from viewer.models import Genre, Movie, Creator


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


@login_required
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


def movies_by_popularity(request):
    result = Movie.objects.all().order_by('-clicked', 'title')
    return render(request,
                  'movies_by_popularity.html',
                  {'title': 'List of movies by popularity', 'movies': result})



# DONE: detailní informace o jednom konkrétním filmu (id zadané v adrese)
# DONE: template
# DONE: view
# DONE: url
# DONE: odkaz z názvu filmu v seznamu filmů (movies)
def movie(request, pk):
    if Movie.objects.filter(id=pk).exists():  # otestujeme, zda film existuje
        result = Movie.objects.get(id=pk)
        # TODO: počítat kliknutí
        result.clicked += 1
        result.save()
        return render(request, 'movie.html', {'title': result.title, 'movie': result})

    # pokud daný film neexistuje, vypíšeme seznam všech filmů
    # TODO: lepší by bylo vypsat chybovou hlášku
    result = Movie.objects.all().order_by('title')
    return render(request,
                  'movies.html',
                  {'title': 'Movies', 'movies': result})


def genre(request, pk):
    if Genre.objects.filter(id=pk).exists():
        genre = Genre.objects.get(id=pk)
        items = genre.movies.all()  #Movie.objects.filter(genre=genre)
        return render(request,
                      "genre.html",
                      {'movies': items, 'genre': genre})

    return genres(request)


""" Class-Based Views """

""" 
# první verze pomocí View - jen se funkce vloží do třídy
class MoviesView(View):
    def get(self, request):
        result = Movie.objects.all().order_by('title')
        return render(request,
                      'movies.html',
                      {'title': 'List of movies', 'movies': result})
"""


"""
# druhá verze pomocí TemplateView - již potřebujeme jen zada jméno tamplaty a data
class MoviesView(TemplateView):
    template_name = 'movies.html'
    extra_context = {'title': 'List of movies',
                     'movies': Movie.objects.all().order_by('title')}
"""


# třetí verze pomocí ListView (zobrazení seznamu) - již definujeme jenom template a model
class MoviesView(ListView):
    template_name = 'movies2.html'
    model = Movie


# druhá verze pomocí TemplateView - již potřebujeme jen zada jméno tamplaty a data
class MoviesByRatingView(TemplateView):
    template_name = 'movies_by_rating.html'
    extra_context = {'title': 'List of movies by rating',
                     'movies': Movie.objects.all().order_by('-rating', 'title')}


class MoviesByPopularityView(TemplateView):
    template_name = 'movies_by_popularity.html'
    extra_context = {'title': 'List of movies by popularity',
                     'movies': Movie.objects.all().order_by('-clicked', 'title')}


class MovieView(View):
    def get(self, request, pk):
        if Movie.objects.filter(id=pk).exists():  # otestujeme, zda film existuje
            result = Movie.objects.get(id=pk)
            return render(request, 'movie.html', {'title': result.title, 'movie': result})

        # pokud daný film neexistuje, vypíšeme seznam všech filmů
        # TODO: lepší by bylo vypsat chybovou hlášku
        result = Movie.objects.all().order_by('title')
        return render(request,
                      'movies.html',
                      {'title': 'Movies', 'movies': result})


"""
class GenresView(View):
    def get(self, request):
        result = Genre.objects.all().order_by('name')
        return render(request,
                      'genres.html',
                      {'title': 'List of genres', 'genres': result})
"""


"""
class GenresView(TemplateView):
    template_name = 'genres.html'
    extra_context = {'title': 'List of genres', 'genres': Genre.objects.all()}
"""


class GenresView(ListView):
    template_name = 'genres2.html'
    model = Genre


class CreatorsView(ListView):
    template_name = 'creators.html'
    model = Creator
    context_object_name = 'creators'


class CreatorView(View):
    def get(self, request, pk):
        if Creator.objects.filter(id=pk).exists():  # otestujeme, zda film existuje
            result = Creator.objects.get(id=pk)
            return render(request, 'creator.html', {'title': result, 'creator': result})

        result = Creator.objects.all()
        return render(request,
                      'creators.html',
                      {'title': 'Creators', 'creators': result})


""" Forms """

""" Validators """


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized.')


class PastMonthField(DateField):

    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Only past dates allowed here.')

    def clean(self, value):
        result = super().clean(value)
        return date(year=result.year, month=result.month, day=1)


class MovieForm(Form):
    title = CharField(max_length=64)
    genre = ModelChoiceField(queryset=Genre.objects)
    rating = IntegerField(min_value=1, max_value=10)
    released = DateField()
    description = CharField(widget=Textarea, required=False)

    def clean_title(self):
        initial_data = super().clean()  # původní data ve formuláři od uživatele
        initial = initial_data['title']  # původní title od uživatele
        return initial.strip()  # odtraníme prázdné znaky na začátku a konci textu

    def clean_description(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'Commedy' and result['rating'] > 5:
            self.add_error('genre', '')
            self.add_error('rating', '')
            raise ValidationError(
                "Commedies aren't so good to be rated over 5."
            )
        return result


class MovieModelForm(ModelForm):

    class Meta:
        model = Movie       # z kterého modelu bude brát informace
        #fields = ['genre', 'title']  # které položky chceme ve formuláři zobrazit
        #exclude = ['description']    # které položky nechceme zobrazit
        fields = '__all__'

    title = CharField(validators=[capitalized_validator])
    rating = IntegerField(min_value=1, max_value=10)
    released = PastMonthField()

    def clean_title(self):
        initial_data = super().clean()  # původní data ve formuláři od uživatele
        initial = initial_data['title']  # původní title od uživatele
        return initial.strip()  # odtraníme prázdné znaky na začátku a konci textu

    def clean_description(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        """if result['genre'].name == 'Commedy' and result['rating'] > 5:
            self.add_error('genre', '')
            self.add_error('rating', '')
            raise ValidationError(
                "Commedies aren't so good to be rated over 5."
            )"""
        return result


class MovieFormView(FormView):
    template_name = 'form.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movie_create')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Movie.objects.create(
            title=cleaned_data['title'],
            genre=cleaned_data['genre'],
            rating=cleaned_data['rating'],
            released=cleaned_data['released'],
            description=cleaned_data['description']
        )
        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Movie
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'movie_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('movies')


class GenreModelForm(ModelForm):

    class Meta:
        model = Genre
        fields = '__all__'

    def clean_name(self):
        initial_data = super().clean()
        initial = initial_data['name'].strip()
        return initial.capitalize()


class GenreFormView(FormView):
    template_name = 'form.html'
    form_class = GenreModelForm
    success_url = reverse_lazy('genre_create')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Genre.objects.create(name=cleaned_data['name'])
        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class GenreCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = GenreModelForm
    success_url = reverse_lazy('genres')


class GenreUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Genre
    form_class = GenreModelForm
    success_url = reverse_lazy('genres')


class GenreDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'genre_confirm_delete.html'
    model = Genre
    success_url = reverse_lazy('genres')


class CreatorModelForm(ModelForm):
    class Meta:
        model = Creator
        fields = '__all__'

    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.strip().capitalize()

    def clean_surname(self):
        initial = self.cleaned_data['surname']
        return initial.strip().capitalize()


class CreatorCreateView(CreateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')

    def form_invalid(self, form):
        LOGGER.warning('Invalid data in CreatorCreateView')
        return super().form_invalid(form)


class CreatorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Creator
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')


class CreatorDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'creator_confirm_delete.html'
    model = Creator
    success_url = reverse_lazy('creators')
