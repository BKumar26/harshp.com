from django.db import models

from sitebase import ratings
from sitebase.models import Tag


class Hobby(models.Model):
    """Base Hobby model. Depicts a abstract hobby.
    Aggregates common fields for all hobbies."""

    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, db_index=True)

    # blank date_start means I do not remember when I started this hobby
    # or that I haven't read this book yet
    date_start = models.DateField(blank=True, db_index=True)
    # blank date_end can mean two things:
    # 1. I do not remember when I finished this hobby
    # 2. I have not finished this hobby yet
    date_end = models.DateField(blank=True, null=True, db_index=True)

    # completed indicates if I have finished or stopped this hobby
    completed = models.BooleanField(default=False, db_index=True)
    # wishlist is if I want to do this in the future
    wishlist = models.BooleanField(default=False, db_index=True)

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    url = models.URLField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        abstract = True
        ordering = ['-date_end']
        verbose_name = 'Hobby'
        verbose_name_plural = 'Hobbies'

    def __str__(self):
        return self.title


class Person(models.Model):
    """A person of interest.
    Connected to some hobby as creator or collaborator."""

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True, blank=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
