from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Folder(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    link=models.URLField(max_length=1280,unique=False,null=True  ,blank=True)
    date_posted = models.DateTimeField(default=timezone.now,verbose_name='Date')
