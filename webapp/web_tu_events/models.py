from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(blank=True,null=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    student_id = models.IntegerField(unique=True,blank=True,null=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.name} ({self.student_id})'

class Announcement(models.Model):
    CATEGORIES_CHOICES = [
        ('entertainment', 'Entertainment'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('religions', 'Religions'),
        ('education', 'Education'),
        ('clubs','Clubs')
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(blank=True,null=True)
    date = models.DateTimeField(auto_now=True,auto_now_add=False)
    categories = models.CharField(max_length=100,choices=CATEGORIES_CHOICES)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False,help_text="กรอกวันที่เริ่มกิจกรรม")    
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False,help_text="กรอกวันที่สิ้นสุดกิจกรรม")
    place = models.CharField(max_length=200,default="TU")    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])
    
class Club(models.Model):
    ORIGIN_CHOICES = [
        ('tu','Thammasat University (มหาวิทยาลัยธรรมศาสตร์)'),
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
    image = models.ImageField(blank=False,null=True)    
    description = models.TextField()
    enable_to_join = models.BooleanField(default=True)
    origin = models.CharField(max_length=100, choices=ORIGIN_CHOICES)

    def get_absolute_url(self):
        return reverse('club_detail', kwargs={'club_id': self.id})

    def __str__(self):
        return self.title
    
class Lost(models.Model):
    items_name = models.CharField(max_length=100)
    image = models.ImageField(blank=True,null=True)
    description = models.TextField(default="description")
    lost_at = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    founded_status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('lost_detail', kwargs={'lost_id': self.id})

    def get_absolute_url_edit(self):
        return reverse('lost_edit', kwargs={'lost_id': self.id})

    
    def __str__(self):
        return self.items_name    

class Found(models.Model):
    items_name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField(default="description")
    found_at = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    founded_status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('found_detail', kwargs={'found_id': self.id})

    def get_absolute_url_edit(self):
        return reverse('found_edit', kwargs={'found_id': self.id})

    def __str__(self):
        return self.items_name  
    
class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interests")
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="interested_users")
    interested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')  # ป้องกันการกดสนใจกิจกรรมเดิมซ้ำ

    def __str__(self):
        return f"{self.user.username} สนใจกิจกรรม {self.announcement.title}"