from django.test import TestCase, Client
from django.urls import reverse
from .models import Announcement, Student, Interest, Club
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone


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


class MyAccountViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="6610611111", password="password123"
        )
        self.student = Student.objects.create(user=self.user, student_id="6610611111")

        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.admin_student = Student.objects.create(
            user=self.admin_user, student_id="6610622222"
        )

        self.club = Club.objects.create(name="Test Club", origin="01")
        self.announcement = Announcement.objects.create(
            title="Test Event",
            description="This is a test event.",
            student=self.student,
            categories="clubs",
        )
        self.interest = Interest.objects.create(
            user=self.user, announcement=self.announcement
        )

    def test_toggle_interest(self):
        self.client.login(username="6610611111", password="password123")

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

    def test_my_account(self):
        self.client.login(username="6610611111", password="password123")

        response = self.client.get(reverse("my_account"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Personal Information")

    def test_event_edit(self):
        self.client.login(username="6610622222", password="password123")

        response = self.client.get(reverse("event-edit", args=[self.announcement.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("event-edit", args=[self.announcement.id]),
            {
                "title": "Updated Event",
                "description": "Updated content for the event.",
            },
        )
        self.announcement.refresh_from_db()
        self.assertEqual(self.announcement.title, "Updated Event")
        self.assertEqual(
            self.announcement.description, "Updated content for the event."
        )

    def test_event_delete(self):
        self.client.login(username="6610622222", password="password123")

        response = self.client.post(
            reverse("event-delete", args=[self.announcement.id])
        )
        self.assertRedirects(response, reverse("clubs_announcement_list"))
        with self.assertRaises(Announcement.DoesNotExist):
            self.announcement.refresh_from_db()

    def test_club_post_history(self):
        self.client.login(username="6610622222", password="password123")

        response = self.client.get(reverse("club_post_history"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Club Posts")
        self.assertContains(response, self.announcement.title)

    def test_all_club_list_admin(self):
        self.client.login(username="admin", password="adminpass")

        response = self.client.get(reverse("all_club_list_admin"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All Clubs")
        self.assertContains(response, self.club.title)

    def test_clubs_by_faculty_admin(self):
        self.client.login(username="admin", password="adminpass")

        response = self.client.get(reverse("clubs_by_faculty_admin"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Faculty Clubs")
        self.assertContains(response, self.club.title)
