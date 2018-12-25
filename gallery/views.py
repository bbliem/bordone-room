import exiftool
import logging
import sys

from django.conf import settings
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views import generic

from .exif_reader import ExifReader
from .forms import AlbumCreateForm, PhotoUploadForm, PhotoBatchEditForm
from .models import Album, Photo

log = logging.getLogger(__name__)

class PhotoListView(generic.ListView):
    template_name = 'gallery/photo_list.html'
    #model = Photo

    def get_queryset(self):
        """Return the last couple of photos."""
        #return Photo.objects.order_by('-date_taken')[:2]
        return Photo.objects.order_by('-date_taken')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PhotoUploadForm()
        # TODO the following occurs many times -- refactor
        context['thumbnail_sizes'] = settings.GALLERY_THUMBNAIL_SIZES
        return context

    def post(self, request, *args, **kwargs):
        return PhotoUploadView.as_view()(request, args, kwargs)


class PhotoDetailView(generic.DetailView):
    model = Photo
    template_name = 'gallery/photo_detail.html'


class PhotoUploadView(generic.FormView):
    form_class = PhotoUploadForm
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


class AlbumListView(generic.ListView):
    template_name = 'gallery/album_list.html'
    model = Album

    def get_queryset(self):
        return Album.objects.order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AlbumCreateForm()
        context['thumbnail_sizes'] = settings.GALLERY_THUMBNAIL_SIZES
        return context

    def post(self, request, *args, **kwargs):
        return AlbumCreateView.as_view()(request, args, kwargs)


class AlbumCreateView(generic.CreateView):
    form_class = AlbumCreateForm
    model = Album
    success_url = reverse_lazy('gallery:album_list')


class AlbumDetailView(generic.DetailView):
    model = Album
    template_name = 'gallery/album_detail.html'


class PhotoBatchEditView(generic.FormView):
    template_name = 'gallery/photo_batch_edit.html'
    form_class = PhotoBatchEditForm
    success_url = reverse_lazy('gallery:index')

    def form_valid(self, form):
        albums = form.cleaned_data['albums_field']
        for photo in form.cleaned_data['photos_field']:
            log.debug(f"Changing album set of photo {photo.id} from "
                      f"{photo.album_set} to {albums}")
            photo.album_set.set(albums)
            photo.save()
        return super().form_valid(form)
