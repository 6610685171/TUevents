from django.test import TestCase
from web_tu_events.views import (
    get_faculty_by_code,
    get_faculty_name,
)


class FacultyFunctionsTest(TestCase):

    def test_get_faculty_by_code_valid(self):

        faculty_code = "01"
        faculty = get_faculty_by_code(faculty_code)
        self.assertEqual(faculty, "law")

        faculty_code = "02"
        faculty = get_faculty_by_code(faculty_code)
        self.assertEqual(faculty, "business")

        faculty_code = "11"
        faculty = get_faculty_by_code(faculty_code)
        self.assertEqual(faculty, "medicine")

    def test_get_faculty_by_code_invalid(self):

        faculty_code = "99"
        faculty = get_faculty_by_code(faculty_code)
        self.assertEqual(faculty, "law")

    def test_get_faculty_name_valid(self):

        faculty_code = "law"
        faculty_name = get_faculty_name(faculty_code)
        self.assertEqual(faculty_name, "Faculty of Law")

        faculty_code = "business"
        faculty_name = get_faculty_name(faculty_code)
        self.assertEqual(faculty_name, "Faculty of Business")

        faculty_code = "medicine"
        faculty_name = get_faculty_name(faculty_code)
        self.assertEqual(faculty_name, "Faculty of Medicine")

    def test_get_faculty_name_invalid(self):

        faculty_code = "unknown_faculty"
        faculty_name = get_faculty_name(faculty_code)
        self.assertEqual(faculty_name, "Unknown Faculty")

    def test_faculty_code_mapping(self):

        mappings = {
            "01": "law",
            "02": "business",
            "03": "political_science",
            "04": "economics",
            "05": "social_administration",
            "06": "liberal_arts",
            "07": "journalism_mass_comm",
            "08": "sociology_anthropology",
            "09": "science_technology",
            "10": "engineering",
            "11": "medicine",
            "12": "allied_health",
            "13": "dentistry",
        }

        for code, expected_faculty in mappings.items():
            self.assertEqual(get_faculty_by_code(code), expected_faculty)

    def test_faculty_name_mapping(self):
        names = {
            "law": "Faculty of Law",
            "business": "Faculty of Business",
            "political_science": "Faculty of Political Science",
            "economics": "Faculty of Economics",
            "social_administration": "Faculty of Social Administration",
            "sociology_anthropology": "Faculty of Sociology and Anthropology",
            "liberal_arts": "Faculty of Liberal Arts",
            "journalism_mass_comm": "Faculty of Journalism and Mass Communication",
            "science_technology": "Faculty of Science and Technology",
            "engineering": "Faculty of Engineering",
            "architecture_planning": "Faculty of Architecture and Planning",
            "medicine": "Faculty of Medicine",
            "allied_health": "Faculty of Allied Health Sciences",
            "dentistry": "Faculty of Dentistry",
            "nursing": "Faculty of Nursing",
            "public_health": "Faculty of Public Health",
        }

        for code, expected_name in names.items():
            self.assertEqual(get_faculty_name(code), expected_name)
