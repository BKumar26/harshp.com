from django.db import models
from django.db import IntegrityError
import markdown
from subdomains.utils import reverse
from django.utils import timezone

from utils.meta_generator import create_meta
from utils.models import get_unique_slug
from sitebase.editors import EDITOR_TYPES
from sitebase.markdown_extensions import ext_formatting
from sitebase import ratings
from sitebase.models import Tag

from .hobby import Hobby, Person


class FilmPerson(models.Model):
    """A person with Film Industry affiliation.
    Acts as a base class for Actors, Directors, etc."""
    # ID
    imdb_id = models.CharField(max_length=12, unique=True, blank=True)
    tmdb_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    # score
    imdbrating = models.FloatField(default=0.0)
    metascore = models.PositiveSmallIntegerField(default=0.0)
    tomatometer = models.PositiveSmallIntegerField(default=0.0)
    # score - my metrics
    # a measure of how likely I am to like things by this person
    hpl_score = models.FloatField(default=0.0)
    # my favorite
    favorite = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True


class Director(FilmPerson):
    """Director"""
    person = models.OneToOneField(Person, related_name='director')

    class Meta:
        get_latest_by = 'pk'
        ordering = ['person__name']
        verbose_name = 'Director'
        verbose_name_plural = 'Directors'

    def __str__(self):
        return self.person.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:film:director',
            args=[self.person.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.person.name,
            description='Film Director',
            keywords=['harshp.com', 'movies', 'film', 'director'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(Director, self).save(*args, **kwargs)


class Actor(FilmPerson):
    """Actor"""
    person = models.OneToOneField(Person, related_name='actor')

    class Meta:
        get_latest_by = 'pk'
        ordering = ['person__name']
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

    def __str__(self):
        return self.person.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:film:actor',
            args=[self.person.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.person.name,
            description='Actor',
            keywords=['harshp.com', 'movies', 'film', 'actor'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(Actor, self).save(*args, **kwargs)


class Scriptwriter(FilmPerson):
    """Scriptwriter"""
    person = models.OneToOneField(Person, related_name='scriptwriter')

    class Meta:
        get_latest_by = 'pk'
        ordering = ['person__name']
        verbose_name = 'ScriptWriter'
        verbose_name_plural = 'ScriptWriters'

    def __str__(self):
        return self.person.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:film:scriptwriter',
            args=[self.person.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.person.name,
            description='ScriptWriter',
            keywords=['harshp.com', 'movies', 'film', 'scriptwriter'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(Scriptwriter, self).save(*args, **kwargs)


class Cinematographer(FilmPerson):
    """Cinematographer"""
    person = models.OneToOneField(Person, related_name='cinematographer')

    class Meta:
        get_latest_by = 'pk'
        ordering = ['person__name']
        verbose_name = 'Cinematographer'
        verbose_name_plural = 'Cinematographers'

    def __str__(self):
        return self.person.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:film:cinematographers',
            args=[self.person.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.person.name,
            description='Film Director',
            keywords=['harshp.com', 'movies', 'film', 'cinematographer'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(Cinematographer, self).save(*args, **kwargs)


class Composer(FilmPerson):
    """Film Music Composer"""
    person = models.OneToOneField(Person, related_name='composer')

    class Meta:
        get_latest_by = 'pk'
        ordering = ['person__name']
        verbose_name = 'Music Composer'
        verbose_name_plural = 'Music Composers'

    def __str__(self):
        return self.person.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:film:composer',
            args=[self.person.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.person.name,
            description='Film Music Composer',
            keywords=['harshp.com', 'movies', 'film', 'composer'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(Composer, self).save(*args, **kwargs)


class Movie(models.Model):
    """Movie"""

    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, db_index=True)

    # ID
    imdb_id = models.CharField(max_length=12, unique=True, blank=True)
    tmdb_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    # score
    imdbrating = models.FloatField(default=0.0)
    metascore = models.PositiveSmallIntegerField(default=0.0)
    tomatometer = models.PositiveSmallIntegerField(default=0.0)

    # cast
    directors = models.ManyToManyField(
        Director, related_name='movies', blank=True)
    actors = models.ManyToManyField(
        Actor, related_name='movies', blank=True)
    writers = models.ManyToManyField(
        Scriptwriter, related_name='movies', blank=True)
    cinematographers = models.ManyToManyField(
        Cinematographer, related_name='movies', blank=True)
    composers = models.ManyToManyField(
        Composer, related_name='movies', blank=True)

    # movie metadata
    poster = models.URLField(max_length=256, blank=True, null=True)
    # date_start = date_end == when I saw the movie
    release_date = models.DateField(blank=True, null=True)
    runtime = models.PositiveSmallIntegerField(blank=True, null=True)
    short_plot = models.TextField(blank=True)
    plot = models.TextField(blank=True)
    critic_consensus = models.TextField(blank=True)

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        get_latest_by = '-pk'
        ordering = ['title']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'hobbies:film:movie',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description='Movie',
            keywords=['harshp.com', 'movies', 'film'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Movie, self, 'title', title=self.title)
        return super(Movie, self).save(*args, **kwargs)


class MovieList(models.Model):
    """A collection of movies by me."""

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)
    movies = models.ManyToManyField(Movie, related_name='lists', blank=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['name']
        verbose_name = 'Movie List'
        verbose_name_plural = 'Movie Lists'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:film:movie_list',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.name,
            description='Movie List',
            keywords=['harshp.com', 'movies', 'film', 'list', 'collection'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                MovieList, self, 'name', name=self.name)
        return super(MovieList, self).save(*args, **kwargs)


class MovieQuote(models.Model):
    """A quote from a movie."""

    movie = models.ForeignKey(Movie, related_name='quotes')
    quote = models.TextField()
    favorite = models.BooleanField(default=False, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['movie__title']
        verbose_name = 'Movie Quote'
        verbose_name_plural = 'Movie Quotes'

    def __str__(self):
        return self.quote

    def get_absolute_url(self):
        return reverse(
            'hobbies:film:quote',
            args=[self.pk], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.quote,
            description='Movie Quote',
            keywords=['harshp.com', 'movies', 'film', 'quote'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(MovieQuote, self).save(*args, **kwargs)


class TVShow(models.Model):
    """TV Show
    Is representitative of the entire show, not any season."""

    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, db_index=True)

    # ID
    imdb_id = models.CharField(max_length=12, unique=True, blank=True)
    tmdb_id = models.PositiveIntegerField(unique=True, blank=True, null=True)

    # score
    imdbrating = models.FloatField(default=0.0)
    metascore = models.PositiveSmallIntegerField(default=0.0)
    tomatometer = models.PositiveSmallIntegerField(default=0.0)

    favorite = models.BooleanField(default=True, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['title']
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'hobbies:tvshow:tvshow',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description='TV Show',
            keywords=['harshp.com', 'tv', 'tv show'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(TVShow, self).save(*args, **kwargs)


class TVShowSeason(Hobby):
    """A Season of a particular TV Show"""

    tvshow = models.ForeignKey(TVShow, related_name='seasons')

    # ID
    imdb_id = models.CharField(max_length=12, unique=True, blank=True)
    tmdb_id = models.PositiveIntegerField(unique=True, blank=True, null=True)

    # cast
    directors = models.ManyToManyField(
        Director, related_name='tvshows', blank=True)
    actors = models.ManyToManyField(
        Actor, related_name='tvshows', blank=True)
    writers = models.ManyToManyField(
        Scriptwriter, related_name='tvshows', blank=True)
    cinematographers = models.ManyToManyField(
        Cinematographer, related_name='tvshows', blank=True)
    composers = models.ManyToManyField(
        Composer, related_name='tvshows', blank=True)

    # score
    imdbrating = models.FloatField(default=0.0)
    metascore = models.PositiveSmallIntegerField(default=0.0)
    tomatometer = models.PositiveSmallIntegerField(default=0.0)

    favorite = models.BooleanField(default=True, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    url = models.URLField(blank=True, null=True)

    # tv show metadata
    season = models.PositiveSmallIntegerField(default=1)
    poster = models.URLField(max_length=256, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    short_plot = models.TextField(blank=True)
    plot = models.TextField(blank=True)
    critic_consensus = models.TextField(blank=True)

    class Meta:
        get_latest_by = '-pk'
        ordering = ['tvshow__title', 'season']
        verbose_name = 'TV Show Season'
        verbose_name_plural = 'TV Show Seasons'

    def __str__(self):
        return self.tvshow.title + ' Season ' + self.season

    def get_absolute_url(self):
        return reverse(
            'hobbies:tvshow:season',
            args=[self.tvshow.slug, self.season], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=str(self),
            description: 'Season of TV Show',
            keyword['harshp.com', 'tv', 'tvshow', 'season'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            # check for duplicate season
            seasons = list(self.tvshow.seasons.order_by('season'))
            if self.season in seasons:
                raise IntegrityError('Duplicate season for tv show')
            for season in range(1, self.season):
                if season not in seasons:
                    raise IntegrityError('Previous seasons missing')
        return super(TVShowSeason, self).save(*args, **kwargs)


class TVShowList(models.Model):
    """A collection of tv shows by me."""

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)
    tvshows = models.ManyToManyField(TVShow, related_name='lists', blank=True)

    class Meta:
        get_latest_by = '-pk'
        ordering = ['name']
        verbose_name = 'TV Show List'
        verbose_name_plural = 'TV Show Lists'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:tvshow:list',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.name,
            description='TV Show List',
            keywords=['harshp.com', 'tvshow', 'tv', 'list', 'collection'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                TVShowList, self, 'name', name=self.name)
        return super(TVShowList, self).save(*args, **kwargs)


class TVShowQuote(models.Model):
    """A quote from a tv show."""

    tvshow = models.ForeignKey(TVShow, related_name='quotes')
    quote = models.TextField()
    favorite = models.BooleanField(default=False, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['movie__title']
        verbose_name = 'Movie Quote'
        verbose_name_plural = 'Movie Quotes'

    def __str__(self):
        return self.quote

    def get_absolute_url(self):
        return reverse(
            'hobbies:film:quote',
            args=[self.pk], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.quote,
            description='Movie Quote',
            keywords=['harshp.com', 'movies', 'film', 'quote'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(MovieQuote, self).save(*args, **kwargs)
