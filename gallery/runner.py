# Based on https://www.caktusgroup.com/blog/2013/06/26/media-root-and-django-tests/

import logging
import shutil
import tempfile

from django.conf import settings
from django.test.runner import DiscoverRunner

log = logging.getLogger(__name__)


class TempMediaMixin():
    """Mixin to create temporary MEDIA_ROOT directory."""

    def setup_test_environment(self):
        super().setup_test_environment()
        settings._original_media_root = settings.MEDIA_ROOT
        settings._original_file_storage = settings.DEFAULT_FILE_STORAGE
        self._temp_media = tempfile.mkdtemp()
        log.debug(f"Created temporary MEDIA_ROOT {self._temp_media}")
        settings.MEDIA_ROOT = self._temp_media
        settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    def teardown_test_environment(self):
        super().teardown_test_environment()
        log.debug(f"Destroying temporary MEDIA_ROOT...")
        shutil.rmtree(self._temp_media, ignore_errors=True)
        settings.MEDIA_ROOT = settings._original_media_root
        del settings._original_media_root
        settings.DEFAULT_FILE_STORAGE = settings._original_file_storage
        del settings._original_file_storage


class CustomDiscoverRunner(TempMediaMixin, DiscoverRunner):
    """Local test suite runner."""
