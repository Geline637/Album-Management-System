from django.conf import settings
from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField


class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="albums",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("albums:album-detail", kwargs={"pk": self.pk})


class Photo(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    image = CloudinaryField("image")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("albums:album-detail", kwargs={"pk": self.album.pk})
