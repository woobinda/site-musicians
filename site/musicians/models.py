from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


@python_2_unicode_compatible
class MusicStyle(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    def __str__(self):
        return '%s' % self.name


@python_2_unicode_compatible
class MusicianInstrument(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    def __str__(self):
        return '%s' % self.name


@python_2_unicode_compatible
class Musician(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, unique=True)
    playing_style = models.ForeignKey(
        MusicStyle, verbose_name="Playing style", default=None)
    instrument = models.ForeignKey(
        MusicianInstrument, verbose_name='Instrument', default=None)
    created_date = models.DateTimeField(auto_now_add=True, editable=True)
    avatar = models.ImageField(upload_to='musicians_avatars', blank=True)
    about = models.TextField(blank=True, max_length=700)
    slug = models.SlugField(max_length=100, verbose_name='slug', )
    owner = models.ForeignKey(User, related_name='musicians', null=True)

    def full_name(self):
        return str(self.first_name + ' ' + self.last_name)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        kwargs = {'id': self.id,
                  'slug': self.slug,
                  }
        return reverse('musicians:musician_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name())
        super(Musician, self).save(*args, **kwargs)


@python_2_unicode_compatible
class VideoUrl(models.Model):
    name = models.CharField(max_length=100, verbose_name='Video Name')
    url = models.TextField(max_length=100, verbose_name='URL form YouTube')
    host = models.ForeignKey(
        Musician, verbose_name='host', blank=True, null=True)

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.url = str(self.url.split('/')[-1])
        super(VideoUrl, self).save(*args, **kwargs)
