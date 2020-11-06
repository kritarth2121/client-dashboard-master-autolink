from django.contrib import admin

# Register your models here.
from .models import Comment,CommentTask

admin.site.register(Comment)

admin.site.register(CommentTask)
