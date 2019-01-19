import exiftool
import json
import logging
import sys

from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic

from .exif_reader import ExifReader
from .forms import AlbumCreateForm, PhotoUploadForm, PhotoBatchEditForm
from .models import Album, Photo

log = logging.getLogger(__name__)

class CommonContextMixin(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thumbnail_sizes'] = settings.GALLERY_THUMBNAIL_SIZES
        return context

class PhotoListView(CommonContextMixin, generic.ListView):
    model = Photo
    ordering = ['-upload_date']
    paginate_by = 50
    template_name = 'gallery/photo_list.html'

    # def get_queryset(self):
    #     """Return the last couple of photos."""
    #     #return Photo.objects.order_by('-date_taken')[:2]
    #     return Photo.objects.order_by('-date_taken')[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload_form'] = PhotoUploadForm()
        context['albums'] = Album.objects.order_by('-creation_date')
        return context

    def post(self, request, *args, **kwargs):
        return PhotoUploadView.as_view()(request, args, kwargs)


class PhotoDetailView(generic.DetailView):
    model = Photo
    template_name = 'gallery/photo_detail.html'

    def patch(self, request, *args, **kwargs):
        request_str = request.body.decode('utf-8')
        data = json.loads(request_str)
        log.debug(f"PhotoDetailView got PATCH request: {data}")

        # Get photo
        photo_id = data.get('photo')
        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            return HttpResponseBadRequest(reason="Invalid photo specified")
        log.debug(f"Updating photo {photo}")

        # Get albums
        try:
            albums = [Album.objects.get(id=album_id)
                      for album_id in data.get('albums')]
        except Album.DoesNotExist:
            return HttpResponseBadRequest(reason="Invalid albums specified")
        log.debug(f"Setting albums {albums}")

        # Update photo
        photo.album_set.set(albums)
        photo.save()
        return HttpResponse() # success


class PhotoUploadView(generic.FormView):
    form_class = PhotoUploadForm
    success_url = reverse_lazy('gallery:index')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            log.debug(f"Uploaded files {files}")

            with exiftool.ExifTool() as et:
                exif_reader = ExifReader(et)
                for f in files:
                    # XXX this assumes that all files are instances of TemporaryUploadedFile.
                    # We therefore need to force all uploads to be written to disk.
                    filename = f.temporary_file_path()
                    instance = Photo.create_with_exif(exif_reader, filename, original=f)
                    log.debug(f"Created {instance.__dict__}")
                    instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AlbumListView(CommonContextMixin, generic.ListView):
    template_name = 'gallery/album_list.html'
    model = Album

    def get_queryset(self):
        return Album.objects.order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AlbumCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        return AlbumCreateView.as_view()(request, args, kwargs)


class AlbumCreateView(generic.CreateView):
    form_class = AlbumCreateForm
    model = Album
    success_url = reverse_lazy('gallery:album_list')


class AlbumDetailView(CommonContextMixin, generic.DetailView):
    model = Album
    template_name = 'gallery/album_detail.html'


class PhotoBatchEditView(CommonContextMixin, generic.FormView):
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
