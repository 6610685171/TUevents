from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Lost, Found, Student
from unittest.mock import patch


class LostAndFoundTests(TestCase):
    def setUp(self):

        self.owner_user = User.objects.create_user(
            username="6610611111", password="password"
        )
        self.student = Student.objects.create(user=self.owner_user, student_id="123456")
        self.other_user = User.objects.create_user(
            username="6610612222", password="password"
        )

        self.client = Client()
        self.client.login(username="6610611111", password="password")

        self.mock_image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

        self.lost_item = Lost.objects.create(
            items_name="Lost Wallet",
            description="Brown leather wallet lost in the cafeteria.",
            lost_at="Cafeteria",
            contact="9876543210",
            founded_status=False,
            student=self.student,
        )
        self.found_item = Found.objects.create(
            items_name="Found Phone",
            description="Black smartphone found near the library.",
            found_at="Library",
            contact="0123456789",
            founded_status=False,
            student=self.student,
        )

    def test_create_found_item_get(self):

        response = self.client.get(reverse("create_found_item"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "found/create_found_item.html")

    def test_create_found_item_not_login(self):
        self.client.logout()
        data = {
            "items_name": "Found Phone",
            "description": "Black smartphone found near the library.",
            "found_at": "Library",
            "contact": "0123456789",
            "founded_status": False,
            "image": self.mock_image,
        }
        url = reverse("create_found_item")
        response = self.client.post(url, data)
        self.assertNotEqual(response.status_code, 200)

    def test_create_found_item_post_valid(self):

        data = {
            "items_name": "Found Phone",
            "description": "Black smartphone found near the library.",
            "found_at": "Library",
            "contact": "0123456789",
            "founded_status": False,
            "image": self.mock_image,
        }
        response = self.client.post(reverse("create_found_item"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Found.objects.count(), 1)
        found_item = Found.objects.last()
        self.assertEqual(found_item.items_name, "Found Phone")
        self.assertEqual(
            found_item.description, "Black smartphone found near the library."
        )

    def test_create_found_item_post_invalid_data(self):

        data = {
            "items_name": "",
            "description": "Black smartphone found near the library.",
            "found_at": "Library",
            "contact": "0123456789",
            "founded_status": False,
            "image": self.mock_image,
        }
        response = self.client.post(reverse("create_found_item"), data)
        self.assertEqual(response.status_code, 200)

    def test_found_items_list_with_data(self):

        response = self.client.get(reverse("found_items_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "found/found_items_list.html")
        self.assertContains(response, "Found Phone")

    def test_found_item_redirects_to_detail(self):

        response = self.client.get(
            reverse("found_detail", kwargs={"found_id": self.found_item.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "found/found_item_detail.html")
        self.assertContains(response, self.found_item.items_name)
        self.assertContains(response, self.found_item.description)
        self.assertContains(response, self.found_item.found_at)

    def test_found_edit_view(self):

        response = self.client.get(
            reverse("found_edit", kwargs={"found_id": self.found_item.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "found/edit_found_item.html")
        self.assertContains(response, self.found_item.items_name)

    def test_create_lost_item_get(self):

        response = self.client.get(reverse("create_lost_item"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lost/create_lost_item.html")

    def test_create_lost_item_not_login(self):
        self.client.logout()
        data = {
            "items_name": "Lost Wallet",
            "description": "Brown leather wallet lost in the cafeteria.",
            "lost_at": "Library",
            "contact": "987654321",
            "founded_status": False,
            "image": self.mock_image,
        }
        url = reverse("create_lost_item")
        response = self.client.post(url, data)
        self.assertNotEqual(response.status_code, 200)

    def test_create_lost_item_post_valid(self):

        data = {
            "items_name": "Lost Wallet",
            "description": "Brown leather wallet lost in the cafeteria.",
            "lost_at": "Library",
            "contact": "987654321",
            "founded_status": False,
            "image": self.mock_image,
        }
        response = self.client.post(reverse("create_lost_item"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lost.objects.count(), 1)
        lost_item = Lost.objects.last()
        self.assertEqual(lost_item.items_name, "Lost Wallet")
        self.assertEqual(
            lost_item.description, "Brown leather wallet lost in the cafeteria."
        )

    def test_create_lost_item_post_invalid_data(self):

        data = {
            "items_name": "",
            "description": "Brown leather wallet lost in the cafeteria.",
            "found_at": "Library",
            "contact": "987654321",
            "founded_status": False,
            "image": self.mock_image,
        }
        response = self.client.post(reverse("create_found_item"), data)
        self.assertEqual(response.status_code, 200)

    def test_lost_items_list_with_data(self):

        response = self.client.get(reverse("lost_items_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lost/lost_items_list.html")
        self.assertContains(response, "Lost Wallet")

    def test_lost_item_redirects_to_detail(self):

        response = self.client.get(
            reverse("lost_detail", kwargs={"lost_id": self.lost_item.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lost/lost_item_detail.html")
        self.assertContains(response, self.lost_item.items_name)
        self.assertContains(response, self.lost_item.description)
        self.assertContains(response, self.lost_item.lost_at)

    def test_owner_can_delete_lost_item(self):

        response = self.client.post(
            reverse("lost_delete", kwargs={"lost_id": self.lost_item.id})
        )
        self.assertRedirects(response, reverse("lost_items_list"))
        self.assertEqual(Lost.objects.count(), 0)

    def test_lost_edit_view_owner(self):

        self.client.login(username="6610611111", password="password")

        data = {
            "items_name": "Updated Lost Wallet",
            "description": "Updated description.",
            "lost_at": "Library",
            "contact": "9876543210",
            "founded_status": False,
        }

        response = self.client.post(
            reverse("lost_edit", kwargs={"lost_id": self.lost_item.id}), data
        )

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response, reverse("lost_detail", kwargs={"lost_id": self.lost_item.id})
        )

        updated_lost_item = Lost.objects.get(id=self.lost_item.id)
        self.assertEqual(updated_lost_item.items_name, "Updated Lost Wallet")
        self.assertEqual(updated_lost_item.description, "Updated description.")
