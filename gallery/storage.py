import logging
import os
import pathlib

from django.core.files.storage import FileSystemStorage

log = logging.getLogger(__name__)

class PhotoStorage(FileSystemStorage):
    def url(self, name):
        log.debug(f"Getting URL of original {name}")
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        # url = filepath_to_uri(name)
        # if url is not None:
        #     url = url.lstrip('/')
        # return urljoin(self.base_url, url)
        slug, _ = os.path.splitext(os.path.basename(name))
        return f'{self.base_url}originals/{slug}'


class ThumbnailStorage(FileSystemStorage):
    def url(self, name):
        log.debug(f"Getting URL of thumbnail {name}")
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        *_, size, filename = pathlib.Path(name).parts
        slug, _ = os.path.splitext(filename)
        return f'{self.base_url}thumbnails/{slug}/{size}'
