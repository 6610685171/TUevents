from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Announcement, Interest, Club
from datetime import datetime
from django.utils import timezone
from datetime import date


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
            end_date=date(2024, 12, 31),
            start_date=date(2024, 12, 1)
        )
        self.announcement2 = Announcement.objects.create(
            title="Alert",
            categories="alerts",
            date="2024-01-02",
            end_date=date(2024, 12, 31),
            start_date=date(2024, 12, 1)
        )
        self.announcement3 = Announcement.objects.create(
            title="EventClub",
            categories="clubs",
            date="2024-01-02",
            end_date=date(2024, 12, 31),
            start_date=date(2024, 12, 1)
        )
        Interest.objects.create(
            user=self.user, announcement=self.announcement1)

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

    def test_alerts_redirect(self):
        response = self.client.get(reverse('home'))
        expected_url = reverse("event-detail", args=[self.announcement2.id])
        self.assertIn(f'<a href="{expected_url}"',
                      response.content.decode('utf-8'))

    def test_specific_text_display(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Welcome")
        self.assertContains(response, "to TU Event")

    def test_event_redirect(self):
        response = self.client.get(reverse('home'))
        expected_url = "/events/all_events.html/"
        self.assertIn(f'<a href="{expected_url}"',
                      response.content.decode('utf-8'))

    def test_club_redirect_not_login(self):
        response = self.client.get(reverse('home'))
        expected_url = "/login/"
        self.assertIn(f'<a href="{expected_url}"',
                      response.content.decode('utf-8'))

    def test_club_redirect_not_login_have_message(self):
        response = self.client.get(reverse('home'))
        self.assertIn(
            'You have to login first to see all the announcements from clubs.', response.content.decode())

    def test_lostfound_redirect(self):
        response = self.client.get(reverse('home'))
        expected_url = "/lost/list/"
        self.assertRegex(
            response.content.decode('utf-8'),
            rf'<a[^>]+href="{expected_url}"[^>]*>')

    def test_about_redirect(self):
        response = self.client.get(reverse('home'))
        self.assertIn('<a class="nav-link" href="/about">About</a>',
                      response.content.decode('utf-8'))

    def test_myaccount_redirect(self):
        response = self.client.get(reverse('home'))
        self.assertIn('href="/my_account/personal_info"',
                      response.content.decode())
