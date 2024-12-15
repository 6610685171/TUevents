from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Announcement, Interest, Club
from datetime import datetime
from django.utils import timezone


class HomeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teststudent", password="studentpassword"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="user2password"
        )
        self.club = Club.objects.create(origin="tu", title="Test Club")
        self.announcement1 = Announcement.objects.create(
            title="Event1",
            categories="sports",
            date="2024-01-01",
            # start_date="2024-01-01T10:00:00Z", end_date="2024-01-01T12:00:00Z"
        )
        self.announcement2 = Announcement.objects.create(
            title="Alert",
            categories="alerts",
            date="2024-01-02",
            # start_date="2024-01-02T10:00:00Z", end_date="2024-01-02T12:00:00Z"
        )
        self.announcement3 = Announcement.objects.create(
            title="EventClub",
            categories="clubs",
            date="2024-01-02",
            # start_date="2024-01-02T10:00:00Z", end_date="2024-01-02T12:00:00Z"
        )
        Interest.objects.create(user=self.user, announcement=self.announcement1)

    def test_home_view_guest_user(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "alert")
        self.assertContains(response, "Events")

    def test_home_view_logged_in_user_with_interest(self):
        self.client.login(username="teststudent", password="studentpassword")
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Alert")
        self.assertContains(response, "Event1")
        self.assertContains(response, "EventClub")
        self.assertTrue(
            Interest.objects.filter(
                user=self.user, announcement=self.announcement1
            ).exists()
        )

    def test_home_view_logged_in_user_without_interest(self):
        self.client.login(username="user2", password="user2password")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Alert")
        self.assertContains(response, "Event1")
        self.assertContains(response, "EventClub")
        self.assertFalse(Interest.objects.filter(user=self.user2).exists())
