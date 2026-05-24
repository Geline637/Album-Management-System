from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from .models import Album


class AlbumViewTests(TestCase):
    def setUp(self):
        self.admin_group = Group.objects.create(name="album_admin")
        self.user = User.objects.create_user(username="member", password="password123")
        self.admin = User.objects.create_user(username="admin", password="password123")
        self.admin.groups.add(self.admin_group)
        self.album = Album.objects.create(
            title="Test Album",
            description="A test album",
            owner=self.admin,
        )
        self.client = Client()

    def _create_image_file(self):
        return SimpleUploadedFile(
            "test.jpg",
            b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00",
            content_type="image/jpeg",
        )

    def test_album_list_open(self):
        response = self.client.get(reverse("albums:album-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.album.title)

    def test_album_create_requires_login(self):
        response = self.client.get(reverse("albums:album-create-with-photo"))
        self.assertEqual(response.status_code, 302)

    def test_admin_can_create_album_with_photo(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("albums:album-create-with-photo"),
            {
                "title": "New Album",
                "description": "Cloudinary test",
                "photo_title": "Sample Photo",
                "photo_caption": "Test caption",
                "image": self._create_image_file(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Album.objects.filter(title="New Album").exists())
