from django.db import models

from subdomains.utils import reverse

from utils.meta_generator import create_meta
from utils.models import get_unique_slug
from sitebase import ratings
from sitebase.models import Tag

from hobbies.models import Hobby


class Game(Hobby):
    """A Video Game"""

    WINDOWS = 'MSWIN'
    MACOS = 'MACOS'
    LINUX = 'LINUX'
    IOS = 'iOS'
    ANDROID = 'ANDRD'
    CONSOLE = 'CONSL'
    EMULATOR = 'EMLTR'
    PS3 = 'PS3'
    PS4 = 'PS4'
    XBOX = 'XBOX'
    XBOX_ONE = 'XBOX1'
    PLATFORMS = (
        (WINDOWS, 'WINDOWS'),
        (MACOS, 'MACOS'),
        (LINUX, 'LINUX'),
        (IOS, 'IOS'),
        (ANDROID, 'ANDROID'),
        (CONSOLE, 'CONSOLE'),
        (EMULATOR, 'EMULATOR'),
        (PS3, 'PS3'),
        (PS4, 'PS4'),
        (XBOX, 'XBOX'),
        (XBOX_ONE, 'XBOX_ONE'),
    )

    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, db_index=True)

    platform = models.CharField(
        max_length=5, choices=PLATFORMS,
        default=WINDOWS, db_index=True)

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    url = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        get_latest_by = 'title'
        ordering = ['title']
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'hobbies:game',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description=self.title,
            keywords=['games', 'hobby', 'video games'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Game, self, 'title', title=self.title)
        return super(Game, self).save(*args, **kwargs)


class GamingList(models.Model):
    """A list of games by me."""

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)
    games = models.ManyToManyField(Game, related_name='lists')
