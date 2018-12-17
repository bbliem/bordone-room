import exiftool
import sys

from django.conf import settings
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views import generic

from .exif_reader import ExifReader
from .forms import PhotoUploadForm
from .models import Photo

class IndexView(generic.ListView):
    template_name = 'gallery/index.html'
    #model = Photo

    def get_queryset(self):
        """Return the last couple of photos."""
        #return Photo.objects.order_by('-date_taken')[:2]
        return Photo.objects.order_by('-date_taken')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thumbnail_sizes'] = settings.GALLERY_THUMBNAIL_SIZES
        return context


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
