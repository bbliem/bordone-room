from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('photo/<int:photo_id>/', views.view_photo, name='view_photo'),
    path('album/<int:album_id>/', views.view_album, name='view_album'),
]
