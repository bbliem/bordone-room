from datetime import datetime
import pytz

import logging
from pprint import pformat

log = logging.getLogger(__name__)

EXIF_DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

def _parse_datetime(s):
    try:
        dto = datetime.strptime(s, EXIF_DATE_FORMAT)
        # XXX use UTC as EXIF has no information on time zones
        return dto.replace(tzinfo=pytz.UTC)
    except (ValueError, TypeError):
        return None

def _parse_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None

def _parse_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None

class ExifReader:
    # Tags that will be extracted from files and may be used in _field_readers
    _relevant_tags = [
            'EXIF:DateTimeOriginal',
            'EXIF:Make',
            'EXIF:Model',
            'Composite:LensID',
            'Composite:Aperture',
            'EXIF:FocalLength',
            'Composite:ShutterSpeed',
            'EXIF:ISO',
            ]

    # Maps model field names to functions of an exiftool metadata object returning the value (or None if not available)
    _field_readers = {
            'date_taken': lambda m: _parse_datetime(m.get('EXIF:DateTimeOriginal')),
            'make': lambda m: m.get('EXIF:Make'),
            'model': lambda m: m.get('EXIF:Model'),
            'lens': lambda m: m.get('Composite:LensID'),
            'aperture': lambda m: _parse_float(m.get('Composite:Aperture')),
            'focal_length': lambda m: _parse_float(m.get('EXIF:FocalLength')),
            'shutter_speed': lambda m: _parse_float(m.get('Composite:ShutterSpeed')),
            'iso': lambda m: _parse_int(m.get('EXIF:ISO')),
            }

    def __init__(self, exiftool):
        """exiftool will be used for opening files and extracting metadata."""
        self.exiftool = exiftool

    def tags(self, filename):
        """Return relevant EXIF tags as a dict."""
        metadata = self.exiftool.get_tags(self._relevant_tags, filename)
        log.info(f"Read EXIF metadata from '{filename}':\n{pformat(metadata)}")
        result = {field: parser(metadata) for field, parser in self._field_readers.items()}
        log.info(f"Parsed EXIF metadata from '{filename}':\n{pformat(result)}")
        return result
