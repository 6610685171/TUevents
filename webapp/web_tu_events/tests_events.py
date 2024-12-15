from django.test import TestCase, Client
from django.urls import reverse
from .models import Announcement, Student, Interest, Club
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


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
        response = self.client.get(
            reverse("category_events", args=["entertainment"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event1")
        self.assertNotContains(response, "Test Event2")

    def test_nothing_to_show_on_category_events(self):
        response = self.client.get(
            reverse("category_events", args=["invalid"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Result.")


class EventEditTest(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.student = Student.objects.create(
            user=self.user, username="testuser")

        self.announcement = Announcement.objects.create(
            title="Test Event", description="Test Description", start_date="2024-12-01", end_date="2024-12-15", student=self.student)

        self.url = reverse("event-edit", args=[self.announcement.id])

    def test_event_edit_view_get(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/edit_event.html")

    def test_event_edit_permission(self):

        other_user = get_user_model().objects.create_user(
            username="otheruser", password="password123"
        )
        other_student = Student.objects.create(
            user=other_user, username="otheruser")
        other_announcement = Announcement.objects.create(
            student=other_student, title="Other Event", description="Other Description", start_date="2024-12-01", end_date="2024-12-15"
        )

        self.client.login(username="testuser", password="password123")
        response = self.client.get(
            reverse("event-edit", args=[other_announcement.id]))

        self.assertRedirects(
            response, reverse("event-detail", args=[other_announcement.id])
        )

    def test_event_edit_valid_post(self):
        self.client.login(username="testuser", password="password123")
        data = {"title": "Updated Event", "description": "Updated Description"}
        response = self.client.post(self.url, data)
        self.announcement.refresh_from_db()

        self.assertEqual(self.announcement.title, "Updated Event")
        self.assertEqual(self.announcement.description, "Updated Description")
        self.assertRedirects(
            response, reverse("event-detail", args=[self.announcement.id])
        )

    def test_event_edit_invalid_post(self):
        self.client.login(username="testuser", password="password123")
        data = {"title": "", "description": "Updated Description"}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', "title",
                             "This field is required.")


class EventDeleteTest(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.student = Student.objects.create(
            user=self.user, username="testuser")

        self.announcement = Announcement.objects.create(
            student=self.student, title="Test Event", description="Test Description", start_date="2024-12-01", end_date="2024-12-15"
        )

        self.url = reverse("event-delete", args=[self.announcement.id])

    def test_event_delete_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse("clubs_announcement_list"))

    def test_event_delete_permission(self):
        other_user = get_user_model().objects.create_user(
            username="otheruser", password="password123"
        )
        other_student = Student.objects.create(
            user=other_user, username="otheruser")
        other_announcement = Announcement.objects.create(
            student=other_student, title="Other Event", description="Other Description", start_date="2024-12-01", end_date="2024-12-15"
        )

        self.client.login(username="testuser", password="password123")
        response = self.client.get(
            reverse("event-delete", args=[other_announcement.id])
        )

        self.assertRedirects(response, reverse("clubs_announcement_list"))

    def test_event_delete_success(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)

        self.assertFalse(Announcement.objects.filter(
            id=self.announcement.id).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         "Announcement deleted successfully!")
