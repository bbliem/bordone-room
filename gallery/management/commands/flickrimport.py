import exiftool
import glob
import json
import logging
import os
import re
from shutil import copyfile

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from gallery.exif_reader import ExifReader
from gallery.models import Photo

log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import photos from Flickr data dump"

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs=1, help="Directory containing all extracted archives")

    def handle(self, *args, **options):
        directory = options['directory'][0]
        self.import_photos(directory)
        self.import_albums(directory)

    @transaction.atomic
    def import_photos(self, directory):
        with exiftool.ExifTool(print_conversion=True) as et:
            exif_reader = ExifReader(et)
            log.debug(f'Importing directory {directory}')

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
                                                       num_views=data['count_views'],
                                                       upload_date=data['date_imported'],
                                                       original=File(pf, name=new_basename))
                        log.debug(f"Created model instance {photo.original}")
                        photo.save()

    def import_albums(self, directory):
        with open(f'{directory}/albums.json', 'rt') as f:
            pass
