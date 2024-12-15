from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student, Interest, Announcement, Club
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
