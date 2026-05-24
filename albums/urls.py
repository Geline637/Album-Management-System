from django.urls import path

from . import views

app_name = "albums"

urlpatterns = [
    path("", views.AlbumListView.as_view(), name="album-list"),
    path("albums/create-with-photo/", views.AlbumCreateWithPhotoView.as_view(), name="album-create-with-photo"),
    path("albums/<int:pk>/", views.AlbumDetailView.as_view(), name="album-detail"),
    path("albums/<int:pk>/edit/", views.AlbumUpdateView.as_view(), name="album-update"),
    path("albums/<int:pk>/delete/", views.AlbumDeleteView.as_view(), name="album-delete"),
    path("albums/<int:album_pk>/photos/add/", views.PhotoCreateView.as_view(), name="photo-create"),
    path("photos/<int:pk>/", views.PhotoDetailView.as_view(), name="photo-detail"),
    path("photos/<int:pk>/edit/", views.PhotoUpdateView.as_view(), name="photo-update"),
    path("photos/<int:pk>/delete/", views.PhotoDeleteView.as_view(), name="photo-delete"),
]
