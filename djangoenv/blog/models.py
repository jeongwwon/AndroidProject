from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db import models
from django.dispatch import receiver

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
    default=timezone.now)
    published_date = models.DateTimeField(
    blank=True, null=True)
    image = models.ImageField(upload_to='intruder_image/%Y/%m/%d/',default='intruder_image/default_error.png')
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title
    
class ResponseModel(models.Model):
    status = models.CharField(max_length=255, default="")
    message = models.CharField(max_length=255, default="")
    issuccess = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.status} - {self.message} - {self.issuccess}"
    


