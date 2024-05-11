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

## Spuštění
`python manage.py runserver` -- spustí standardně na adrese http://127.0.0.1:8000/

Pokud potřebujeme spustit více serverů najednou, tak můžeme změnit port:
`python manage.py runserver 8001` -- server poběží na portu 8001, tedy na adrese http://127.0.0.1:8001/


