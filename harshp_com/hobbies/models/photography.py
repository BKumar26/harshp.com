from django.db import models

from sitebase.editors import EDITOR_TYPES

from hobbies.models import Hobby
from sitebase.models import Author, Post, Tag


class Camera(models.Model):
    """Camera"""

    NIKON = 'NK'
    CANON = 'CN'

    NIKON_F = 'F'
    CANON_EFS = 'EFS'

    FULL_FRAME = 'F'
    APS_C = 'C'

    MANUFACTURERS = (
        (NIKON, 'Nikon'),
        (CANON, 'Canon'))

    MOUNTS = (
        (NIKON_F, 'NIKON F'),
        (CANON_EFS, 'CANON EF-S'))

    SENSOR_TYPES = (
        (FULL_FRAME, 'Full Frame'),
        (APS_C, 'APS-C'))

    model = models.CharField(max_length=256, db_index=True)
    company = models.CharField(
        max_length=2, choices=MANUFACTURERS, db_index=True)
    mount = models.CharField(max_length=3, choices=MOUNTS, db_index=True)
    sensor_type = models.CharField(
        max_length=1, choices=SENSOR_TYPES, db_index=True)
    sensor_size = models.FloatField()
    bought_new = models.BooleanField()
    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()


class CameraLens(models.Model):
    """Camera Lens"""

    PORTRAIT = 'P'
    WIDE_ANGLE = 'W'
    ZOOM = 'Z'
    MACRO = 'M'

    NIKON = 'NK'
    CANON = 'CN'
    CARL_ZEISS_JENA = 'CJ'
    TAMROM = 'TM'
    PENTAX = 'PT'

    TYPE = (
        (PORTRAIT, 'Portrait'),
        (WIDE_ANGLE, 'Wide Angle'),
        (ZOOM, 'Zoom'),
        (MACRO, 'Macro'))

    MANUFACTURERS = (
        (NIKON, 'Nikon'),
        (CANON, 'Canon'),
        (CARL_ZEISS_JENA, 'Carl Zeiss Jena'),
        (TAMROM, 'Tamrom'),
        (PENTAX, 'Pentax'))

    prime = models.BooleanField(db_index=True)
    lens_type = models.CharField(max_length='1', choices=TYPE, db_index=True)
    focal_length_start = models.PositiveSmallIntegerField(db_index=True)
    focal_length_end = models.PositiveSmallIntegerField(db_index=True)
    company = models.CharField(
        max_length=2, choices=MANUFACTURERS, db_index=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()


class PhotoshootCategory(models.Model):
    """A Photoshoot or Photo Expedition."""

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)


class PhotoshootIdea(Post):
    """An idea about a kind of photoshoot I want to do."""

    category = models.ForeignKey(PhotoshootCategory, related_name='ideas')

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()


class Photoshoot(Hobby):
    """A Photoshoot that I undertook."""

    category = models.ForeignKey(
        PhotoshootCategory,
        related_name='photoshoots', blank=True, null=True)
    url = models.URLField(max_length=256, blank=True, null=True)
    idea = models.ForeignKey(PhotoshootIdea, related_name='photoshoots')
    # TODO: add geoposition
    # https://github.com/philippbosch/django-geoposition/
    author = models.ManyToManyField(Author)
    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()
    tags = models.ManyToManyField(Tag)
