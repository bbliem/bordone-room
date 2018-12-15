from datetime import datetime
from decimal import Decimal, InvalidOperation
import pytz

from django.db import models

EXIF_DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

def _parse_datetime(s):
    try:
        dto = datetime.strptime(s, EXIF_DATE_FORMAT)
        # XXX use UTC as EXIF has no information on time zones
        return dto.replace(tzinfo=pytz.UTC)
    except (ValueError, TypeError):
        return None

def _parse_decimal(s):
    try:
        return Decimal(s)
    except (TypeError, InvalidOperation):
        return None

def _parse_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None

def _parse_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None

class Photo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    num_views = models.IntegerField('number of views', default=0)
    original = models.ImageField()
    # Metadata
    date_taken = models.DateTimeField(blank=True, null=True)
    make = models.CharField(max_length=200) # camera producer
    model = models.CharField(max_length=200) # camera model
    lens = models.CharField(max_length=200)
    aperture = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    focal_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    shutter_speed = models.FloatField(blank=True, null=True)
    iso = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def create_with_exif(cls, exiftool, filename, **kwargs):
        """exiftool is an instance of exiftool that will be used for opening the given file and extracting the metadata. kwargs are passed to constructor after being updated with EXIF information."""

        # Extract EXIF tags from file
        tags = ["EXIF:DateTimeOriginal",
                "EXIF:Make",
                "EXIF:Model",
                "Composite:LensID",
                "Composite:Aperture",
                "EXIF:FocalLength",
                "Composite:ShutterSpeed",
                "EXIF:ISO",
                ]
        metadata = exiftool.get_tags(tags, filename)

        new_kwargs = {
                'date_taken': _parse_datetime(metadata.get('EXIF:DateTimeOriginal', '')),
                'make': metadata.get('EXIF:Make'),
                'model': metadata.get('EXIF:Model'),
                'lens': metadata.get('Composite:LensID'),
                'aperture': _parse_decimal(metadata.get('Composite:Aperture')),
                'focal_length': _parse_decimal(metadata.get('EXIF:FocalLength')),
                'shutter_speed': _parse_float(metadata.get('Composite:ShutterSpeed')),
                'iso': _parse_int(metadata.get('EXIF:ISO')),
                }
        for k, v in new_kwargs.items():
            if v:
                kwargs[k] = v

        return cls(**kwargs)

class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, related_name='+') # TODO enforce that it's in this album? Avoid NULL values?
    num_views = models.IntegerField('number of views', default=0)
    photos = models.ManyToManyField(Photo)

    def __str__(self):
        return self.title
