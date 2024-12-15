from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Announcement, Interest, Student, Club
from unittest.mock import patch


class MyAccountViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.student = Student.objects.create(user=self.user, student_id="12345678")
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.admin_student = Student.objects.create(
            user=self.admin_user, student_id="87654321"
        )

        self.club = Club.objects.create(name="Test Club", origin="01")
        self.announcement = Announcement.objects.create(
            title="Test Event",
            content="This is a test event.",
            student=self.user.student,
            categories="clubs",
        )
        self.interest = Interest.objects.create(
            user=self.user, announcement=self.announcement
        )

    def test_toggle_interest(self):
        self.client.login(username="testuser", password="password123")

        response = self.client.post(
            reverse("toggle_interest", args=[self.announcement.id])
        )
        self.assertRedirects(response, "/")
        self.assertTrue(
            Interest.objects.filter(
                user=self.user, announcement=self.announcement
            ).exists()
        )

        response = self.client.post(
            reverse("toggle_interest", args=[self.announcement.id])
        )
        self.assertRedirects(response, "/")
        self.assertFalse(
            Interest.objects.filter(
                user=self.user, announcement=self.announcement
            ).exists()
        )
