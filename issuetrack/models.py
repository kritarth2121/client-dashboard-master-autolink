from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from analytics.models import Feed,Project,Work
# Create your models here.

status=[
    ('1','Waiting for staff response'),
    ('2','Waiting for client response'),
    ('3','Closed')
    ]

class IssueTrack(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    description=models.TextField(max_length=500)
    title = models.CharField(max_length=300,null=True,blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    comment=models.TextField(max_length=500,null=True,blank=True)
    project=models.ForeignKey(Project,related_name='projects_issue',on_delete=models.CASCADE,null=True)

    work=models.ForeignKey(Work, related_name='works_issue',on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=200, choices=status,default='1')
    image = models.ImageField(default='default.jpg',null=True, upload_to='profile_pics',verbose_name='Add an image for further details(* Not necessary)')

