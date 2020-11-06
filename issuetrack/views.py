from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import IssueTrack
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import IssueTrackForm

# Create your views here.
@login_required
def issuecreate(request):
    if request.method == 'POST':

        b=IssueTrackForm(request.user,request.POST)
        if b.is_valid():
            model_instance = b.save(commit=False)
            model_instance.user=request.user
            model_instance.save()
            return redirect('issuetrack:issuelist',name=request.user.username)
    else:
        b= IssueTrackForm(request.user)
            
        return render(request,'issue/issuecreation.html',{'form':b})

@login_required
def issuetrack(request,name):
            users=User.objects.filter(is_active=True,is_staff=False,is_superuser=False)
            postss= IssueTrack.objects.filter(user=User.objects.get(username=name)).order_by('-date_posted')
            name=User.objects.get(username=name).get_full_name()
            page = request.GET.get('page', 1)
            paginator = Paginator(postss, 7)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            return render(request, 'issue/issuetrack.html', {'posts': posts,'users':users,'name':name})

@login_required
def issuefilter(request):
            users=User.objects.filter(is_active=True,is_staff=False,is_superuser=False)
           
            return render(request, 'issue/issuetrack.html', {'users':users})
@login_required
def issuetrackcomment(request,id):
    ins=IssueTrack.objects.get(id=id)
    comment=request.GET['comment']
    ins.comment=comment
    ins.status='2'
    name=ins.user.username
    ins.save()
    messages.success(request, f'Your issue reply has been added')

    return redirect('issuetrack:issuelist',name=name)

@login_required
def issuetrackclose(request,id):
    ins=IssueTrack.objects.get(id=id)
    
    ins.status='3'
    name=ins.user.username
    ins.save()
    messages.success(request, f'Your issue has been closed')

    return redirect('issuetrack:issuelist',name=name)