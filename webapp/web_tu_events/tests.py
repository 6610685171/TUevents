from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from django.contrib.admin.sites import AdminSite, site
from django.contrib.auth.models import User
from .models import Student, Announcement, Club, Lost, Found
from .admin import StudentAdmin, AnnouncementAdmin, ClubAdmin, LostAdmin, FoundAdmin


class AdminTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username="admintest",
            password="admintest1234",
            email="admintest@example.com",
        )

        # self.request = RequestFactory().get("/admin/")
        # self.request.user = self.user

        self.user = User.objects.create_user(username="6610666666", password="usertest")
        self.student = Student.objects.create(
            student_id="6610666666",
            name="Test Student1",
            email="teststudent1@example.com",
            username="6610666666",
        )
        self.announcement = Announcement.objects.create(
            title="Event 1",
            description="Event1 description",
            categories="entertainment",
            start_date="2024-11-01 15:00:00",
            end_date="2024-11-02 17:00:00",
            place="Puey 100 years",
        )
        self.club = Club.objects.create(
            title="testclub",
            origin="Thammasat School of Engineering",
            enable_to_join=True,
        )
        self.lost = Lost.objects.create(
            items_name="Wallet",
            lost_at="Thammasat School of Engineering",
            contact="0811111111",
            founded_status=False,
        )
        self.found = Found.objects.create(
            items_name="Key",
            found_at="Green Canteen",
            contact="9876543210",
            founded_status=True,
        )

        self.student_admin = StudentAdmin(Student, site)
        self.announcement_admin = AnnouncementAdmin(Announcement, AdminSite())
        self.club_admin = ClubAdmin(Club, site)
        self.lost_admin = LostAdmin(Lost, AdminSite())
        self.found_admin = FoundAdmin(Found, AdminSite())

    # def test_student_admin_queryset(self):
    #     # self.request.user.is_staff = False
    #     queryset = self.student_admin.get_queryset(self.request)
    #     self.assertQuerysetEqual(
    #         queryset,
    #         Student.objects.none(),
    #     )

    def test_student_admin_list_display(self):
        self.assertEqual(
            self.student_admin.list_display, ["student_id", "name", "email", "username"]
        )

    def test_student_admin_search_fields(self):
        self.assertEqual(
            self.student_admin.search_fields,
            ("name", "email", "student_id", "username"),
        )

    def test_student_admin_readonly_fields(self):
        self.assertEqual(self.student_admin.readonly_fields, ("password",))

    def test_announcement_admin_list_display(self):
        self.assertEqual(
            self.announcement_admin.list_display,
            ["title", "categories", "date", "start_date", "end_date"],
        )

    def test_club_admin_list_display(self):
        self.assertEqual(
            self.club_admin.list_display, ["title", "origin", "enable_to_join"]
        )

    def test_lost_admin_list_display(self):
        self.assertEqual(
            self.lost_admin.list_display,
            ["items_name", "lost_at", "contact", "founded_status"],
        )

    def test_found_admin_list_display(self):
        self.assertEqual(
            self.found_admin.list_display,
            ["items_name", "found_at", "contact", "founded_status"],
        )

    def test_admin_can_edit_annoucement(self):
        self.client.login(username="admintest", password="admintest1234")
        announcement_change_url = (
            f"/admin/web_tu_events/announcement/{self.announcement.id}/change/"
        )
        response = self.client.post(
            announcement_change_url,
            {
                "title": "Updated Announcement",
                "description": "This is the updated description.",
                "categories": "education",
                "start_date": "2024-11-05 10:00:00",
                "end_date": "2024-11-06 15:00:00",
                "place": "Thammasat school of engineering",
            },
            follow=True,
        )

        self.announcement.refresh_from_db()
        self.assertEqual(self.announcement.title, "Updated Announcement")
        self.assertEqual(
            self.announcement.description, "This is the updated description."
        )
        self.assertEqual(self.announcement.categories, "education")
        self.assertEqual(
            self.announcement.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "2024-11-05 10:00:00",
        )
        self.assertEqual(
            self.announcement.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "2024-11-06 15:00:00",
        )
        self.assertEqual(self.announcement.place, "Thammasat school of engineering")
        self.assertEqual(response.status_code, 200)

    def test_admin_can_edit_user(self):
        self.client.login(username="admintest", password="admintest1234")

        user_change_url = f"/admin/auth/user/{self.user.id}/change/"

        response = self.client.post(
            user_change_url,
            {
                "username": "updateuser",
                "email": "updateduser@example.com",
                "first_name": "Updated",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            },
            follow=True,
        )
        self.user.refresh_from_db()
        print(self.user)

        self.assertEqual(self.user.username, "updateuser")
        self.assertEqual(self.user.email, "updateduser@example.com")
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(response.status_code, 200)

