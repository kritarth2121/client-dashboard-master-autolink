from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tags(models.Model):
    title = models.CharField(max_length=300)
    def __str__(self):
        return self.title