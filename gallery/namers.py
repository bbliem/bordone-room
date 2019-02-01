import os
from pathlib import Path

from django.conf import settings
from pilkit.utils import suggest_extension

def source_name_as_path(generator):
    """
    Copied from ImageKit and changed so that thumbnail file names are not just
    hashes of the thumbnail.
    """
    source_filename = getattr(generator.source, 'name', None)

    if source_filename is None or os.path.isabs(source_filename):
        # Generally, we put the file right in the cache file directory.
        dir = settings.IMAGEKIT_CACHEFILE_DIR
        new_basename_root = generator.get_hash()
    else:
        # For source files with relative names (like Django media files),
        # use the source's name to create the new filename.
        if not generator.options.get('thumbnail_size'):
            raise Exception("You must supply a 'thumbnail_size' option to ImageKit fields.")

        source_path = Path(source_filename)
        if source_path.parts[0] != 'originals':
            raise Exception(f"Source filename '{source_filename}' does not start with 'originals/'.")

        dir = os.path.join(settings.IMAGEKIT_CACHEFILE_DIR,
                           *source_path.parts[1:-1],
                           str(generator.options.get('thumbnail_size')))
        basename = os.path.basename(generator.source.name)
        new_basename_root = os.path.splitext(basename)[0]

    ext = suggest_extension(source_filename or '', generator.format)
    return os.path.normpath(os.path.join(dir, '%s%s' % (new_basename_root, ext)))
