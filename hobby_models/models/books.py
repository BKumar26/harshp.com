from django.db import models
from subdomains.utils import reverse

from utils.meta_generator import create_meta
from utils.models import get_unique_slug

from sitebase import ratings
from sitebase.models import Tag
from .hobby import Person


class Author(models.Model):
    """An author of a book or a comic."""

    person = models.OneToOneField(Person)
    favorite = models.BooleanField(default=False, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['person']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.person.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:books:author',
            args=[self.person.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.person.name,
            description='Book Author',
            keywords=['book', 'author'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(Author, self).save(*args, **kwargs)


class NovelSeries(models.Model):
    """Depicts a series of books."""

    name = models.CharField(max_length=250, db_index=True)
    favorite = models.BooleanField(default=False, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['name']
        verbose_name = 'Novel Series'
        verbose_name_plural = 'Novel Series'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'hobbies:books:novel_series',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.name,
            description='Book Series',
            keywords=['book', 'novel', 'series'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                NovelSeries, self, 'name', name=self.name)
        return super(NovelSeries, self).save(*args, **kwargs)


class Novel(models.Model):
    """Reading novels as a hobby."""

    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, db_index=True)

    series = models.ForeignKey(NovelSeries, related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')

    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    url = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        get_latest_by = '-pk'
        ordering = ['title']
        verbose_name = 'Novel'
        verbose_name_plural = 'Novels'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'hobbies:books:novel',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description=self.title,
            keywords=['book', 'hobby', 'novel', 'reading'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Novel, self, 'title', title=self.title)
        return super(Novel, self).save(*args, **kwargs)


# class NovelNote(Post):
#     """Note about a novel"""

#     novel = models.ForeignKey(Novel, related_name='notes')
#     body_type = models.CharField(
#         max_length=8, choices=EDITOR_TYPES, default='markdown')
#     body_text = models.TextField(blank=True)
#     body = models.TextField()

#     class Meta:
#         get_latest_by = '-date_published'
#         ordering = ['-date_published', 'title']
#         verbose_name = 'Novel note'
#         verbose_name_plural = 'Novel notes'

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse(
#             'hobbies:books:novel_note',
#             args=[self.novel.slug, self.slug], subdomain='hobbies')

#     def get_seo_meta(self):
#         return create_meta(
#             title=self.title,
#             description=self.title,
#             keywords=[tag for tag in self.tags_set.all()],
#             url=self.get_absolute_url())

#     def save(self, *args, **kwargs):
#         if self.pk is None:
#             self.slug = get_unique_slug(NovelNote, self, 'title', self.title)
#         self.date_updated = timezone.now()
#         if self.body_type == 'markdown':
#             self.body_text = markdown.markdown(
#                 self.body, extensions=ext_formatting, output_format='html5')
#         else:
#             self.body_text = self.body
#         return super(NovelNote, self).save(*args, **kwargs)


# class NovelSeriesNote(Post):
#     """Note about a book series"""

#     series = models.ForeignKey(NovelSeries, related_name='notes')
#     body_type = models.CharField(
#         max_length=8, choices=EDITOR_TYPES, default='markdown')
#     body_text = models.TextField(blank=True)
#     body = models.TextField()

#     class Meta:
#         get_latest_by = '-date_published'
#         ordering = ['-date_published', 'title']
#         verbose_name = 'Novel Series note'
#         verbose_name_plural = 'Novel Series notes'

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse(
#             'hobbies:books:novel_series_note',
#             args=[self.book.slug, self.slug], subdomain='hobbies')

#     def get_seo_meta(self):
#         return create_meta(
#             title=self.title,
#             description=self.title,
#             keywords=[tag for tag in self.tags_set.all()],
#             url=self.get_absolute_url())

#     def save(self, *args, **kwargs):
#         if self.pk is None:
#             self.slug = get_unique_slug(
#                 NovelSeriesNote, self, 'title', self.title)
#         self.date_updated = timezone.now()
#         if self.body_type == 'markdown':
#             self.body_text = markdown.markdown(
#                 self.body, extensions=ext_formatting, output_format='html5')
#         else:
#             self.body_text = self.body
#         return super(NovelSeriesNote, self).save(*args, **kwargs)


class NovelList(models.Model):
    """A collection of books or comics by me."""

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True, db_index=True)
    novels = models.ManyToManyField(Novel, related_name='lists')

    class Meta:
        ordering = ['name']
        verbose_name = 'Novel List'
        verbose_name_plural = 'Novel Lists'

    def get_absolute_url(self):
        return reverse(
            'hobbies:books:novel_list',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.name,
            description='Reading List',
            keywords=['book', 'reading list'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                NovelList, self, 'name', self.name)
        return super(NovelList, self).save(*args, **kwargs)


class NovelQuote(models.Model):
    """A quote from a book."""

    novel = models.ForeignKey(Novel, related_name='quotes')
    quote = models.TextField()
    favorite = models.BooleanField(default=False, db_index=True)

    class Meta:
        get_latest_by = 'pk'
        ordering = ['novel__title']
        verbose_name = 'Novel Quote'
        verbose_name_plural = 'Novel Quotes'

    def get_absolute_url(self):
        return reverse(
            'hobbies:books:novel_quote',
            args=[self.pk], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.novel.title,
            description='A quote from a book',
            keywords=['book', 'novel', 'quote'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            pass
        return super(NovelQuote, self).save(*args, **kwargs)


class Manga(models.Model):
    """Manga books"""

    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, db_index=True)
    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    ongoing = models.BooleanField(default=True, db_index=True)
    url = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        get_latest_by = '-pk'
        ordering = ['title']
        verbose_name = 'Manga'
        verbose_name_plural = 'Manga'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'hobbies:books:manga',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description=self.title,
            keywords=['book', 'hobby', 'manga', 'reading'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Manga, self, 'title', title=self.title)
        return super(Manga, self).save(*args, **kwargs)


class MangaList(models.Model):
    """A collection of manga"""

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True, db_index=True)
    novels = models.ManyToManyField(Novel, related_name='lists')

    class Meta:
        ordering = ['name']
        verbose_name = 'Manga List'
        verbose_name_plural = 'Manga Lists'

    def get_absolute_url(self):
        return reverse(
            'hobbies:books:manga_list',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.name,
            description='Manga List',
            keywords=['book', 'manga', 'list'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                MangaList, self, 'name', self.name)
        return super(MangaList, self).save(*args, **kwargs)


class Comics(models.Model):
    """Comics books"""

    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(
        max_length=256, unique=True, blank=True, db_index=True)
    favorite = models.BooleanField(default=False, db_index=True)
    rating = models.PositiveSmallIntegerField(
        choices=ratings.scale_5to1,
        default=ratings.scale_5to1_lowest.score, db_index=True)
    url = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        get_latest_by = '-pk'
        ordering = ['title']
        verbose_name = 'Comics'
        verbose_name_plural = 'Comics'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'hobbies:books:manga',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.title,
            description=self.title,
            keywords=['book', 'hobby', 'manga', 'reading'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Comics, self, 'title', title=self.title)
        return super(Comics, self).save(*args, **kwargs)


class ComicsList(models.Model):
    """A collection of manga"""

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=256, unique=True, db_index=True)
    novels = models.ManyToManyField(Novel, related_name='lists')

    class Meta:
        ordering = ['name']
        verbose_name = 'Comics List'
        verbose_name_plural = 'Comics Lists'

    def get_absolute_url(self):
        return reverse(
            'hobbies:books:manga_list',
            args=[self.slug], subdomain='hobbies')

    def get_seo_meta(self):
        return create_meta(
            title=self.name,
            description='Comics List',
            keywords=['book', 'manga', 'list'],
            url=self.get_absolute_url())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                ComicsList, self, 'name', self.name)
        return super(ComicsList, self).save(*args, **kwargs)
