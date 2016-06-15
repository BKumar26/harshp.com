from django.models import models
from subdomains.utils import reverse
import markdown

from sitebase.editors import EDITOR_TYPES
from sitebase.markdown_extensions import ext_formatting
from utils.models import get_unique_slug

from sitebase import ratings


class Artist(models.Model):
    """Artist"""

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=256, unique=True)

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()

    class Meta:
        ordering = 'name'
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:music:artist', args=[self.slug], subdomain='hobbies')

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Artist, self, 'name', name=self.name)
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_formatting, output_format='html5')
        else:
            self.body_text = self.body
        return super(Artist, self).save(*args, **kwargs)


class Album(models.Model):
    """Album"""

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=256, unique=True)

    artists = models.ManyToManyField(Artist, related_name='albums')

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:music:album', args=[self.slug], subdomain='hobbies')

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Artist, self, 'name', name=self.name)
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_formatting, output_format='html5')
        else:
            self.body_text = self.body
        return super(Album, self).save(*args, **kwargs)


class Song(models.Model):
    """Song"""

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=256, unique=True)

    artists = models.ManyToManyField(Artist, related_name='songs')
    album = models.ForeignKey(
        Album, related_name='songs', blank=True, null=True)

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:music:song', args=[self.slug], subdomain='hobbies')

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Artist, self, 'name', name=self.name)
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_formatting, output_format='html5')
        else:
            self.body_text = self.body
        return super(Artist, self).save(*args, **kwargs)
