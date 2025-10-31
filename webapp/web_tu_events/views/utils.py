def get_faculty_by_code(faculty_code):
    faculty_map = {
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
    return faculty_map.get(faculty_code, "law")  # ค่าพื้นฐานคือ 'law'


def get_faculty_name(faculty_code):
    faculties = {
        "law": "Faculty of Law (คณะนิติศาสตร์)",
        "business": "Faculty of Business (คณะพาณิชยศาสตร์และการบัญชี)",
        "political_science": "Faculty of Political Science (คณะรัฐศาสตร์)",
        "economics": "Faculty of Economics (คณะเศรษฐศาสตร์)",
        "social_administration": "Faculty of Social Administration (คณะสังคมสงเคราะห์ศาสตร์)",
        "sociology_anthropology": "Faculty of Sociology and Anthropology (คณะสังคมวิทยาและมานุษยวิทยา)",
        "liberal_arts": "Faculty of Liberal Arts (คณะศิลปศาสตร์)",
        "journalism_mass_comm": "Faculty of Journalism and Mass Communication (คณะวารสารศาสตร์และสื่อสารมวลชน)",
        "science_technology": "Faculty of Science and Technology (คณะวิทยาศาสตร์และเทคโนโลยี)",
        "engineering": "Faculty of Engineering (คณะวิศวกรรมศาสตร์)",
        "architecture_planning": "Faculty of Architecture and Planning (คณะสถาปัตยกรรมศาสตร์และการผังเมือง)",
        "medicine": "Faculty of Medicine (คณะแพทยศาสตร์)",
        "allied_health": "Faculty of Allied Health Sciences (คณะสหเวชศาสตร์)",
        "dentistry": "Faculty of Dentistry (คณะทันตแพทยศาสตร์)",
        "nursing": "Faculty of Nursing (คณะพยาบาลศาสตร์)",
        "public_health": "Faculty of Public Health (คณะสาธารณสุขศาสตร์)",
    }
    full_name = faculties.get(faculty_code, "Unknown Faculty")
    english_name = full_name.split(" (")[0]
    return english_name