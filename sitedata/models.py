"""sitedata models

    Tag
"""

from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone
from redactor.fields import RedactorField
from subdomains.utils import reverse


class Tag(models.Model):

    """    Tag - meta for models
    """
    tagid = models.AutoField(primary_key=True)
    tagname = models.CharField(max_length=150, unique=True)
    count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        """string representation for tags

        Args:
            self(Tag)

        Returns:
            str: tag name

        Raises:
            None
        """
        return self.tagname

    class Meta:

        """attributes for tag
        """
        ordering = ('tagname',)

    def save(self, *args, **kwargs):
        """save tags to database

        check for duplicates, and update modified timestamps

        Args:
            self(Tag)
            *args: arguments
            **kwargs: parameters

        Returns:
            return from Tag.super()

        Raises:
            None
        """
        self.slug = slugify(self.tagname)
        self.count = 0
        for x in Tag.__dict__:
            if x.endswith('_set'):
                self.count += getattr(self, x).count()

        return super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='sitedata:tagname',
            subdomain='www',
            kwargs={'tagname': self.slug, })

"""
# Future work
# User class
# Author relationship
# Comments class
# associate comments with each post
# page -> would be a template? auto-add related entries
# |-> create a specific tag and list that in the templates
"""


class Feedback(models.Model):

    """Feedback about the site

    if feedback is anonymous, name and email are blank
    name will not be shown on site
    will only be available to me
    name: your name if you wish to give it, leaving it blank makes the
    feedback anonymous
    email: if you want to receive a copy of my reply to your email
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=250,
        help_text='A title is needed for the feedback you wish to give.')
    text = RedactorField(
        help_text='Enter the text of the feedback here.')
    published = models.DateTimeField()
    user_name = models.CharField(
        max_length=250, blank=True, verbose_name='Name', default='Anonymous',
        help_text='Leave name blank for an Anonymous feedback. '
        'If you enter your name, only I will be able to see it.')
    user_email = models.EmailField(
        max_length=150, blank=True, null=True, verbose_name='Email',
        help_text='Email (optional) will be used to send you the reply to '
        'this feedback. Replies will also be published on site without '
        'any personal details such as name/email.')
    linked_post = models.URLField(
        max_length=250, blank=True, null=True, verbose_name='Post URL',
        help_text='(optional) URL of the post/page you wish to give your '
        'feedback on. Leave it blank for a general feedback.')
    reply = RichTextField(blank=True, null=True)
    reply_date = models.DateTimeField(blank=True, null=True)

    class Meta:

        """Meta attributes for Feedback
        """
        verbose_name = 'Anonymous Feedback'
        verbose_name = 'Anonymous Feedbacks'
        ordering = ('-published', )

    def save(self, *args, **kwargs):
        """save feedback to database
        """
        self.published = timezone.now()
        print self.reply_date, self.reply
        if self.reply_date is None:
            if self.reply != '' and self.reply is not None:
                self.reply_date = timezone.now()
        if not self.user_name:
            self.user_name = 'Anonymous'
        return super(Feedback, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return url for this object"""
        return reverse(
            viewname='sitedata:feedback',
            subdomain='www',
            kwargs={'feedback_no': self.id, })
