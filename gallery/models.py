from django.db import models

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

class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, related_name='+') # TODO enforce that it's in this album? Avoid NULL values?
    num_views = models.IntegerField('number of views', default=0)
    photos = models.ManyToManyField(Photo)

    def __str__(self):
        return self.title
