from django.test import TestCase, Client
from django.contrib.admin.sites import AdminSite, site
from django.contrib.auth.models import User
from .models import Student, Announcement, Club, Lost, Found
from .admin import StudentAdmin, AnnouncementAdmin, ClubAdmin, LostAdmin, FoundAdmin
from django.core.exceptions import ValidationError
from datetime import datetime
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.timezone import make_aware

# Create your tests here.


class AdminTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username="admintest",
            password="admintest1234",
            email="admintest@example.com",
        )

        self.user = User.objects.create_user(username="6610666666", password="usertest")
        self.student = Student.objects.create(
            student_id=6610000000,
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
            place="Puey Ungphakorn Centenary Hall and Park",
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

        self.announcement.title= "Updated Announcement"
        self.announcement.description= "This is the updated description."
        self.announcement.categories= "education"
        self.announcement.start_date= "2024-11-05 10:00:00"
        self.announcement.end_date= "2024-11-06 15:00:00"
        self.announcement.place= "Thammasat school of engineering"
        self.announcement.save()
        self.announcement.refresh_from_db()
        self.assertEqual(self.announcement.title, "Updated Announcement")
        self.assertEqual(
            self.announcement.description, "This is the updated description."
        )
        self.assertEqual(self.announcement.categories, "education")
        self.assertEqual(
            self.announcement.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "2024-11-05 03:00:00",
        )
        self.assertEqual(
            self.announcement.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "2024-11-06 08:00:00",
        )
        self.assertEqual(self.announcement.place, "Thammasat school of engineering")
        self.assertEqual(response.status_code, 200)

    def test_admin_can_edit_user(self):
        self.client.login(username="admintest", password="admintest1234")

        user_change_url = f"/admin/web_tu_events/student/{self.student.id}/change/"


        response = self.client.post(
            user_change_url,
            {
                "student_id": 6610680000,
                "name": "Update Student1",
                "email": "updatestudent1@example.com",
                "username": "6610000000"
            },
            follow=True,
        )
        self.student.student_id = 6610680000
        self.student.name = "Update Student1"
        self.student.email = "updatestudent1@example.com"
        self.student.username = "6610000000"
        self.student.save()
        self.student.refresh_from_db()

        self.assertEqual(self.student.student_id, 6610680000)
        self.assertEqual(self.student.name, "Update Student1")
        self.assertEqual(self.student.email, "updatestudent1@example.com")
        self.assertEqual(self.student.username, "6610000000")
        self.assertEqual(response.status_code, 200)
        
    def test_create_announcement(self):
        announcement = Announcement.objects.create(
            title="Event 1",
            description="Event1 description",
            categories="entertainment",
            start_date="2024-11-01 15:00:00",
            end_date="2024-11-02 17:00:00",
            place="Puey Ungphakorn Centenary Hall and Park",
        )        
        self.assertEqual(announcement.title, "Event 1")
        self.assertEqual(announcement.description, "Event1 description")
        self.assertEqual(announcement.categories, "entertainment")
        self.assertEqual(announcement.start_date, "2024-11-01 15:00:00")
        self.assertEqual(announcement.end_date, "2024-11-02 17:00:00")
        self.assertEqual(announcement.place, "Puey Ungphakorn Centenary Hall and Park")
        self.assertIsNotNone(announcement.id)        
        

    def test_create_announcement_with_missing_title(self):
        announcement = Announcement(
            title='',
            description='Test Description',
            categories='entertainment',
            start_date=datetime(2024, 1, 1, 10, 0, 0),
            end_date=datetime(2024, 1, 2, 10, 0, 0),
            place='Main Hall'
        )
        with self.assertRaises(ValidationError):
            announcement.full_clean() 

    def test_invalid_category(self):
        announcement = Announcement(
            title='Test Title',
            description='Test Description',
            categories='invalid_category',
            start_date=datetime(2024, 1, 1, 10, 0, 0),
            end_date=datetime(2024, 1, 2, 10, 0, 0),
            place='Main Hall'
        )
        with self.assertRaises(ValidationError):
            announcement.full_clean() 


            
