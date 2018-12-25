from django.forms.widgets import SelectMultiple

from .models import Photo

class SelectMultipleImages(SelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        option['attrs']['data-img-src'] = Photo.objects.get(id=value).thumbnail().url
        return option
