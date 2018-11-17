from django.db import models

class Photo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    num_views = models.IntegerField('number of views', default=0)
    original = models.ImageField()
    # Metadata
    date_taken = models.DateTimeField()
    make = models.CharField(max_length=200) # camera producer
    model = models.CharField(max_length=200) # camera model
    lens = models.CharField(max_length=200)
    aperture = models.DecimalField(max_digits=4, decimal_places=2)
    focal_length = models.DecimalField(max_digits=6, decimal_places=2)
    shut_numer = models.IntegerField('shutter speed numerator') # TODO enforce that either this or the denominator is 1?
    shut_denom = models.IntegerField('shutter speed denominator')
    iso = models.IntegerField()

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
