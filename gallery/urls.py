from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'gallery'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='gallery:photo_list',
                                  permanent=False),
         name='index'),
    path('photos/', views.PhotoListView.as_view(), name='photo_list'),
    path('photos/<int:pk>/', views.PhotoDetailView.as_view(),
         name='photo_detail'),
    path('albums/<int:pk>/', views.view_album, name='album_detail'),
]
