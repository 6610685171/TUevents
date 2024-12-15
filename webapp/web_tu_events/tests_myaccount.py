from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student, Interest, Announcement, Club, Lost, Found
from django.contrib import messages
from datetime import date
from .forms import StudentProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone


class MyAccountViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.student = Student.objects.create(
            user=self.user,
            email="test@example.com",
            name="Test Student",
            student_id=12345,
            username="testuser",
            password="password",
        )
        self.url = reverse("my_account")

    def test_my_account_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("my_account"))
        self.assertContains(response, "Test Student")

    def test_my_account_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, "/login/")


class MyEventsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.student = Student.objects.create(
            user=self.user,
            email="test@example.com",
            name="Test Student",
            student_id=12345,
            username="teststudent",
            password="password",
        )
        self.announcement = Announcement.objects.create(
            title="Test Event",
            description="Test Event Description",
            student=self.user.student,
            start_date=date.today(),
            end_date=date.today(),
        )
        self.interest = Interest.objects.create(
            user=self.user, announcement=self.announcement
        )
        self.url = reverse("my_events")

    def test_my_events_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("my_events"))
        self.assertContains(response, "Test Event")

    def test_my_events_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You haven't shown interest in any events yet.")


class ClubPostHistoryTest(TestCase):

    def setUp(self):
        now = timezone.now()
        self.user_with_student = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.student = Student.objects.create(user=self.user_with_student)
        self.user_with_student.student = self.student
        self.user_with_student.save()
        self.user_without_student = User.objects.create_user(
            username="testuser2", password="testpassword2"
        )
        self.announcement_1 = Announcement.objects.create(
            student=self.student,
            start_date=now,
            end_date=now + timezone.timedelta(days=1),
            title="Test Announcement 1",
            description="This is a test announcement.",
        )
        self.announcement_2 = Announcement.objects.create(
            student=self.student,
            start_date=now,
            end_date=now + timezone.timedelta(days=2),
            title="Test Announcement 2",
            description="This is a test announcement.",
        )

    def test_club_post_no_history(self):
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.get(reverse("my_club_post_history"))
        self.assertEqual(response.context["announcements"], [])

    def test_club_post_with_history(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("my_club_post_history"))
        announcements = response.context["announcements"]
        self.assertEqual(len(announcements), 2)
        self.assertEqual(announcements[0].title, "Test Announcement 1")
        self.assertEqual(announcements[1].title, "Test Announcement 2")

    def test_club_post_history_ordering(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("my_club_post_history"))
        announcements = response.context["announcements"]
        self.assertTrue(announcements[0].start_date >= announcements[1].start_date)


class ToggleInterestTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            description="This is a test event",
            start_date="2024-12-15 10:00:00",
            end_date="2024-12-15 12:00:00",
        )

    def test_toggle_interest_create(self):

        self.client.login(username="testuser", password="testpassword")

        url = reverse(
            "toggle_interest", kwargs={"announcement_id": self.announcement.id}
        )
        response = self.client.get(url)

        self.assertTrue(
            Interest.objects.filter(
                user=self.user, announcement=self.announcement
            ).exists()
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_toggle_interest_delete(self):
        Interest.objects.create(user=self.user, announcement=self.announcement)
        self.client.login(username="testuser", password="testpassword")
        url = reverse(
            "toggle_interest", kwargs={"announcement_id": self.announcement.id}
        )
        response = self.client.get(url)
        self.assertFalse(
            Interest.objects.filter(
                user=self.user, announcement=self.announcement
            ).exists()
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")


class EditProfileViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.student = Student.objects.create(
            user=self.user,
            username="testuser",
            email="test@example.com",
            student_id=12345,
        )
        self.url = reverse("edit_profile")
        self.original_image = self.student.image

    def test_edit_profile_view_get(self):

        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "my_account/edit_profile.html")
        self.assertContains(response, "<form")

    def test_edit_profile_view_post_valid_with_image(self):

        self.client.login(username="testuser", password="password123")
        new_image = SimpleUploadedFile(
            name="new_profile_pic.jpg",
            content=b"file_content",
            content_type="image/jpeg",
        )
        data = {"image": new_image}
        response = self.client.post(self.url, data, follow=True)
        self.student.refresh_from_db()
        self.assertNotEqual(self.student.image.name, self.original_image.name)

    def test_edit_profile_view_post_valid_remove_image(self):

        self.client.login(username="testuser", password="password123")

        data = {
            "image": "",
            "remove_image": "on",
        }

        response = self.client.post(self.url, data, follow=True)

        self.student.refresh_from_db()
        self.assertEqual(self.student.image.name, "")

        self.assertRedirects(response, reverse("my_account"))

    def test_edit_profile_view_post_invalid(self):

        self.client.login(username="testuser", password="password123")

        response = self.client.post(self.url, {}, follow=True)

        form = response.context.get("form")

        self.assertFalse(form.errors.get("image"))


class LostFoundHistoryViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="password")

        self.student = Student.objects.create(
            user=self.user,
            name="Test Student",
            email="test@student.com",
            student_id=12345,
        )
        self.user.student = self.student
        self.user.save()

        self.lost_item = Lost.objects.create(
            items_name="Lost Phone",
            description="Lost my phone near the cafeteria",
            lost_at="Library",
            contact="testcontact",
            student=self.student,
            founded_status=False,
        )
        self.found_item = Found.objects.create(
            items_name="Found Wallet",
            description="Found a wallet in the park",
            found_at="Park",
            contact="testcontact",
            student=self.student,
            founded_status=True,
        )

        self.url = reverse("lost_found_history")

    def test_lost_found_history_view_for_authenticated_user(self):
        self.client.login(username="testuser", password="password")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lost Phone")
        self.assertContains(response, "Found Wallet")
        self.assertContains(response, "Library")

    def test_lost_found_history_view_for_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Lost Phone")
        self.assertNotContains(response, "Found Wallet")

    def test_lost_found_history_view_for_user_without_student_profile(self):

        no_student_user = User.objects.create_user(
            username="no_student_user", password="password"
        )

        self.client.login(username="no_student_user", password="password")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Lost Phone")
        self.assertNotContains(response, "Found Wallet")
