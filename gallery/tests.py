from datetime import datetime, timezone

from django.test import TestCase

from .exif_reader import ExifReader

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
