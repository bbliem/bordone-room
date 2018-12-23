from django import forms

from .models import Album

class PhotoUploadForm(forms.Form):
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']
