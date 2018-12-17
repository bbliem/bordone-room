from django.apps import AppConfig


class GalleryConfig(AppConfig):
    name = 'gallery'

    def ready(self):
        from . import signals
