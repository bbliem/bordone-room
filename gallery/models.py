from django.db import models

class Photo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    num_views = models.IntegerField('number of views', default=0)
    original = models.ImageField(upload_to='%Y/%m/%d')
    # Metadata
    date_taken = models.DateTimeField(blank=True, null=True)
    make = models.CharField(max_length=200) # camera producer
    model = models.CharField(max_length=200) # camera model
    lens = models.CharField(max_length=200)
    aperture = models.FloatField(blank=True, null=True)
    focal_length = models.FloatField(blank=True, null=True)
    shutter_speed = models.FloatField(blank=True, null=True)
    iso = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def create_with_exif(cls, exif_reader, filename, **kwargs):
        """kwargs are passed to constructor after being updated with EXIF information."""
        kwargs.update(exif_reader.tags(filename))
        return cls(**kwargs)

class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, related_name='+') # TODO enforce that it's in this album? Avoid NULL values?
    num_views = models.IntegerField('number of views', default=0)
    photos = models.ManyToManyField(Photo)

    def __str__(self):
        return self.title
