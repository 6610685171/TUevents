from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Student


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="teststudent", password="studentpassword"
        )
        self.superuser = User.objects.create_superuser(
            username="testadmin", password="adminpassword"
        )
        self.student = Student.objects.create(
            user=self.user,
            email="student@example.com",
            name="Test Student",
            student_id=12345,
            username="teststudent",
            password="studentpassword",
        )
        self.url = reverse("login")

    def test_login_valid_user(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "teststudent",
                "password": "studentpassword",
            },
        )
        self.assertRedirects(response, reverse("home"))

    def test_login_invalid_username(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "invaliduser",
                "password": "studentpassword",
            },
        )
        self.assertContains(response, "Invalid username.")
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_password(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "teststudent",
                "password": "invalidpassword",
            },
        )
        self.assertContains(response, "Invalid password.")
        self.assertEqual(response.status_code, 200)

    def test_login_redirect_to_admin_for_superuser(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testadmin",
                "password": "adminpassword",
            },
        )
        self.assertRedirects(response, reverse("admin:index"))

    def test_login_with_next_url(self):
        next_url = "/my_account/personal_info"
        response = self.client.post(
            reverse("login") + f"?next={next_url}",
            {
                "username": "teststudent",
                "password": "studentpassword",
            },
        )
        self.assertRedirects(response, next_url)

    def test_login_view_get_method(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "login.html")
        self.assertIsInstance(response.context["form"], AuthenticationForm)

    def test_logout(self):
        self.client.login(username="teststudent", password="studentpassword")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
