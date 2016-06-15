from django.db import models
from subdomains.utils import reverse

from utils.meta_generator import create_meta
from utils.models import get_unique_slug

from sitebase import ratings
from hobbies.models import Hobby


class Cuisine(models.Model):
    """A food cuisine."""

    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)
    favorite = models.BooleanField(default=False, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['title']
        verbose_name = 'Cuisine'
        verbose_name_plural = 'Cuisines'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'hobbies:food:cuisine',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description='Food Cuisine',
            keywords=['food', 'cuisine'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Cuisine, self, 'title', title=self.title)
        return super(Cuisine, self).save(*args, **kwargs)


class FoodDish(models.Model):
    """A food dish."""

    cuisine = models.ForeignKey(Cuisine, related_name='dishes')
    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)
    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['title']
        verbose_name = 'Food Dish'
        verbose_name_plural = 'Food Dishes'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'hobbies:food:dish',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description='Food Dish',
            keywords=['food', 'dish'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                FoodDish, self, 'title', title=self.title)
        return super(FoodDish, self).save(*args, **kwargs)


class FoodPlace(models.Model):
    """A food place."""

    title = models.CharField(max_length=250, db_index=True)
    address = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)
    # TODO: geolocation
    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['title']
        verbose_name = 'Food Place'
        verbose_name_plural = 'Food Places'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'hobbies:food:place',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description='Food Place',
            keywords=['food', 'place', 'restaurant'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                FoodPlace, self, 'title', title=self.title)
        return super(FoodPlace, self).save(*args, **kwargs)


class FoodExperience(Hobby):
    """My experience of eating food at some place."""

    # title - what I ate
    # date_start = date_end
    # completed - irrelevant
    # wishlist - whether this is in the future?
    # favorite - whether I liked it
    # rating
    # tags

    dishes = models.ManyToManyField(FoodDish, related_name='places')
    location = models.ForeignKey(
        FoodPlace, related_name='experiences', blank=True, null=True)
    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['title']
        verbose_name = 'Food Experience'
        verbose_name_plural = 'Food Experience'

    def __str__(self):
        if self.location:
            return 'eating at ' + self.location.title + ' on ' + self.date
        return 'eating on ' + self.date

    def get_absolute_url(self):
        return reverse(
            'hobbies:food:experience',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description='Eating food',
            keywords=['food', 'eating'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(FoodExperience, self).save(*args, **kwargs)


# class FoodBlog(Post):
#     """My blog about food."""

#     experience = models.ForeignKey(FoodExperience, related_name='posts')
#     body_type = models.CharField(
#         max_length=8, choices=EDITOR_TYPES, default='markdown')
#     body_text = models.TextField(blank=True)
#     body = models.TextField()


class Cheese(models.Model):
    """My love of cheese."""

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=256, unique=True)

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['name']
        verbose_name = 'Cheese'
        verbose_name_plural = 'Cheese'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:food:cheese',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.name,
            description='Cheese',
            keywords=['food', 'cheese'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Cheese, self, 'name', name=self.name)
        return super(Cheese, self).save(*args, **kwargs)


class Pasta(models.Model):
    """My love of pasta."""

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=256, unique=True)

    shape = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Long'),
            (2, 'Ribbon'),
            (3, 'Short'),
            (4, 'Decorative'),
            (5, 'Minute'),
            (6, 'Stuffed'),
            (7, 'Irregular')),
        db_index=True)

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['title']
        verbose_name = 'Pasta'
        verbose_name_plural = 'Pasta'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:food:pasta',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.name,
            description='Pasta',
            keywords=['food', 'pasta'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Pasta, self, 'name', name=self.name)
        return super(Pasta, self).save(*args, **kwargs)


class Tea(models.Model):
    """My love of tea."""

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=256, unique=True)

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['name']
        verbose_name = 'Tea'
        verbose_name_plural = 'Tea'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:food:tea',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.name,
            description='Tea',
            keywords=['food', 'tea'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Tea, self, 'name', title=self.name)
        return super(Tea, self).save(*args, **kwargs)
