from django.conf import settings
import os
from pilkit.utils import suggest_extension

def source_name_as_path(generator):
    """
    Copied from ImageKit and changed so that thumbnail file names are not just
    hashes of the thumbnail but hashes of the original image plus a suffix.
    """
    source_filename = getattr(generator.source, 'name', None)

    if source_filename is None or os.path.isabs(source_filename):
        # Generally, we put the file right in the cache file directory.
        dir = settings.IMAGEKIT_CACHEFILE_DIR
        new_basename_root = generator.get_hash()
    else:
        # For source files with relative names (like Django media files),
        # use the source's name to create the new filename.
        dir = os.path.join(settings.IMAGEKIT_CACHEFILE_DIR,
                           #os.path.splitext(source_filename)[0])
                           os.path.dirname(source_filename))
        basename = os.path.basename(generator.source.name)
        basename_root = os.path.splitext(basename)[0]

        if not basename_root.endswith('_o'):
            raise Exception(f"Expected basename to end with '_o' for {source_filename}.")

        if not isinstance(generator.options.get('suffix'), str):
            raise Exception(f"You must supply a 'suffix' option to ImageKit fields.")

        new_basename_root = basename_root[:-2] + '_' + generator.options.get('suffix')

    ext = suggest_extension(source_filename or '', generator.format)
    return os.path.normpath(os.path.join(dir, '%s%s' % (new_basename_root, ext)))
