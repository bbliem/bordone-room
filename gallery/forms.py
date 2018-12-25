from django import forms

from .models import Album, Photo
from .widgets import SelectMultipleImages

class PhotoUploadForm(forms.Form):
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']


class PhotoBatchEditForm(forms.Form):
    photos_field = forms.ModelMultipleChoiceField(
        queryset=Photo.objects.all(),
        widget=SelectMultipleImages,
    )
    albums_field = forms.ModelMultipleChoiceField(queryset=Album.objects.all(),
                                                  required=False)
