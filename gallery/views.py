import exiftool
import sys

from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views import generic

from .forms import PhotoUploadForm
from .models import Photo

from .exif_reader import ExifReader

class IndexView(generic.ListView):
    template_name = 'gallery/index.html'
    #model = Photo

    def get_queryset(self):
        """Return the last couple of photos."""
        #return Photo.objects.order_by('-date_taken')[:2]
        queryset = Photo.objects.order_by('-date_taken')

        # Generate thumbnails
        # TODO Make this more maintainable
        for photo in queryset:
            photo.thumbnail_320.generate()
            photo.thumbnail_500.generate()
            photo.thumbnail_640.generate()
            photo.thumbnail_800.generate()
            photo.thumbnail_1024.generate()

        return queryset

class PhotoView(generic.DetailView):
    model = Photo
    template_name = 'gallery/view_photo.html'

def view_album(request, album_id):
    raise Http404("TODO")

class PhotoUploadView(generic.FormView):
    form_class = PhotoUploadForm
    template_name = 'gallery/index.html'
    success_url = reverse_lazy('gallery:index')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            print(f"Files {files}", file=sys.stderr)

            with exiftool.ExifTool() as et:
                exif_reader = ExifReader(et)
                for f in files:
                    # XXX this assumes that all files are instances of TemporaryUploadedFile.
                    # We therefore need to force all uploads to be written to disk.
                    filename = f.temporary_file_path()
                    instance = Photo.create_with_exif(exif_reader, filename, original=f)
                    print(f"Created {instance.__dict__}", file=sys.stderr)
                    instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
