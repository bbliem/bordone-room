from datetime import datetime, timezone
from io import BytesIO
from unittest import mock

from django.conf import settings
from django.core.files.images import ImageFile
from django.test import TestCase
from PIL import Image

from .exif_reader import ExifReader
from .models import Photo

def create_image(filename, size=(10,10), color='black'):
    buf = BytesIO()
    image = Image.new('RGB', size=size, color=color)
    image.save(buf, 'JPEG')
    return ImageFile(buf, name=filename)


def verify_image_file(path):
    with Image.open(path) as image:
        image.verify()


class ExifReaderTests(TestCase):
    metadata = {
            'EXIF:DateTimeOriginal': '2018:12:15 03:47:23',
            'EXIF:Make': 'Make X',
            'EXIF:Model': 'Model Y',
            'Composite:LensID': 'Lens Z',
            'Composite:Aperture': 0.95,
            'EXIF:FocalLength': 42.5,
            'Composite:ShutterSpeed': 1.2,
            'EXIF:ISO': 3200,
            }

    def setUp(self):
        self.exif_reader = ExifReader(None)

    def test_parse_date_taken_none(self):
        value = self.exif_reader._field_readers['date_taken']({'EXIF:DateTimeOriginal': None})
        self.assertIs(value, None)

    def test_parse_date_taken_empty(self):
        value = self.exif_reader._field_readers['date_taken']({'EXIF:DateTimeOriginal': ''})
        self.assertIs(value, None)

    def test_parse_date_taken_seconds_missing(self):
        value = self.exif_reader._field_readers['date_taken']({'EXIF:DateTimeOriginal': '2018:12:15 03:47'})
        self.assertIs(value, None)

    def test_parse_date_taken_valid(self):
        value = self.exif_reader._field_readers['date_taken'](self.metadata)
        self.assertEqual(value, datetime(2018, 12, 15, 3, 47, 23, 00, timezone.utc))

    def test_make_valid(self):
        value = self.exif_reader._field_readers['make'](self.metadata)
        self.assertEqual(value, self.metadata['EXIF:Make'])

    def test_model_valid(self):
        value = self.exif_reader._field_readers['model'](self.metadata)
        self.assertEqual(value, self.metadata['EXIF:Model'])

    def test_lens_valid(self):
        value = self.exif_reader._field_readers['lens'](self.metadata)
        self.assertEqual(value, self.metadata['Composite:LensID'])

    def test_aperture_none(self):
        value = self.exif_reader._field_readers['aperture']({'Composite:Aperture': None})
        self.assertIs(value, None)

    def test_aperture_valid(self):
        value = self.exif_reader._field_readers['aperture'](self.metadata)
        self.assertEqual(value, self.metadata['Composite:Aperture'])

    def test_iso_none(self):
        value = self.exif_reader._field_readers['iso']({'EXIF:ISO': None})
        self.assertIs(value, None)

    def test_iso_float(self):
        value = self.exif_reader._field_readers['iso']({'EXIF:ISO': 100.1})
        self.assertIs(value, 100)

    def test_iso_valid(self):
        value = self.exif_reader._field_readers['iso'](self.metadata)
        self.assertEqual(value, self.metadata['EXIF:ISO'])


class PhotoModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.images = {}
        for color in ('black', 'green'):
            cls.images[color] = create_image(f'{color}.jpg', color=color)

        cls.black_photo = cls.create_photo('black')

    @classmethod
    def create_photo(cls, color='green'):
        return Photo.objects.create(
            name=f'{color} photo',
            original=cls.images[color],
        )

    @mock.patch.object(Photo, 'generate_thumbnails')
    def test_thumbnails_generated(self, mock_generate_thumbnails):
        self.create_photo()
        self.assertTrue(mock_generate_thumbnails.called)

    @mock.patch.object(Photo, 'generate_thumbnails')
    def test_thumbnails_updated_after_original_changed(self, mock_generate_thumbnails):
        self.assertEqual(mock_generate_thumbnails.call_count, 0)
        green_photo = self.create_photo('green')
        self.assertEqual(mock_generate_thumbnails.call_count, 1)
        green_photo.original = self.images['black']
        green_photo.save()
        self.assertEqual(mock_generate_thumbnails.call_count, 2)

    def test_original_file_created(self):
        verify_image_file(self.black_photo.original.path)

    def test_thumbnail_files_created(self):
        for thumbnail in self.black_photo.thumbnails():
            verify_image_file(thumbnail.path)
