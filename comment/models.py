from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from analytics.models import Profile,Work,Project,Feed

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed , null=True,related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='replies')
    comment = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

class CommentTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Work , null=True,related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='replies')
    comment = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)