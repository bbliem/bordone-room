from django.http import Http404
from django.views import generic

from .models import Photo

class IndexView(generic.ListView):
    template_name = 'gallery/index.html'
    #model = Photo

    def get_queryset(self):
        """Return the last couple of photos."""
        return Photo.objects.order_by('-date_taken')[:2]

class PhotoView(generic.DetailView):
    model = Photo
    template_name = 'gallery/view_photo.html'

def view_album(request, album_id):
    raise Http404("TODO")
