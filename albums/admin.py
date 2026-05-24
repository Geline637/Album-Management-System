from django.contrib import admin

from .models import Album, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "created_at")
    search_fields = ("title", "description")
    list_filter = ("created_at",)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "album", "uploaded_at")
    search_fields = ("title", "caption")
    list_filter = ("uploaded_at",)
