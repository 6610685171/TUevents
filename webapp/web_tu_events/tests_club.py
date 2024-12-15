from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Club, Announcement, Student
from .forms import ClubAnnouncementForm
from django.contrib.messages import get_messages
from django.utils import timezone
import datetime


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


class ClubListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.club = Club.objects.create(title="Test Club", origin="medicine")
        self.student = Student.objects.create(user=self.user, club=self.club)
        start_date = timezone.make_aware(datetime.datetime(2024, 12, 20))
        end_date = timezone.make_aware(datetime.datetime(2024, 12, 21))

        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            description="Test description",
            categories="clubs",
            club=self.club,
            start_date=start_date,
            end_date=end_date,
        )
        self.url = reverse("clubs_announcement_list")

    def test_all_club_list_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, 200
        )  # Expecting 200 since the user is logged in
        # self.assertContains(response, "Test Club")
        self.assertContains(response, "Test Announcement")

    def test_all_club_list_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("login"))


# class TUClubListViewTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", password="testpassword"
#         )
#         self.club = Club.objects.create(name="TU Club", origin="tu")
#         self.student = Student.objects.create(user=self.user, club=self.club)
#         self.announcement = Announcement.objects.create(
#             title="TU Club Announcement",
#             description="Test description",
#             categories="clubs",
#             club=self.club,
#             date="2024-12-20",
#             end_date="2024-12-21",
#         )
#         self.url = reverse("tu_clubs_list")

#     def test_tu_club_list_authenticated(self):
#         self.client.login(username="testuser", password="testpassword")
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "TU Club")
#         self.assertContains(response, "TU Club Announcement")

#     def test_tu_club_list_not_authenticated(self):
#         response = self.client.get(self.url)
#         self.assertRedirects(response, reverse("login"))


# class ClubAnnouncementTests(TestCase):

#     def setUp(self):
#         # Create test users and students
#         self.user1 = User.objects.create_user(
#             username="testuser1", password="password123"
#         )
#         self.user2 = User.objects.create_user(
#             username="testuser2", password="password123"
#         )
#         self.club = Club.objects.create(title="Test Club", origin="tu")
#         self.student1 = Student.objects.create(
#             user=self.user1, student_id="6610611111", club=self.club
#         )
#         self.student2 = Student.objects.create(user=self.user2, student_id="6610611112")

#     def test_create_announcement_as_member(self):
#         self.client.login(username="testuser1", password="password123")

#         # POST request to create an announcement
#         data = {
#             "title": "Test Announcement",
#             "description": "This is a test announcement.",
#             "start_date": "2024-12-20T12:00",
#             "end_date": "2024-12-21T12:00",
#             "place": "TU",
#             "club": self.club.id,  # Make sure the club field is filled
#         }
#         response = self.client.post(reverse("club_create_announcement"), data)

#         # Check the response and database state
#         self.assertEqual(response.status_code, 302)  # Redirect after success
#         self.assertTrue(Announcement.objects.filter(title="Test Announcement").exists())

#     def test_create_announcement_as_non_member(self):
#         self.client.login(username="testuser2", password="password123")

#         # Attempt to create an announcement without being in any club
#         data = {
#             "title": "Test Announcement",
#             "description": "This is a test announcement.",
#             "start_date": "2024-12-20T12:00",
#             "end_date": "2024-12-21T12:00",
#             "place": "TU",
#             "club": self.club.id,
#         }
#         response = self.client.post(reverse("club_create_announcement"), data)

#         # Should redirect to home as the user is not part of any club
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, "/")  # The redirect URL can be adjusted


# class AllClubListTests(TestCase):

#     def setUp(self):
#         # Create test users and students
#         self.admin_user = User.objects.create_superuser(
#             username="admin", password="adminpass"
#         )
#         self.user = User.objects.create_user(
#             username="testuser1", password="password123"
#         )
#         self.club = Club.objects.create(title="Test Club", origin="tu")
#         self.student = Student.objects.create(
#             user=self.user, student_id="6610611111", club=self.club
#         )

#     def test_all_club_list_as_admin(self):
#         self.client.login(username="admin", password="adminpass")

#         # Get the page showing all clubs
#         response = self.client.get(reverse("all_club_list"))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.club.title)  # Should contain club title

#     def test_all_club_list_as_member(self):
#         self.client.login(username="testuser1", password="password123")

#         # Get the page showing clubs specific to the user's faculty
#         response = self.client.get(reverse("all_club_list"))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.club.title)  # Should contain club title


# class TuClubsListTests(TestCase):

#     def setUp(self):
#         # Create test users and students
#         self.user = User.objects.create_user(
#             username="testuser1", password="password123"
#         )
#         self.club = Club.objects.create(title="TU Club", origin="tu")
#         self.student = Student.objects.create(
#             user=self.user, student_id="6610611111", club=self.club
#         )

#     def test_tu_clubs_list(self):
#         self.client.login(username="testuser1", password="password123")

#         # Get the TU clubs page
#         response = self.client.get(reverse("tu_clubs_list"))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.club.title)  # Should contain TU club title


# class ClubDetailTests(TestCase):

#     def setUp(self):
#         # Create test users and students
#         self.user = User.objects.create_user(
#             username="testuser1", password="password123"
#         )
#         self.club = Club.objects.create(title="Test Club", origin="tu")
#         self.student = Student.objects.create(
#             user=self.user, student_id="6610611111", club=self.club
#         )
#         self.announcement = Announcement.objects.create(
#             title="Test Event",
#             description="Test event description",
#             start_date="2024-12-20T12:00",
#             end_date="2024-12-21T12:00",
#             place="TU",
#             club=self.club,
#             student=self.student,
#         )

#     def test_club_detail(self):
#         self.client.login(username="testuser1", password="password123")

#         # Access the club detail page
#         response = self.client.get(reverse("club_detail", args=[self.club.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.club.title)  # Should display club title
#         self.assertContains(
#             response, self.announcement.title
#         )  # Should display announcement
