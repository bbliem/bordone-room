from datetime import datetime, timezone
from decimal import Decimal

from django.test import TestCase

from .models import Photo, _parse_datetime, _parse_decimal, _parse_float, _parse_int

class PhotoModelTests(TestCase):
    def test_parse_datetime_none(self):
        self.assertIs(_parse_datetime(None), None)

    def test_parse_datetime_empty(self):
        self.assertIs(_parse_datetime(''), None)

    def test_parse_datetime_seconds_missing(self):
        self.assertIs(_parse_datetime('2018:12:15 03:47'), None)

    def test_parse_datetime_valid(self):
        date = datetime(2018, 12, 15, 3, 47, 23, 00, timezone.utc)
        self.assertEqual(_parse_datetime('2018:12:15 03:47:23'), date)

    def test_parse_decimal_none(self):
        self.assertIs(_parse_decimal(None), None)

    def test_parse_decimal_empty(self):
        self.assertIs(_parse_decimal(''), None)

    def test_parse_decimal_hex(self):
        self.assertIs(_parse_decimal('0xdeadbeef'), None)

    def test_parse_decimal_valid(self):
        self.assertEqual(_parse_decimal('12.345'), Decimal('12.345'))

    def test_parse_float_none(self):
        self.assertIs(_parse_float(None), None)

    def test_parse_float_empty(self):
        self.assertIs(_parse_float(''), None)

    def test_parse_float_hex(self):
        self.assertIs(_parse_float('0xdeadbeef'), None)

    def test_parse_float_valid(self):
        self.assertEqual(_parse_float('0.5'), 0.5)

    def test_parse_int_none(self):
        self.assertIs(_parse_int(None), None)

    def test_parse_int_empty(self):
        self.assertIs(_parse_int(''), None)

    def test_parse_int_float(self):
        self.assertIs(_parse_int('0.5'), None)

    def test_parse_int_valid(self):
        self.assertEqual(_parse_int('05'), 5)
