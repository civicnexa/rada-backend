from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=500)
    body = models.TextField()
    image = models.ImageField(upload_to='blog', default='default.jpg')
    from_blog = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title