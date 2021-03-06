from django.db import models
from django.utils import timezone
import markdown
from django.core.urlresolvers import reverse
from sitebase.editors import EDITOR_TYPES
from sitebase.markdown_extensions import ext_formatting
from utils.models import get_unique_slug
from sitebase.models import Post


class BlogSeries(models.Model):
    """A series of blog posts on harshp_com"""

    title = models.CharField(max_length=128, db_index=True)
    short_description = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=150, unique=True, db_index=True, blank=True)

    class Meta(object):

        ordering = ['title']
        verbose_name = 'Blog Series'
        verbose_name_plural = 'Blog Series'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                BlogSeries, self, 'title', title=self.title)
        return super(BlogSeries, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:series', args=[self.slug])


class BlogPost(Post):
    """A blog post on harshp_com"""

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()
    headerimage = models.URLField(max_length=256, blank=True, null=True)
    highlight = models.BooleanField(default=False, db_index=True)
    series = models.ForeignKey(
        BlogSeries,
        blank=True, null=True, default=None, db_index=True)

    class Meta(object):

        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                BlogPost, self, 'title', title=self.title)
        self.date_updated = timezone.now()
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(
                self.body, extensions=ext_formatting, output_format='html5')
        else:
            self.body_text = self.body
        return super(BlogPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.series:
            return reverse(
                'blog:post',
                args=[self.series.slug, self.slug])
        return reverse('blog:post', args=[self.slug])

    def get_seo_meta(self):
        """get meta properties for this object"""
        meta = super(BlogPost, self).get_seo_meta()
        if self.headerimage:
            meta['image'] = self.headerimage
        return meta
