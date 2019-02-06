from django.contrib import admin

from .models import Photo
from .models import Album

class PhotoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description', 'upload_date', 'public', 'original']}),
        ('Metadata', {'fields': ['date_taken',
                                 'make',
                                 'model',
                                 'lens',
                                 'aperture',
                                 'focal_length',
                                 'shutter_speed',
                                 'iso',
                                 ],
                      'classes': ['collapse']}),
        ]
    list_display = ('name', 'original', 'date_taken', 'upload_date')
    list_filter = ['date_taken', 'upload_date']
    search_fields = ['name', 'original']

admin.site.register(Photo, PhotoAdmin)

admin.site.register(Album)
