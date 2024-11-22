from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class LoginViewTests(TestCase):
    def setUp(self):
        # Create test users
        self.student_user = User.objects.create_user(
            username="6610611111", password="studentpassword"
        )
        self.admin_user = User.objects.create_superuser(
            username="adminuser", password="adminpassword"
        )
        self.club_user = User.objects.create_user(
            username="clubuser", password="clubpassword"
        )
        self.login_url = reverse("login")

    def post_login(self, username, password):
        """Helper function to simulate a login POST request."""
        return self.client.post(
            self.login_url, {"username": username, "password": password}
        )

    def test_invalid_username(self):
        response = self.post_login("nonexistentuser", "password")
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Invalid username.", messages)
        self.assertRedirects(response, self.login_url)

    def test_invalid_password(self):
        response = self.post_login("clubuser", "wrongpassword")
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Invalid password.", messages)
        self.assertRedirects(response, self.login_url)

    def test_missing_username_and_password(self):
        response = self.post_login("", "")
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Both fields are required.", messages)
        self.assertRedirects(response, self.login_url)

    def test_student_login(self):
        response = self.post_login("6610611111", "studentpassword")
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Welcome, Student!", messages)
        self.assertTemplateUsed(response, "home.html")

    def test_admin_login(self):
        response = self.post_login("adminuser", "adminpassword")
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Welcome, Admin! Redirecting to the admin panel.", messages)
        self.assertRedirects(response, reverse("admin:index"))

    def test_club_account_login(self):
        response = self.post_login("clubuser", "clubpassword")
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Welcome, Club Account!", messages)
        self.assertTemplateUsed(response, "home.html")
