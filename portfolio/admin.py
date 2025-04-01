from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Service)
admin.site.register(SubServices)
admin.site.register(Testimonial)
admin.site.register(Contact)
admin.site.register(Project)
admin.site.register(Team)
admin.site.register(Clients)