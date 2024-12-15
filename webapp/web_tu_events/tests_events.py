from django.test import TestCase, Client
from django.urls import reverse
from .models import Announcement, Student, Interest, Club
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model


class AnnouncementTests(TestCase):
    def setUp(self):
        self.announcement1 = Announcement.objects.create(
            title="Test Event1",
            description="This is test event",
            categories="entertainment",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            place="Thammasat school of engineering",
        )
        self.announcement2 = Announcement.objects.create(
            title="Test Event2",
            description="This is test event",
            categories="sports",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=2),
            place="Main Stadium",
        )

    def test_all_events(self):
        response = self.client.get(reverse("all_events"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event1")
        self.assertContains(response, "Test Event2")

    def test_incorrect_event_detail(self):
        response = self.client.get(reverse("event-detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_event_detail(self):
        response = self.client.get(
            reverse("event-detail", args=[self.announcement1.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_category_events(self):
        response = self.client.get(reverse("category_events", args=["entertainment"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event1")
        self.assertNotContains(response, "Test Event2")

    def test_nothing_to_show_on_category_events(self):
        response = self.client.get(reverse("category_events", args=["invalid"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Result.")


class EventEditTest(TestCase):

    def setUp(self):
        # Create users
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="password1"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="password2"
        )

        # Create a club and announcements for the users
        self.club = Club.objects.create(name="Art Club", origin="liberal_arts")
        self.announcement = Announcement.objects.create(
            title="Art Event",
            categories="clubs",
            student=self.user1.student,
            club=self.club,
        )

    def test_event_edit_valid(self):
        # Log in as user1
        self.client.login(username="user1", password="password1")

        # Update data for the announcement
        data = {
            "title": "Updated Art Event",
            "categories": "clubs",
            "club": self.club.id,
        }

        response = self.client.post(
            reverse("event_edit", args=[self.announcement.id]), data
        )

        # Check if the redirect occurs to the correct detail page
        self.assertRedirects(
            response, reverse("event-detail", args=[self.announcement.id])
        )

        # Fetch the updated announcement from the database
        self.announcement.refresh_from_db()

        # Assert the title is updated
        self.assertEqual(self.announcement.title, "Updated Art Event")

    def test_event_edit_not_owner(self):
        # Log in as user2 (not the owner)
        self.client.login(username="user2", password="password2")

        # Try to edit the announcement
        response = self.client.get(reverse("event_edit", args=[self.announcement.id]))

        # The user should be redirected to the event-detail page because they aren't the owner
        self.assertRedirects(
            response, reverse("event-detail", args=[self.announcement.id])
        )

    def test_event_edit_not_logged_in(self):
        # Try to access the edit page without logging in
        response = self.client.get(reverse("event_edit", args=[self.announcement.id]))

        # Ensure the user is redirected to the login page
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('event_edit', args=[self.announcement.id])}",
        )
