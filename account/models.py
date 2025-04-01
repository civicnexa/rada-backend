from django.db import models
from django.contrib.auth.models import User
from rada.modules.choices import ROLE_CHOICES
from django.utils import timezone
from django.utils import timezone
import datetime
import random

# Create your models here.
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default="readOnly")
    phoneNumber = models.CharField(max_length=100, blank=True, null=True)

    image = models.ImageField(upload_to="profile", default="default.jpg")
    createdBy = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_by",
    )
    createdOn = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    subscribed_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        ordering = ["-subscribed_at"]
        

class UserOtp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp")
    otp = models.CharField(max_length=8)
    createdOn = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    verifiedOn = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    verification_type = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return str(self.otp)
    
    def save(self, *args, **kwargs) -> None:
        otp = random.choices(population=[str(i) for i in range(0, 10)], k=6)
        otp = ''.join(otp)
        self.otp = otp
        return super().save(*args, **kwargs)
    
    @property
    def not_expired(self) -> bool:
        current_time = timezone.now()
        return (current_time - (self.createdOn)) <= datetime.timedelta(minutes = 10)
    
    
    @property
    def not_verificationInvalid(self) -> bool:
        current_time = timezone.now()
        return (current_time - (self.verifiedOn)) <= datetime.timedelta(minutes = 5)
    