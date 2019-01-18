import exiftool
import glob
import json
import logging
import os
import re

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, connection # XXX remove connection

from gallery.exif_reader import ExifReader
from gallery.models import Album, Photo

log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import photos from Flickr data dump"

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs=1, help="Directory containing all extracted archives")

    @transaction.atomic
    def handle(self, *args, **options):
        directory = options['directory'][0]
        pk_of_flickr_id = self.import_photos(directory)
        log.debug(f"PKs: {pk_of_flickr_id}")
        self.import_albums(directory, pk_of_flickr_id)

    def import_photos(self, directory):
        pk_of_flickr_id = {}
        with exiftool.ExifTool(print_conversion=True) as et:
            exif_reader = ExifReader(et)
            log.debug(f"Importing photos from directory {directory}")

            for filename in glob.glob(f'{directory}/photo_*.json'):
                log.debug(f'Importing file {filename}')
                with open(filename, 'rt') as jf:
                    data = json.load(jf)
                    fid = data['id']

                    # Import original
                    photo_filenames = glob.glob(f'{directory}/*_{fid}_o.jpg')
                    if len(photo_filenames) != 1:
                        raise CommandError(f"Image file for photo with Flickr ID {fid} not found")
                    old_filename = photo_filenames[0]
                    new_basename = os.path.basename(old_filename)
                    new_basename = re.sub(r'(.*)_(\d+)_o\.(.+)', r'\1.\3', new_basename)

                    # Create model instance
                    with open(old_filename, 'rb') as pf:
                        photo = Photo.create_with_exif(exif_reader,
                                                       old_filename,
                                                       name=data['name'],
                                                       description=data['description'],
                                                       upload_date=data['date_imported'],
                                                       original=File(pf, name=new_basename))
                        photo.save()
                        log.debug(f"Created photo model instance {photo}")
                        pk_of_flickr_id[fid] = photo.id
            return pk_of_flickr_id

    def import_albums(self, directory, pk_of_flickr_id):
        log.debug(f"Importing albums from directory {directory}")
        with open(f'{directory}/albums.json', 'rt') as f:
            for data in json.load(f)['albums']:
                photo_ids = [pk_of_flickr_id[k] for k in data['photos']]
                photos = Photo.objects.filter(id__in=photo_ids) # XXX can we use IDs instead of QuerySets later to avoid the SELECT?

                cover_photo_flickr_id = data['cover_photo']
                assert cover_photo_flickr_id.startswith('https://www.flickr.com/photos//')
                cover_photo_flickr_id = cover_photo_flickr_id[31:]
                cover_photo_id = pk_of_flickr_id.get(cover_photo_flickr_id)

                album = Album(title=data['title'],
                              description=data['description'],
                              creation_date=data['created'],
                              modification_date=data['last_updated'],
                              cover_photo_id=cover_photo_id)
                album.save()
                album.photos.set(photos)
                log.debug(f"Created album model instance {album}")
