import sys

from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views import generic

from .forms import PhotoUploadForm
from .models import Photo

class IndexView(generic.ListView):
    template_name = 'gallery/index.html'
    #model = Photo

    def get_queryset(self):
        """Return the last couple of photos."""
        #return Photo.objects.order_by('-date_taken')[:2]
        return Photo.objects.order_by('-date_taken')

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
        files = request.FILES.getlist('file_field')
        print(f"Files {files}", file=sys.stderr)
        if form.is_valid():
            for f in files:
                # TODO Do something with each file.
                instance = Photo(original=f)
                print(f"Created {instance.__dict__}", file=sys.stderr)
                instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
