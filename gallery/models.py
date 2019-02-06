import logging
import os
from datetime import date

from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, Transpose

from .storage import PhotoStorage

log = logging.getLogger(__name__)
photo_storage = PhotoStorage()

def original_path(photo, filename):
    today = date.today()
    _, extension = os.path.splitext(filename)
    return f'originals/{photo.upload_date.year}/{photo.upload_date.month}/{photo.upload_date.day}/{photo.slug}{extension}'


class ThumbnailField(ImageSpecField):
    def __init__(self, source, size):
        super().__init__(source=source,
                         format='JPEG',
                         options={'quality': 90,
                                  'thumbnail_size': size},
                         processors=[Transpose(Transpose.AUTO), ResizeToFit(size, size)],
                         )


class Photo(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True, null=True)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    public = models.BooleanField(default=False)
    original = models.ImageField(upload_to=original_path, storage=photo_storage)

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
        return f'Photo {self.slug}'

    @classmethod
    def create_with_exif(cls, exif_reader, filename, **kwargs):
        """kwargs are passed to constructor after being updated with EXIF information."""
        kwargs.update(exif_reader.tags(filename))
        return cls(**kwargs)

    def thumbnail(self, size=settings.GALLERY_THUMBNAIL_SIZES[0]):
        assert size in settings.GALLERY_THUMBNAIL_SIZES
        return getattr(self, f'thumbnail_{size}')

    def thumbnails(self):
        for size in settings.GALLERY_THUMBNAIL_SIZES:
            yield getattr(self, f'thumbnail_{size}')

    def photo_detail_thumbnail(self):
        return getattr(self, f'thumbnail_{settings.PHOTO_DETAIL_THUMBNAIL_SIZE}')

    def biggest_thumbnail(self):
        return getattr(self, f'thumbnail_{settings.GALLERY_THUMBNAIL_SIZES[-1]}')

    def generate_thumbnails(self):
        log.debug(f"Generating thumbnails for photo {self.original}")
        for size in settings.GALLERY_THUMBNAIL_SIZES:
            self.thumbnail(size).generate(force=True)

    def delete_files(self):
        log.debug(f"Deleting files for photo {self.original}")
        self.original.storage.delete(self.original.path)
        for size in settings.GALLERY_THUMBNAIL_SIZES:
            t = self.thumbnail(size)
            t.storage.delete(t.path)

    def shutter_speed_str(self):
        if self.shutter_speed >= 1:
            return str(shutter_speed)
        else:
            inverse = round(1/self.shutter_speed)
            return f"1/{inverse}"


class Album(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    description = models.TextField()
    cover_photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, related_name='+') # TODO enforce that it's in this album? Avoid NULL values?
    photos = models.ManyToManyField(Photo)
    creation_date = models.DateTimeField(default=timezone.now)
    modification_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
