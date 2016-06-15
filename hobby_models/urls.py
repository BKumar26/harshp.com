"""urls config for blog at harshp_com"""

from django.conf.urls import include, url

from . import views

film_urlpatterns = [
    # people collective
    url(r'^people/$', views.film.people, name='people'),
    url(r'^people/actors/$', views.film.actors, name='actors'),
    url(r'^people/directors/$', views.film.directors, name='directors'),
    url(
        r'^people/scriptwriters/$',
        views.film.scriptwriters, name='scriptwriters'),
    url(
        r'^people/cinematographers/$',
        views.film.cinematographers, name='cinematographers'),
    url(
        r'^people/composers/$',
        views.film.composers, name='composers'),
    # people singular
    url(
        r'^people/actors/(?P<slug>[\w-_]+)/$',
        views.film.actor, name='actors'),
    url(
        r'^people/directors/(?P<slug>[\w-_]+)/$',
        views.film.director, name='director'),
    url(
        r'^people/scriptwriters/(?P<slug>[\w-_]+)/$',
        views.film.scriptwriter, name='scriptwriter'),
    url(
        r'^people/cinematographers/(?P<slug>[\w-_]+)/$',
        views.film.cinematographer, name='cinematographer'),
    url(
        r'^people/composers/(?P<slug>[\w-_]+)/$',
        views.film.composer, name='composer'),
    # movies
    url(r'^movies/$', views.film.movies, name='movies'),
    url(r'^movies/lists/$', views.film.movie_lists, name='movie_lists'),
    url(
        r'^movies/lists/(?P<slug>[\w-_]+)/$',
        views.film.movie_list, name='movie_list'),
    url(r'^movies/quotes/$', views.film.quotes, name='quote'),
    url(
        r'^movies/quotes/(?P<pk>[\w-_]+)/$',
        views.film.quote, name='quote'),

    url(r'^movies/(?P<slug>[\w-_]+)/$', views.film.movie, name='movie'),
    url(r'^tvshows/$', views.film.tvshows, name='tvshows'),
    url(r'^tvshows/(?P<slug>[\w-_]+)/$', views.film.tvshow, name='tvshow'),
]

food_urlpatterns = [
]

photography_urlpatterns = [
]

music_urlpatterns = [
]

games_urlpatterns = [
]

books_urlpatterns = [
]

hobbies_urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^film/', include(film_urlpatterns, namespace='film')),
    url(r'^food/', include(food_urlpatterns, namespace='food')),
    url(r'^photography/', include(
        photography_urlpatterns, namespace='photography')),
    url(r'^music/', include(music_urlpatterns, namespace='music')),
    url(r'^games/', include(games_urlpatterns, namespace='games')),
    url(r'^books/', include(books_urlpatterns, namespace='books')),
]

urlpatterns = [
    url(r'', include(hobbies_urlpatterns, namespace='hobbies')),
]

handler404 = 'harshp_com.views.handler404'
