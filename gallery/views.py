from django.http import HttpResponse
#from django.shortcuts import render

from .models import Photo

def index(request):
    photos_list = Photo.objects.order_by('-date_taken')[:2]
    output = ', '.join([ph.name for ph in photos_list])
    return HttpResponse(output)

def view_photo(request, photo_id):
    return HttpResponse(f"Viewing photo {photo_id}")

def view_album(request, album_id):
    return HttpResponse(f"Viewing album {album_id}")
