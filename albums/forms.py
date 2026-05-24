from django import forms
from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class AlbumWithPhotoForm(forms.ModelForm):
    photo_title = forms.CharField(max_length=200, label="Photo title")
    photo_caption = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Photo caption",
    )
    image = forms.ImageField(label="Photo image")

    class Meta:
        model = Album
        fields = ["title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["title", "caption", "image"]
        widgets = {
            "caption": forms.Textarea(attrs={"rows": 3}),
        }
