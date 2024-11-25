from django.test import TestCase
from django.urls import reverse
from .models import Announcement
from datetime import datetime, timedelta


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
