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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

import api.views
from accounts.views import SubmittableLoginView, SubmittablePasswordChangeView, SignUpView, ProfilesListView, \
    ProfileDetailView, ProfileUpdateView, ProfileDeleteView
from hollymovies import settings
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
    #path('genre/create/', GenreFormView.as_view(), name='genre_create'),
    path('genre/create/', GenreCreateView.as_view(), name='genre_create'),
    path('genre/update/<pk>/', GenreUpdateView.as_view(), name='genre_update'),
    path('genre/delete/<pk>/', GenreDeleteView.as_view(), name='genre_delete'),
    path('genre/<pk>/', genre, name='genre'),

    #path('movies/', movies, name='movies'),
    path('movies/', MoviesView.as_view(), name='movies'),
    #path('movies_by_rating/', movies_by_rating, name='movies_by_rating'),
    path('movies_by_rating/', MoviesByRatingView.as_view(), name='movies_by_rating'),
    path('movies_by_popularity/', MoviesByPopularityView.as_view(), name='movies_by_populartiy'),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movie/update/<pk>/', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<pk>/', MovieDeleteView.as_view(), name='movie_delete'),
    path('movie/<pk>/', MovieView.as_view(), name='movie'),
    path('creators/', CreatorsView.as_view(), name='creators'),
    path('creator/create/', CreatorCreateView.as_view(), name='creator_create'),
    path('creator/update/<pk>/', CreatorUpdateView.as_view(), name='creator_update'),
    path('creator/delete/<pk>/', CreatorDeleteView.as_view(), name='creator_delete'),
    path('creator/<pk>/', CreatorView.as_view(), name='creator'),
    path('image/create/', ImageCreateView.as_view(), name='image_create'),

    # authentication
    #path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),  # vlastní view pro login
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('accounts/', include('django.contrib.auth.urls')),  # defaultní view pro přihlašování/odhlašování/změnu hesla...

    path('accounts/profiles/', ProfilesListView.as_view(), name='profiles'),
    path('accounts/profile/<pk>/', ProfileDetailView.as_view(), name='profile'),
    path('accounts/profile/update/<pk>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('accounts/profile/delete/<pk>/', ProfileDeleteView.as_view(), name='profile_delete'),

    # API
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('api/movies/', api.views.MovieList.as_view()),
    path('api/movie/<pk>/', api.views.MovieDetail.as_view()),

    path('search/', search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
