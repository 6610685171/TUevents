from django.db import models

# Create your models here.

class Student(models.Model):
    image = models.ImageField()
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    student_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=30)

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    date = models.DateField()
    categories = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)    
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    place = models.CharField(max_length=200)    

    def __str__(self):
        return self.title
    
class Club(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    enable_to_join = models.BooleanField(default=True)
    origin = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class Lost(models.Model):
    items_name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField()
    lost_at = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    founded_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.items_name    

class Found(models.Model):
    items_name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField()
    found_at = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    founded_status = models.BooleanField(default=False)

    def __str__(self):
        return self.items_name  