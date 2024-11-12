from django.db import models

# Create your models here.

class Student(models.Model):
    image = models.ImageField()
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    student_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=30)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(user__is_staff=False, user__is_superuser=False)

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    date = models.DateField()
    categories = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)    
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    place = models.CharField(max_length=200,default="TU")    

    def __str__(self):
        return self.title
    
class Club(models.Model):
    ORIGIN_CHOICES = [
        ('law', 'Faculty of Law (คณะนิติศาสตร์)'),
        ('business', 'Thammasat Business School (คณะพาณิชยศาสตร์และการบัญชี)'),
        ('political_science', 'Faculty of Political Science (คณะรัฐศาสตร์)'),
        ('economics', 'Faculty of Economics (คณะเศรษฐศาสตร์)'),
        ('social_administration', 'Faculty of Social Administration (คณะสังคมสงเคราะห์ศาสตร์)'),
        ('sociology_anthropology', 'Faculty of Sociology and Anthropology (คณะสังคมวิทยาและมานุษยวิทยา)'),
        ('liberal_arts', 'Faculty of Liberal Arts (คณะศิลปศาสตร์)'),
        ('journalism_mass_comm', 'Faculty of Journalism and Mass Communication (คณะวารสารศาสตร์และสื่อสารมวลชน)'),
        ('science_technology', 'Faculty of Science and Technology (คณะวิทยาศาสตร์และเทคโนโลยี)'),
        ('engineering', 'Faculty of Engineering (คณะวิศวกรรมศาสตร์)'),
        ('architecture_planning', 'Faculty of Architecture and Planning (คณะสถาปัตยกรรมศาสตร์และการผังเมือง)'),
        ('medicine', 'Faculty of Medicine (คณะแพทยศาสตร์)'),
        ('allied_health', 'Faculty of Allied Health Sciences (คณะสหเวชศาสตร์)'),
        ('dentistry', 'Faculty of Dentistry (คณะทันตแพทยศาสตร์)'),
        ('nursing', 'Faculty of Nursing (คณะพยาบาลศาสตร์)'),
        ('public_health', 'Faculty of Public Health (คณะสาธารณสุขศาสตร์)'),
    ]
        
    title = models.CharField(max_length=100)
    description = models.TextField()
    enable_to_join = models.BooleanField(default=True)
    origin = models.CharField(max_length=100, choices=ORIGIN_CHOICES)

    def __str__(self):
        return self.title
    
class Lost(models.Model):
    items_name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField(default="description")
    lost_at = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    founded_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.items_name    

class Found(models.Model):
    items_name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField(default="description")
    found_at = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    founded_status = models.BooleanField(default=False)

    def __str__(self):
        return self.items_name  