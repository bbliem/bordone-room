from django.contrib import admin

from .models import Photo
from .models import Album

admin.site.register(Photo)
admin.site.register(Album)
