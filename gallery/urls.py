from django.contrib.auth import views as auth_views
from django.contrib.flatpages.views import flatpage
from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'gallery'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='gallery:photo_list',
                                  permanent=False),
         name='index'),
    path('photos/', views.PhotoListView.as_view(), name='photo_list'),
    path('photos/<slug:slug>/', views.PhotoDetailView.as_view(), name='photo_detail'),
    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('albums/<slug:slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='gallery/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('media/thumbnails/<slug:slug>/<int:size>', views.ThumbnailServerView.as_view(), name='serve_thumbnail'),
    path('media/originals/<slug:slug>', views.OriginalServerView.as_view(), name='serve_original'),
]

# Flat pages
urlpatterns += [
    path('about/', flatpage, {'url': '/about/'}, name='about'),
    path('contact/', flatpage, {'url': '/contact/'}, name='contact'),
]
