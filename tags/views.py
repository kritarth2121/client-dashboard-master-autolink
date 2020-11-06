from django.db.models.functions import datetime
import datetime
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from analytics.models import Feed,Profile,Work,Project,Note
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404,redirect

# Create your views here.
@login_required
def createtag(request):
    comment=request.GET['comment']
    ins1=Tags.objects.create(title=comment)
    ins1.save()
    messages.success(request, f'Your tag has been added')
    return redirect('tags:filtersee')

def see(request):
    posts=Tags.objects.all()
    return render(request,'tags/taglist.html',{'posts':posts})

def filtername(request,name):
    project=Project.objects.filter(tags__title=name)
    work=Work.objects.filter(tags__title=name)
    posts=Tags.objects.all()
    return render(request,'tags/projectworklist.html',{'project':project,'work':work,'posts':posts,'name':name})

