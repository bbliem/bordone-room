from django.forms.widgets import SelectMultiple

from .models import Photo

class SelectMultipleImages(SelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        photo = Photo.objects.get(id=value)
        option['attrs']['data-img-src'] = photo.thumbnail().url
        option['attrs']['data-albums'] = sorted([a.id for a in photo.album_set.all()])
        return option
