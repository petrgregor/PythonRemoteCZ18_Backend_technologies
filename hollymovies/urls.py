"""hollymovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from viewer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello/', hello),
    path('hello2/<s>/', hello2),  # User data: Regular expression, eg. http://127.0.0.1:8000/hello2/cruel/
    path('hello3/', hello3),      # User data: URL encoding, eg. http://127.0.0.1:8000/hello3/?s=cruel
    path('hello4/', hello4),
    path('hello5/<s0>/', hello5),

    path('', home, name='home'),  # home
    #path('genres/', genres, name='genres'),
    path('genres/', GenresView.as_view(), name='genres'),
    path('genre/<pk>/', genre, name='genre'),
    #path('movies/', movies, name='movies'),
    path('movies/', MoviesView.as_view(), name='movies'),
    path('movies_by_rating/', movies_by_rating, name='movies_by_rating'),
    path('movie/<pk>/', movie, name='movie'),
]
