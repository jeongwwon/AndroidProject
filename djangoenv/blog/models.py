from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from datetime import date

class GlobalPostCount(models.Model):
    count = models.IntegerField(default=0)

    def increment_count(self,count):
        self.count += count
        self.save()

    def decrement_count(self, count):
        if self.count >= count:
            self.count -= count
            self.save()

    @classmethod
    def get_instance(cls):
        # 클래스 메서드를 통해 항상 하나의 객체를 반환
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
    default=timezone.now)
    published_date = models.DateTimeField(
    blank=True, null=True)
    image = models.ImageField(upload_to='intruder_image/%Y/%m/%d/',default='intruder_image/default_error.png')
    count = models.IntegerField(default=0)
    GlobalPostCount.get_instance().increment_count(count)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def today_count(self):
        today = date.today()
        return GlobalPostCount.objects.filter(created_date__date=today).first().count if self.global_count else 0
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        # 포스트가 삭제될 때 글로벌 카운트에서 해당 카운트 감소
        if self.global_count:
            self.global_count.decrement_count(self.count)

        super().delete(*args, **kwargs)

class ResponseModel(models.Model):
    status = models.CharField(max_length=255, default="")
    message = models.CharField(max_length=255, default="")
    issuccess = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.status} - {self.message} - {self.issuccess}"
    


