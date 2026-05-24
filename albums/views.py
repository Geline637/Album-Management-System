from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import AlbumForm, AlbumWithPhotoForm, PhotoForm
from .models import Album, Photo


class AlbumAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    permission_denied_message = "Administrator access is required to manage albums."

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name="album_admin").exists()


class AlbumOwnerOrAdminMixin(AlbumAdminRequiredMixin):
    def test_func(self):
        user = self.request.user
        album = self.get_object()
        return album.owner == user or user.is_staff or user.groups.filter(name="album_admin").exists()


class PhotoOwnerOrAdminMixin(AlbumAdminRequiredMixin):
    def test_func(self):
        user = self.request.user
        photo = self.get_object()
        return photo.album.owner == user or user.is_staff or user.groups.filter(name="album_admin").exists()


class AlbumListView(ListView):
    model = Album
    context_object_name = "albums"
    paginate_by = 12
    template_name = "albums/album_list.html"


class AlbumDetailView(DetailView):
    model = Album
    context_object_name = "album"
    template_name = "albums/album_detail.html"


class AlbumCreateWithPhotoView(AlbumAdminRequiredMixin, CreateView):
    model = Album
    form_class = AlbumWithPhotoForm
    template_name = "albums/album_with_photo_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        album = form.save()
        Photo.objects.create(
            album=album,
            title=form.cleaned_data["photo_title"],
            caption=form.cleaned_data["photo_caption"],
            image=form.cleaned_data["image"],
        )
        return redirect(album.get_absolute_url())


class AlbumUpdateView(AlbumOwnerOrAdminMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = "albums/album_form.html"


class AlbumDeleteView(AlbumOwnerOrAdminMixin, DeleteView):
    model = Album
    template_name = "albums/album_confirm_delete.html"
    success_url = reverse_lazy("albums:album-list")


class PhotoCreateView(AlbumAdminRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "albums/photo_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.album = get_object_or_404(Album, pk=kwargs["album_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.album = self.album
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album"] = self.album
        return context

    def get_success_url(self):
        return self.album.get_absolute_url()


class PhotoUpdateView(PhotoOwnerOrAdminMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "albums/photo_form.html"

    def get_success_url(self):
        return self.object.album.get_absolute_url()


class PhotoDetailView(DetailView):
    model = Photo
    context_object_name = "photo"
    template_name = "albums/photo_detail.html"


class PhotoDeleteView(PhotoOwnerOrAdminMixin, DeleteView):
    model = Photo
    template_name = "albums/photo_confirm_delete.html"

    def get_success_url(self):
        return self.object.album.get_absolute_url()
