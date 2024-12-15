from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Club, Announcement, Student
from .forms import ClubAnnouncementForm
from django.contrib.messages import get_messages


class ClubAnnouncementTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.club = Club.objects.create(title="Test Club")
        self.student = Student.objects.create(user=self.user, club=self.club)
        self.url = reverse("club_create_announcement")

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

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Announcement.objects.count(), 1)
        self.assertRedirects(
            response,
            reverse(
                "event-detail",
                kwargs={"announcement_id": Announcement.objects.first().id},
            ),
        )


class ClubListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.club = Club.objects.create(name="Test Club", origin="faculty_code")
        self.student = Student.objects.create(user=self.user, club=self.club)
        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            description="Test description",
            categories="clubs",
            club=self.club,
            date="2024-12-20",
            end_date="2024-12-21",
        )
        self.url = reverse("all_club_list")

    def test_all_club_list_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Club")
        self.assertContains(response, "Test Announcement")

    def test_all_club_list_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("login"))


class TUClubListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.club = Club.objects.create(name="TU Club", origin="tu")
        self.student = Student.objects.create(user=self.user, club=self.club)
        self.announcement = Announcement.objects.create(
            title="TU Club Announcement",
            description="Test description",
            categories="clubs",
            club=self.club,
            date="2024-12-20",
            end_date="2024-12-21",
        )
        self.url = reverse("tu_clubs_list")

    def test_tu_club_list_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TU Club")
        self.assertContains(response, "TU Club Announcement")

    def test_tu_club_list_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("login"))


class ClubDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.club = Club.objects.create(name="Test Club", origin="faculty_code")
        self.student = Student.objects.create(user=self.user, club=self.club)
        self.announcement = Announcement.objects.create(
            title="Test Club Announcement",
            description="Test description",
            categories="clubs",
            club=self.club,
            date="2024-12-20",
            end_date="2024-12-21",
        )
        self.url = reverse("club_detail", kwargs={"club_id": self.club.id})

    def test_club_detail_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Club")
        self.assertContains(response, "Test Club Announcement")

    def test_club_detail_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("login"))
