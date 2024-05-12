# Django

## Instalace
Django nainstalujeme příkazem (verze 4.1.1):
`python -m pip install django==4.1.1`

DŮLEŽITÉ: Všichni v týmu musí mít stejnou verzi.

## Vytvoření nového projektu
Vytvoříme nový Django projekt příkazem:
`django-admin startproject hollymovies .`

V `.\hollymovies\setting.py` máme nastavení našeho projektu.

V `.\hollymovies\path.py` máme nastavené cesty.

## Seznam nainstalovaných balíčků
`pip freeze > requirements.txt`

## GitHub

Následně zveřejnit projekt na GitHub -> pozvat ostatní členy týmu jako spolupracovníky.

## Spuštění
`python manage.py runserver` -- spustí standardně na adrese http://127.0.0.1:8000/

Pokud potřebujeme spustit více serverů najednou, tak můžeme změnit port:
`python manage.py runserver 8001` -- server poběží na portu 8001, tedy na adrese http://127.0.0.1:8001/

## Vytvoření aplikace
`python manage.py startapp viewer`

- migrations -- složka, která obsahuje migrace
- admin.py -- administrační část
- apps.py -- nastavení aplikace (necháme beze změn)
- models.py -- zde jsou definované modely (tabulky databáze)
- tests.py -- zde řešíme testování (ukážeme si později)
- views.py -- zde bude logika (propojení databáze a template)

### Registrace aplikace
Aplikaci můsume zaregistrovat v souboru `.\hollymovies\settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # our applications
    'viewer',
]
```

## ORM

Modely vytváříme v souboru `models.py` v dané aplikaci.

DŮLEŽITÉ: Po každé změně v modelech (tj. v souboru `models.py`) musíme migrovat databázi:

- vytvoření migračního skriptu: `python manage.py makemigrations`
- aplikujeme migraci: `python manage.py migrate`

DŮLEŽITÉ: Migrační skripty vkládáme do repozitáře (git), databázi ne (obsahuje mimo jiné i hesla všech uživatelů)

## shell

Pro rychlou práci s databází lze využít Django shell: `python manage.py shell`

## Vytvoření superuživatele (admin)
`python manage.py createsuperuser`

Na stránce http://127.0.0.1:8000/admin je administrační panel.

## Export a import dat

Export dat:
`python manage.py dumpdata viewer --output fixtures.json`,
kde 'viewer' je název aplikace, ze které chci exportovat data.
Data se uloží ve formátu json.

Následně import dat z formátu json do databáze:
`python manage.py loaddata fixtures.json`

DŮLEŽITÉ: Při importu dát pozor na id (pk), protože se do databáze vloží s těmito id a mohou tedy přepsat stávající data.

## Queries

### .get()
Vrací jednu instanci nalezeného záznamu v databázi. 

### .filter()
Vrací kolekci instancí nalezených záznamů.

`Movie.objects.filter(title="The Green Mile")`

`Movie.objects.filter(rating=5)`

`Movie.objects.filter(rating__gt=4)`   `__gt` => "větší než" 

`Movie.objects.filter(rating__gte=4)`  `__gte` => "větší rovno"

`Movie.objects.filter(rating__lt=4)`   `__lt` => "menší než"

`Movie.objects.filter(rating__lte=4)`  `__lte` => menší rovno

`drama = Genre.objects.get(name='Drama')`

`Movie.objects.filter(genre=drama)`

`Movie.objects.filter(genre__name="Drama")`

`Movie.objects.filter(released__year=1994)`

`Movie.objects.filter(title__contains="Gump")`

`Movie.objects.filter(title__in=['Se7en', 'Fight Club'])`  # „Se7en” and „Fight Club”

`Movie.objects.exclude(released__year=1994)`

`Movie.objects.filter(title="Avatar").exists()` -- test, zda existuje nějaký záznam

`Movie.objects.exclude(released__year=1994).count()` -- vrátí počet vyhovujícíh záznamů

`Movie.objects.all().order_by('released')` -- uspořádáme dle data natočení vzestupně

`Movie.objects.all().order_by('-released')` -- sestupně

## Data manipulation

### CREATE
`Genre.objects.create(name='Documentary')`

```python
genre = Genre(name='Comedy')
genre.save()
```

### UPDATE 

`Movie.objects.filter(released__year=2000).update(rating=5)`

```python
pulp_fiction = Movie.objects.get(title='Pulp Fiction')
pulp_fiction.rating = 7
pulp_fiction.save()
```

### DELETE
`Movie.objects.filter(title__contains='Godfather').delete()`

## Domácí úkol
Filtrovat filmy podle žánru:

- template -- movies.html
- view -- zde bude použit filtr dle žánru
- url -- 'genre/<genre>/'
- seznam žánrů bude klikací -- když kliknu na žánr, otevře se stránka se seznamem filmů daného žánru

