from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Photo

import logging

log = logging.getLogger(__name__)

@receiver(post_save, sender=Photo, dispatch_uid='on_save')
def on_save(sender, **kwargs):
    log.debug(f"Model saved (sender: {sender}): {kwargs}")
    photo = kwargs['instance']
    photo.generate_thumbnails()

@receiver(post_delete, sender=Photo, dispatch_uid='on_delete')
def on_delete(sender, **kwargs):
    # XXX Perhaps we don't want this in production
    log.debug(f"Model deleted (sender: {sender}): {kwargs}")
    photo = kwargs['instance']
    photo.delete_files()
