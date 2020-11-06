from django.shortcuts import render
from analytics.models import Profile,Work,Project,Feed
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Comment,CommentTask
from django.db.models.functions import datetime
import datetime
from rest_framework import generics

from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def comment(request,id):
    ins=Feed.objects.get(id=id)
    comment=request.GET['comment']
    ins1=Comment.objects.create(user=request.user,feed=ins,comment=comment)
    ins1.save()
    messages.success(request, f'Your comment has been added')
    return redirect('feed',name=ins.client.username)
@login_required
def commentTask(request,id):
    ins=Work.objects.get(id=id)
    comment=request.GET['comment']
    ins1=CommentTask.objects.create(user=request.user,task=ins,comment=comment)
    ins1.save()
    messages.success(request, f'Your Sub-Task has been added')
    return redirect('post-detail',pk=id)
@login_required
def reply(request,id1,id2):
    ins1=Feed.objects.get(id=id1)
    
    comment=request.GET['comment']
    ins2=Comment.objects.get(id=id2)
    ins3=Comment.objects.create(user=request.user,feed=ins1,parent=ins2,comment=comment)
    ins3.save()
    messages.success(request, f'Your comment has been added')
    return redirect('feed',name=ins1.client.username)

