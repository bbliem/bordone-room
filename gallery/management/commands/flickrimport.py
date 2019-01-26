import exiftool
import glob
import json
import logging
import os
import pytz
import re
from datetime import datetime

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.timezone import make_aware

from gallery.exif_reader import ExifReader
from gallery.models import Album, Photo

log = logging.getLogger(__name__)

FLICKR_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

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
        with exiftool.ExifTool(settings.EXIFTOOL, print_conversion=True) as et:
            exif_reader = ExifReader(et)
            log.debug(f"Importing photos from directory {directory}")

            for filename in glob.glob(f'{directory}/photo_*.json'):
                log.debug(f'Importing file {filename}')
                with open(filename, 'rt') as jf:
                    data = json.load(jf)
                    fid = data['id']
                    public = data['privacy'] == 'public'

                    photo_filenames = glob.glob(f'{directory}/*_{fid}_o.jpg')
                    if len(photo_filenames) != 1:
                        raise CommandError(f"Image file for photo with Flickr ID {fid} not found")
                    old_filename = photo_filenames[0]
                    new_basename = os.path.basename(old_filename)
                    # Remove Flickr secret
                    new_basename = re.sub(r'(.*)_(\d+)_o\.(.+)', r'\1.\3', new_basename)

                    date_imported = datetime.strptime(data['date_imported'], FLICKR_DATE_FORMAT)
                    date_imported = make_aware(date_imported)

                    # Check if the image file already exists (to avoid
                    # unnecessary copying or thumbnail generation)
                    existing_original = None
                    date_dir = f'{date_imported.year}/{date_imported.month}/{date_imported.day}'
                    root, ext = os.path.splitext(new_basename)
                    match = re.compile(f'{root}_[A-Za-z0-9]+{ext}').match
                    date_path = f'{settings.MEDIA_ROOT}/{date_dir}'
                    if os.path.isdir(date_path):
                        for existing_file in os.listdir(date_path):
                            if match(existing_file):
                                existing_original = f'{date_dir}/{existing_file}'
                                log.debug(f"Image {existing_original} already exists")

                    # Create model instance
                    with open(old_filename, 'rb') as pf:
                        photo = Photo.create_with_exif(exif_reader,
                                                       old_filename,
                                                       name=data['name'],
                                                       description=data['description'],
                                                       upload_date=date_imported,
                                                       public=public,
                                                       #original=File(pf, name=new_basename))
                                                       )
                        if existing_original:
                            photo.original.name = existing_original
                        else:
                            photo.original = File(pf, name=new_basename)

                        photo.save()
                        log.debug(f"Upload date: {photo.upload_date}")
                        log.debug(f"Created photo model instance {vars(photo)}")
                        pk_of_flickr_id[fid] = photo.id
                        pass
            return pk_of_flickr_id

    def import_albums(self, directory, pk_of_flickr_id):
        log.debug(f"Importing albums from directory {directory}")
        with open(f'{directory}/albums.json', 'rt') as f:
            for data in json.load(f)['albums']:
                photo_ids = [pk_of_flickr_id[k] for k in data['photos'] if k != '0']
                photos = Photo.objects.filter(id__in=photo_ids) # XXX can we use IDs instead of QuerySets later to avoid the SELECT?

                cover_photo_flickr_id = data['cover_photo']
                assert cover_photo_flickr_id.startswith('https://www.flickr.com/photos//')
                cover_photo_flickr_id = cover_photo_flickr_id[31:]
                cover_photo_id = pk_of_flickr_id.get(cover_photo_flickr_id)

                created = datetime.fromtimestamp(int(data['created']))
                created = make_aware(created)

                last_updated = datetime.fromtimestamp(int(data['last_updated']))
                last_updated = make_aware(last_updated)

                album = Album(title=data['title'],
                              description=data['description'],
                              creation_date=created,
                              modification_date=last_updated,
                              cover_photo_id=cover_photo_id)
                album.save()
                album.photos.set(photos)
                log.debug(f"Created album model instance {album}")
