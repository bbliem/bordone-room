from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Photo

import logging

log = logging.getLogger(__name__)

@receiver(post_save, sender=Photo, dispatch_uid='on_save')
def on_save(sender, **kwargs):
    log.debug(f"Model saved (sender: {sender}): {kwargs}")
    photo = kwargs['instance']

    # We regenerate thumbnails if the instance has been created or the file
    # modification date of the thumbnails is older than the original.
    if kwargs['created']: # FIXME? or kwargs['update_fields'] contains the file?
        photo.generate_thumbnails()
    else:
        thumbnail = photo.thumbnail()
        thumbnail_mtime = thumbnail.storage.get_modified_time(thumbnail.name)
        original_mtime = photo.original.storage.get_modified_time(photo.original.name)
        if thumbnail_mtime < original_mtime:
            photo.generate_thumbnails()

@receiver(post_delete, sender=Photo, dispatch_uid='on_delete')
def on_delete(sender, **kwargs):
    # XXX Perhaps we don't want this in production
    log.debug(f"Model deleted (sender: {sender}): {kwargs}")
    photo = kwargs['instance']
    photo.delete_files()
