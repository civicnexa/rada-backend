from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class BaseModel(models.Model):
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="createdBy")
    updatedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updatedBy")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Service(models.Model):
    title = models.CharField(max_length=500)
    body = models.TextField()
    image = models.ImageField(upload_to='service', default='default.jpg')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
class SubServices(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="subservice")
    title = models.CharField(max_length=500)
    body = models.TextField()
    image = models.ImageField(upload_to='sub_service', default='default.jpg')
    

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    image = models.ImageField(null=True, default='default.jpg')
    body = models.TextField()
    rating = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} - {self.organization}"


class Contact(models.Model):
    fullname = models.CharField(max_length=300)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    isClosed = models.BooleanField(default=False)

class Project(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    client = models.CharField(max_length=500)
    link = models.URLField(max_length=200)
    year_started = models.CharField(max_length=5)
    stack = models.TextField()
    image = models.ImageField(upload_to="project", default='default.jpg')
     
class Team(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="team")
    role = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    educational_qualification = models.CharField(max_length=300)
    bio = models.TextField()
    linkedin = models.URLField(null=True)
    twitter = models.URLField(null=True)
    github = models.URLField(null=True)

class Clients(models.Model):
    client_name = models.CharField(max_length=500)
    client_image = models.ImageField(upload_to="client")
