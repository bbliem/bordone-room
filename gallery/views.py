import exiftool
import json
import logging
import os
import sys

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic

from .exif_reader import ExifReader
from .forms import AlbumCreateForm, PhotoUploadForm
from .models import Album, Photo

log = logging.getLogger(__name__)


class AjaxFormMixin:
    def form_invalid(self, form):
        if self.request.is_ajax():
            response = {
                'status': 'error',
                'errors': form.errors.as_json(),
            }
            return JsonResponse(response, status=400)
        else:
            return super().form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            response = {
                'status': 'ok',
            }
            return JsonResponse(response)
        else:
            return super().form_valid(form)


class CommonContextMixin(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thumbnail_sizes'] = settings.GALLERY_THUMBNAIL_SIZES
        context['jg_row_height'] = settings.JG_ROW_HEIGHT
        context['jg_margins'] = settings.JG_MARGINS
        return context


class PhotoListView(CommonContextMixin, generic.ListView):
    model = Photo
    ordering = ['-upload_date']
    paginate_by = 50
    template_name = 'gallery/photo_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(public=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['upload_form'] = PhotoUploadForm()
        context['album_list'] = Album.objects.order_by('-creation_date')
        context['page_title'] = "Photos"
        return context

    def post(self, request, *args, **kwargs):
        return PhotoUploadView.as_view()(request, args, kwargs)


class PhotoDetailView(generic.DetailView):
    model = Photo
    template_name = 'gallery/photo_detail.html'

    # FIXME this causes a 404 error if the user has no permission, but we should probably report permission denied
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(public=True)
        return queryset

    @method_decorator(permission_required('gallery.change_photo', raise_exception=True))
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
        if data.get('albums') is not None:
            try:
                albums = [Album.objects.get(id=album_id)
                          for album_id in data.get('albums')]
            except Album.DoesNotExist:
                return HttpResponseBadRequest(reason="Invalid albums specified")
            log.debug(f"Setting albums {albums}")
            photo.album_set.set(albums)

        # Get visibility
        visibility = data.get('visibility')
        if visibility:
            log.debug(f"Setting visibility to {visibility}")
            if visibility == 'public':
                photo.public = True
            elif visibility == "private":
                photo.public = False
            else:
                return HttpResponseBadRequest(reason="Invalid visibility specified")

        photo.save()
        return HttpResponse() # success

    @method_decorator(permission_required('gallery.delete_photo', raise_exception=True))
    def delete(self, request, *args, **kwargs):
        request_str = request.body.decode('utf-8')
        data = json.loads(request_str)
        log.debug(f"PhotoDetailView got DELETE request: {data}")

        # Get photo
        photo_id = data.get('photo')
        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            return HttpResponseBadRequest(reason="Invalid photo specified")
        log.debug(f"Deleting photo {photo}")

        # Delete photo
        photo.delete()
        return HttpResponse() # success


class PhotoUploadView(PermissionRequiredMixin, AjaxFormMixin, generic.edit.BaseFormView):
    permission_required = 'gallery.add_photo'
    form_class = PhotoUploadForm
    success_url = reverse_lazy('gallery:index')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            log.debug(f"Uploaded files {files}")

            with exiftool.ExifTool(settings.EXIFTOOL, print_conversion=True) as et:
                exif_reader = ExifReader(et)
                for f in files:
                    # XXX this assumes that all files are instances of TemporaryUploadedFile.
                    # We therefore need to force all uploads to be written to disk.
                    filename = f.temporary_file_path()
                    photo_name, _ = os.path.splitext(f.name)
                    instance = Photo.create_with_exif(exif_reader,
                                                      filename,
                                                      name=photo_name,
                                                      original=f)
                    log.debug(f"Created {instance.__dict__}")
                    instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AlbumListView(CommonContextMixin, generic.ListView):
    model = Album
    ordering = ['-creation_date']
    paginate_by = 50
    template_name = 'gallery/album_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            # Only display albums with a public cover photo
            # FIXME do something more reasonable
            queryset = queryset.select_related('cover_photo').filter(cover_photo__public=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AlbumCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        return AlbumCreateView.as_view()(request, args, kwargs)


class AlbumCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'gallery.add_album'
    form_class = AlbumCreateForm
    model = Album
    success_url = reverse_lazy('gallery:album_list')


class AlbumDetailView(CommonContextMixin, generic.DetailView):
    model = Album
    template_name = 'gallery/photo_list.html'

    # FIXME this causes a 404 error if the user has no permission, but we should probably report permission denied
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            # Only display albums with a public cover photo
            # FIXME do something more reasonable
            queryset = queryset.select_related('cover_photo').filter(cover_photo__public=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos = self.object.photos
        if not self.request.user.is_authenticated:
            photos = photos.filter(public=True)
        else:
            photos = photos.all()
        context['photo_list'] = photos
        context['album_list'] = Album.objects.order_by('-creation_date')
        album = self.object
        context['page_title'] = album.title
        context['page_description'] = album.description
        return context


class ThumbnailServerView(generic.detail.BaseDetailView):
    model = Photo

    # FIXME this causes a 404 error if the user has no permission, but we should probably report permission denied
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(public=True)
        return queryset

    def get(self, request, *args, **kwargs):
        photo = self.get_object()
        size = kwargs['size']
        with open(getattr(photo, f'thumbnail_{size}').path, 'rb') as f:
            # FIXME photo may not always be JPEG. Perhaps use
            # https://github.com/ahupp/python-magic or look at file name
            # extension (and checking on upload if it's good).
            return HttpResponse(f, content_type='image/jpeg')


class OriginalServerView(generic.detail.BaseDetailView):
    model = Photo

    # FIXME this causes a 404 error if the user has no permission, but we should probably report permission denied
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(public=True)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        photo = self.object
        with open(photo.original.path, 'rb') as f:
            # FIXME photo may not always be JPEG. Perhaps use
            # https://github.com/ahupp/python-magic or look at file name
            # extension (and checking on upload if it's good).
            response = HttpResponse(f, content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{photo.name}.jpg"'
            return response
