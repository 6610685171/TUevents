from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Lost, Found, Student


class LostAndFoundTests(TestCase):
    def setUp(self):
        # Create test users with numeric usernames and a student instance
        self.owner_user = User.objects.create_user(
            username="6610611111", password="password"
        )
        self.student = Student.objects.create(user=self.owner_user, student_id="123456")
        self.other_user = User.objects.create_user(
            username="6610612222", password="password"
        )
        self.client = Client()
        self.client.login(username="6610611111", password="password")

        # Mock image
        self.mock_image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

        # Create Lost and Found items
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

    ### Found Item Tests ###
    def test_create_found_item_get(self):
        """Test GET request to create_found_item view."""
        response = self.client.get(reverse("create_found_item"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "found/create_found_item.html")

    def test_create_found_item_post_valid(self):
        """Test POST request with valid data to create a found item."""
        data = {
            "items_name": "Found Watch",
            "description": "Silver wristwatch found near the library.",
            "found_at": "Library",
            "contact": "0123456789",
            "founded_status": False,
            "image": self.mock_image,
        }
        response = self.client.post(reverse("create_found_item"), data)
        self.assertRedirects(response, reverse("found_items_list"))
        self.assertEqual(Found.objects.count(), 2)
        found_item = Found.objects.last()
        self.assertEqual(found_item.items_name, "Found Watch")
        self.assertEqual(
            found_item.description, "Silver wristwatch found near the library."
        )

    def test_found_items_list_with_data(self):
        """Test found_items_list view with data."""
        response = self.client.get(reverse("found_items_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "found/found_items_list.html")
        self.assertContains(response, "Found Phone")

    def test_found_item_redirects_to_detail(self):
        """Test that clicking a Found item redirects to the detail page."""
        response = self.client.get(
            reverse("found_detail", kwargs={"found_id": self.found_item.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "found/found_item_detail.html")
        self.assertContains(response, self.found_item.items_name)
        self.assertContains(response, self.found_item.description)
        self.assertContains(response, self.found_item.found_at)

    def test_found_edit_view(self):
        """Test that the found_edit view works correctly for the owner."""
        response = self.client.get(
            reverse("found_edit", kwargs={"found_id": self.found_item.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "found/edit_found_item.html")
        self.assertContains(response, self.found_item.items_name)

    ### Lost Item Tests ###
    def test_create_lost_item_get(self):
        """Test GET request to create_lost_item view."""
        response = self.client.get(reverse("create_lost_item"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lost/create_lost_item.html")

    def test_create_lost_item_post_valid(self):
        """Test POST request with valid data to create a lost item."""
        data = {
            "items_name": "Lost Bag",
            "description": "Black backpack lost in the library.",
            "lost_at": "Library",
            "contact": "987654321",
            "founded_status": False,
            "image": self.mock_image,
        }
        response = self.client.post(reverse("create_lost_item"), data)
        self.assertRedirects(response, reverse("lost_items_list"))
        self.assertEqual(Lost.objects.count(), 2)
        lost_item = Lost.objects.last()
        self.assertEqual(lost_item.items_name, "Lost Bag")
        self.assertEqual(lost_item.description, "Black backpack lost in the library.")

    def test_lost_items_list_with_data(self):
        """Test lost_items_list view with data."""
        response = self.client.get(reverse("lost_items_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lost/lost_items_list.html")
        self.assertContains(response, "Lost Wallet")

    def test_lost_item_redirects_to_detail(self):
        """Test that clicking a Lost item redirects to the detail page."""
        response = self.client.get(
            reverse("lost_detail", kwargs={"lost_id": self.lost_item.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lost/lost_item_detail.html")
        self.assertContains(response, self.lost_item.items_name)
        self.assertContains(response, self.lost_item.description)
        self.assertContains(response, self.lost_item.lost_at)

    def test_lost_edit_view(self):
        """Test that the lost_edit view works correctly for the owner."""
        response = self.client.get(
            reverse("lost_edit", kwargs={"lost_id": self.lost_item.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lost/edit_lost_item.html")
        self.assertContains(response, self.lost_item.items_name)

    ### Ownership Tests ###
    def test_owner_can_delete_lost_item(self):
        """Test that the owner can delete a Lost item."""
        response = self.client.post(
            reverse("lost_delete", kwargs={"lost_id": self.lost_item.id})
        )
        self.assertRedirects(response, reverse("lost_items_list"))
        self.assertEqual(Lost.objects.count(), 0)

    def test_non_owner_cannot_edit_lost_item(self):
        """Test that a non-owner cannot access the edit page for a Lost item."""
        self.client.login(username="6610612222", password="password")
        response = self.client.get(
            reverse("lost_edit", kwargs={"lost_id": self.lost_item.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_non_owner_cannot_delete_lost_item(self):
        """Test that a non-owner cannot delete a Lost item."""
        self.client.login(username="6610612222", password="password")
        response = self.client.post(
            reverse("lost_delete", kwargs={"lost_id": self.lost_item.id})
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Lost.objects.count(), 1)
