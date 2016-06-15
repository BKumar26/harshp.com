from django.shortcuts import render

from hobbies.models import Director
from hobbies.models import Actor
from hobbies.models import Scriptwriter
from hobbies.models import Cinematographer
from hobbies.models import Composer
from hobbies.models import Movie
from hobbies.models import MovieList
from hobbies.models import MovieListEntry
from hobbies.models import MovieQuote
from hobbies.models import TVShow
from hobbies.models import TVShowSeason
from hobbies.models import TVShowList
from hobbies.models import TVShowListEntry
from hobbies.models import TVShowQuote


# directors
# order by title
Director.objects.order_by('name')
# contains name
Director.objects.filter(person__name__icontains=param)
# by name
Director.objects.get(person__name__iexact=param)
# order by ratings:
# imdb rating
Director.objects.order_by('-imdbrating')
# metascore
Director.objects.order_by('-metascore')
# tomatometer
Director.objects.order_by('-tomatometer')
# hpl
Director.objects.order_by('-hpl')
# favorites
Director.objects.order_by('favorite', 'person__name')


# actors
Actor.objects.order_by('name')
# scriptwriters
Scriptwriter.objects.order_by('name')
# cinematographers
Cinematographer.objects.order_by('name')
# composers
Composer.objects.order_by('name')


# all movies ordered by date - most recent first
Movie.objects.filter(wishlist=False)\
    .order_by('-completed', '-date_start', 'title')

# movies I wish to see
Movie.objects.filter(wishlist=True)\
    .order_by('title')

# movie lists
MovieList.objects.order_by('title')

# order by rating
# imdb
Movie.objects.order_by('-imdbrating', 'title')
# metascore
Movie.objects.order_by('-metascore', 'title')
# tomatometer
Movie.objects.order_by('-tomatometer', 'title')
# release date
Movie.objects.order_by('-release_date', 'title')
# unwatched order by rating
Movie.objects.filter(wishlist=True)\
    .order_by('-tomatometer', '-imdbrating', 'metascore', 'title')

# movie lists
MovieList.objects.order_by('title')
