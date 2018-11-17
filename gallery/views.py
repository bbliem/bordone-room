from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Photo

def index(request):
    photos_list = Photo.objects.order_by('-date_taken')[:2]
    context = {'photos_list': photos_list}
    return render(request, 'gallery/index.html', context)

def view_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    return render(request, 'gallery/view_photo.html', {'photo': photo})

def view_album(request, album_id):
    raise Http404("TODO")
