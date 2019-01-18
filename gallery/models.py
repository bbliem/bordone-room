from datetime import date
import logging
import os
import secrets

from django.conf import settings
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

log = logging.getLogger(__name__)

def original_path(photo, filename):
    today = date.today()
    # Add secret to filename in order to avoid guessing the names of photos
    # without viewing permission
    secret = secrets.token_hex(8)
    base, extension = os.path.splitext(filename)
    base = base[:80] # crop to 80 characters

    # valid_chars = f'-_.() {string.ascii_letters}{string.digits}'
    # base = ''.join(c for c in base if c in valid_chars)
    # base = base.replace(' ','_')

    return f'{today.year}/{today.month}/{today.day}/{base}_{secret}{extension}'

class ThumbnailField(ImageSpecField):
    def __init__(self, source, size):
        super().__init__(source=source,
                         format='JPEG',
                         options={'quality': 90,
                                  'suffix': str(size)},
                         processors=[ResizeToFit(size, size)],
                         )

class Photo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    num_views = models.IntegerField('number of views', default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    original = models.ImageField(upload_to=original_path)

    # Thumbnails
    for size in settings.GALLERY_THUMBNAIL_SIZES:
        vars()[f'thumbnail_{size}'] = ThumbnailField('original', size)

    # Metadata
    date_taken = models.DateTimeField(blank=True, null=True)
    make = models.CharField(max_length=200, blank=True, default='') # camera producer
    model = models.CharField(max_length=200, blank=True, default='') # camera model
    lens = models.CharField(max_length=200, blank=True, default='')
    aperture = models.FloatField(blank=True, null=True)
    focal_length = models.FloatField(blank=True, null=True)
    shutter_speed = models.FloatField(blank=True, null=True)
    iso = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'[untitled photo {self.id}]'

    @classmethod
    def create_with_exif(cls, exif_reader, filename, **kwargs):
        """kwargs are passed to constructor after being updated with EXIF information."""
        kwargs.update(exif_reader.tags(filename))
        return cls(**kwargs)

    def thumbnail(self, size=settings.GALLERY_THUMBNAIL_SIZES[0]):
        assert size in settings.GALLERY_THUMBNAIL_SIZES
        return getattr(self, f'thumbnail_{size}')

    def generate_thumbnails(self):
        log.debug(f"Generating thumbnails for photo {self.original}")
        for size in settings.GALLERY_THUMBNAIL_SIZES:
            self.thumbnail(size).generate()

    def delete_files(self):
        log.debug(f"Deleting files for photo {self.original}")
        self.original.storage.delete(self.original.path)
        for size in settings.GALLERY_THUMBNAIL_SIZES:
            t = self.thumbnail(size)
            t.storage.delete(t.path)

class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, related_name='+') # TODO enforce that it's in this album? Avoid NULL values?
    num_views = models.IntegerField('number of views', default=0)
    photos = models.ManyToManyField(Photo)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
