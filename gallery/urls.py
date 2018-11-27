from django.urls import path

from . import views

app_name = 'gallery'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('photo/<int:pk>/', views.PhotoView.as_view(), name='view_photo'),
    path('album/<int:pk>/', views.view_album, name='view_album'),
]
