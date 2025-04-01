from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(UserDetail)
admin.site.register(UserOtp)
admin.site.register(Subscriber)