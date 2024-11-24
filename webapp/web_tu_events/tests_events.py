from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Announcement
from datetime import datetime, timedelta


class ClubAnnouncementTests(TestCase):
    def setUp(self):
        self.club_user = User.objects.create_user(
            username="tu_clubadmin", password="password"
        )
        self.non_club_user = User.objects.create_user(
            username="john_doe", password="password"
        )
        self.client = Client()

        # Valid data
        self.valid_data = {
            "title": "Test Announcement",
            "description": "This is a valid test announcement.",
            "start_date": (datetime.now() + timedelta(days=1)).strftime(
                "%Y-%m-%dT%H:%M"
            ),
            "end_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M"),
            "place": "Clubhouse",
        }

        # Invalid data
        self.invalid_data = self.valid_data.copy()
        self.invalid_data["title"] = ""  # Title left blank

    def test_redirect_if_not_club_user(self):
        self.client.login(username="john_doe", password="password")
        response = self.client.get(reverse("clubs_create_announcement"))
        self.assertRedirects(response, reverse("home"))

    def test_club_user_access_create_view(self):
        self.client.login(username="tu_clubadmin", password="password")
        response = self.client.get(reverse("clubs_create_announcement"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "club/club_create_announcement.html")

    def test_post_valid_club_announcement(self):
        self.client.login(username="tu_clubadmin", password="password")
        response = self.client.post(
            reverse("clubs_create_announcement"), data=self.valid_data
        )
        self.assertRedirects(response, reverse("clubs_announcement_list"))
        self.assertEqual(Announcement.objects.count(), 1)
        announcement = Announcement.objects.first()
        self.assertEqual(announcement.title, "Test Announcement")

    def test_post_invalid_club_announcement(self):
        self.client.login(username="tu_clubadmin", password="password")
        response = self.client.post(
            reverse("clubs_create_announcement"), data=self.invalid_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "club/club_create_announcement.html")
        self.assertFormError(response, "form", "title", "This field is required.")
        self.assertEqual(Announcement.objects.count(), 0)

    def test_all_club_announcements_view(self):
        Announcement.objects.create(
            title="Club Event",
            description="This is a sample announcement.",
            start_date=datetime.now() + timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2),
            categories="clubs",
            place="Clubhouse",
        )
        response = self.client.get(reverse("clubs_announcement_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "club/club_announcement_list.html")
        self.assertContains(response, "Club Event")
        self.assertQuerysetEqual(
            response.context["announcements"],
            Announcement.objects.filter(categories="clubs").order_by("-date"),
            transform=lambda x: x,
        )

    def test_empty_club_announcement_list(self):
        response = self.client.get(reverse("clubs_announcement_list"))
        self.assertContains(response, "No announcements available.")

    def test_non_authenticated_user_redirect(self):
        response = self.client.get(reverse("clubs_create_announcement"))
        self.assertRedirects(
            response, f'/login/?next={reverse("clubs_create_announcement")}'
        )

    def test_invalid_category_exclusion(self):
        Announcement.objects.create(
            title="Invalid Announcement",
            description="Should not be visible.",
            categories="events",
        )
        response = self.client.get(reverse("clubs_announcement_list"))
        self.assertNotContains(response, "Invalid Announcement")

    def test_date_ordering(self):
        Announcement.objects.create(
            title="Older Announcement",
            description="This is older.",
            start_date=datetime.now() - timedelta(days=10),
            end_date=datetime.now() - timedelta(days=5),
            categories="clubs",
            place="Clubhouse",
        )
        Announcement.objects.create(
            title="Newer Announcement",
            description="This is newer.",
            start_date=datetime.now() + timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2),
            categories="clubs",
            place="Clubhouse",
        )
        response = self.client.get(reverse("clubs_announcement_list"))
        announcements = response.context["announcements"]
        self.assertGreater(announcements[0].date, announcements[1].date)

    def test_missing_dates_in_post(self):
        self.client.login(username="tu_clubadmin", password="password")
        incomplete_data = self.valid_data.copy()
        incomplete_data.pop("start_date")  # Remove required field
        response = self.client.post(
            reverse("clubs_create_announcement"), data=incomplete_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "start_date", "This field is required.")
