from django import forms

class PhotoUploadForm(forms.Form):
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
