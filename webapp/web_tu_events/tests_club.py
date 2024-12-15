from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Club, Announcement, Student, Interest
from .forms import ClubAnnouncementForm
from django.contrib.messages import get_messages
from django.utils import timezone
from unittest.mock import patch
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib import messages
from web_tu_events.views import get_faculty_by_code, get_faculty_name


class ClubAnnouncementTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.club = Club.objects.create(title="Test Club")
        self.student = Student.objects.create(user=self.user, club=self.club)
        self.url = reverse("clubs_create_announcement")

    def test_create_announcement_success(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            self.url,
            {
                "title": "Test Announcement",
                "description": "This is a test announcement.",
                "date": "2024-12-20",
                "end_date": "2024-12-21",
            },
        )

        self.assertEqual(response.status_code, 200)


class AllClubListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.student = Student.objects.create(user=self.user, student_id="12345678")
        self.club = Club.objects.create(title="Sample Club", origin="law")
        self.announcement = Announcement.objects.create(
            title="Club Announcement",
            description="This is an announcement",
            categories="clubs",
            club=self.club,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
        )
        self.interest = Interest.objects.create(
            user=self.user, announcement=self.announcement
        )

    def test_all_club_list_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("clubs_announcement_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Club")
        self.assertContains(response, "Club Announcement")

    def test_all_club_list_unauthenticated(self):

        response = self.client.get(reverse("clubs_announcement_list"))

        self.assertRedirects(response, "/login/")


class TUClubsListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.student = Student.objects.create(user=self.user, student_id="12345678")
        self.club = Club.objects.create(title="TU Club", origin="tu")
        self.announcement = Announcement.objects.create(
            title="TU Club Announcement",
            description="This is an announcement",
            categories="clubs",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            club=self.club,
        )

    def test_tu_clubs_list_authenticated(self):

        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("tu_clubs"))
        self.assertContains(response, "TU Club")


class ClubDetailViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="password")
        self.student = Student.objects.create(user=self.user, student_id="12345678")
        self.club = Club.objects.create(title="Sample Club", origin="law")
        self.announcement = Announcement.objects.create(
            title="Sample Club Announcement",
            description="This is an announcement for the club",
            categories="clubs",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            club=self.club,
        )

    def test_club_detail_authenticated(self):

        self.client.login(username="testuser", password="password")

        response = self.client.get(
            reverse("club_detail", kwargs={"club_id": self.club.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Club")
        self.assertContains(response, "Sample Club Announcement")


class AllClubListAdminViewTest(TestCase):

    def setUp(self):

        self.admin_user = User.objects.create_superuser(
            username="admin", password="password"
        )
        self.club = Club.objects.create(title="Sample All Club", origin="business")
        self.announcement = Announcement.objects.create(
            title="All Club Announcement",
            description="This is an announcement for the all club",
            categories="clubs",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            club=self.club,
        )

    def test_all_club_list_admin_authenticated(self):
        self.client.login(username="admin", password="password")
        response = self.client.get(reverse("clubs_announcement_list_admin"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Sample All Club")
        self.assertContains(response, "All Club Announcement")

    def test_all_club_list_admin_unauthorized(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        response = self.client.get(reverse("clubs_announcement_list_admin"))

        self.assertContains(response, "You do not have permission to view this page.")


class ClubsByFacultyAdminTestCase(TestCase):

    def setUp(self):
        # Create a superuser for permission testing
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password123"
        )

        # Create a regular user
        self.user = User.objects.create_user(
            username="user", email="user@example.com", password="password123"
        )

        # Create some clubs and announcements
        self.club1 = Club.objects.create(title="Club 1", origin="other")
        self.club2 = Club.objects.create(title="Club 2", origin="other")

        self.announcement1 = Announcement.objects.create(
            title="Announcement 1",
            categories="clubs",
            club=self.club1,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
        )
        self.announcement2 = Announcement.objects.create(
            title="Announcement 2",
            categories="clubs",
            club=self.club2,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
        )

    def test_clubs_by_faculty_admin_permission_for_superuser(self):
        self.client.login(username="admin", password="password123")
        response = self.client.get(reverse("clubs_by_faculty_admin"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Club 1")
        self.assertContains(response, "Club 2")
        self.assertContains(response, "Announcement 1")
        self.assertContains(response, "Announcement 2")

    def test_clubs_by_faculty_admin_no_user_logged_in(self):
        response = self.client.get(reverse("clubs_by_faculty_admin"))
        self.assertEqual(response.status_code, 200)
