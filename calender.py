'''
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ['https://www.googleapis.com/auth/calendar']

import pickle
from datetime import datetime, timedelta
credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)
result = service.calendarList().list().execute()
print(result['items'][0])


def create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()'''

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
from datetime import datetime, timedelta
start_time = datetime(2019, 5, 12, 19, 30, 0)
end_time = start_time + timedelta(hours=4)
timezone = 'Asia/Kolkata'
print(start_time)
def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    event = {
    'summary': 'IPL Final 2019',
    'location': 'Hyderabad',
    'description': 'MI vs TBD',
    'start': {
        'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': timezone,
    },
    'end': {
        'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': timezone,
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }
    print(start_time.strftime("%Y-%m-%dT%H:%M:%S"))
    return service.events().insert(calendarId='primary', body=event).execute()


if __name__ == '__main__':
    main()
#2020-07-20 12:25:52+00:00
#2020-07-20T12:25:52
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from django.conf import settings

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
timezone = 'Asia/Kolkata'


from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404,redirect
# Create your views here.
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView

)
def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from django.db.models.functions import datetime
import datetime

from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Feed,Profile,Work,IssueTrack
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,WorkForm,ProjectForm
from django.contrib.auth import logout

class PostDetailView(ListView):
    model = Work    
    template_name = 'detail.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    def get_queryset(self):
        user = get_object_or_404(Work, pk=self.kwargs.get('pk'))
        print(user.id)
        return Work.objects.filter(id=user.id)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Work
    fields = '__all__'
    template_name ='update.html'
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Work
    success_url = '/'
    template_name ='post_confirm_delete.html'
    def test_func(self):
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

@login_required
def committouser(request,id):
    ins=Work.objects.get(id=id)
    ins1=Feed.objects.create(description=ins.description,date_posted=timezone.now(),client=ins.client)
    ins1.save()
    messages.success(request, f'Updated to the mentioned client')
    return redirect('work',name=ins.assigned_user.username)







@login_required
def analytics(request,name):
    if request.user.is_authenticated:
        return render(request,'index.html')
    else:
        return redirect('login')
@login_required
def feed(request,name):
    if request.user.is_authenticated:
        if request.method == 'POST':
            today=request.POST['today']
            ins=Feed.objects.create(description=today,date_posted=timezone.now(),client=User.objects.get(username=name))
            ins.save()
            postss= Feed.objects.filter(client__username=name).order_by('-date_posted')
            page = request.GET.get('page', 1)
            paginator = Paginator(postss, 7)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            messages.success(request, f'Feed is updated')

            return render(request, 'feed.html', {'posts': posts})
        else:
            postss= Feed.objects.filter(client__username=name).order_by('-date_posted')
            page = request.GET.get('page', 1)
            paginator = Paginator(postss, 7)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            return render(request, 'feed.html', {'posts': posts})
    else:

        return render(request, 'login')

@login_required
def profile(request):
    return render(request, 'profile.html')
@login_required
def comment(request,id):
    ins=Feed.objects.get(id=id)
    comment=request.GET['comment']
    ins.comment=comment
    name=ins.client.username
    ins.save()
    print(id,comment)
    messages.success(request, f'Your comment has been added')

    return redirect('feed',name=name)

@login_required
def issuetrackcomment(request,id):
    ins=IssueTrack.objects.get(id=id)
    comment=request.GET['comment']
    ins.comment=comment
    name=ins.client.username
    ins.save()
    print(id,comment)
    messages.success(request, f'Your comment has been added')

    return redirect('issuetrack',name=name)

@login_required
def admi(request):
    for i in Work.objects.all():
        if i.status=='Pending Start' and i.date_posted.date()<datetime.datetime.now() and i.count==0:
            subject = 'Regarding your Pending work at Al-Dashboard'
            from_email = i.assigned_user.email
            message = 'Please login with your username and password and turn its status to another one '
            i.count=1
            i.save()
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [from_email])
                c+=1
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
    if request.user.is_superuser or request.user.is_staff:
        
        return render(request, 'team.html')
    
    else:
        return redirect('analytics',name=request.user.username)

@login_required
def client(request):
    context = {
                'team':User.objects.filter(is_active=True,is_staff=False,is_superuser=False),
                'type':'Client',

            }
        
    return render(request, 'staff.html', context)

@login_required
def staff(request):
    context = {
                'team':User.objects.filter(is_staff=True,is_superuser=False),
                'type':'Staff',

            }
        
    return render(request, 'staff.html', context)

@login_required
def profileup(request,name):
    context={
        'persons':User.objects.filter(username=name),
    }
    return render(request, 'profileup.html', context)



@login_required
def profileupdate(request,name):
    user=User.objects.get(username=name)
    print(type(user))
    print(type(request.user))
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        #j_form= ProfileUpdateForm(request.POST,instance=request.user.profile)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profileup',name=name)

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)
        #j_form= ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profileupdate.html',context)

@login_required
def work(request,name):
    
            postss= Work.objects.filter(assigned_user__username=name).order_by('-date_posted')
            page = request.GET.get('page', 1)
            paginator = Paginator(postss, 7)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            return render(request, 'work.html', {'posts': posts,'name':name,'user1':User.objects.get(username=name)})

from datetime import datetime, timedelta

@login_required
def creatework(request,name):
    if request.method == 'POST':

        b=WorkForm(request.POST)
        if b.is_valid():
            b.save()

            ins= Work.objects.all().order_by('-date_posted').first()
            creds = None
    
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            start_time = datetime(2019, 5, 12, 19, 30, 0)
            end_time = start_time + timedelta(hours=4)
            timezone = 'Asia/Kolkata'
            print(ins.date_posted.strftime("%Y-%m-%dT%H:%M:%S"),start_time.strftime("%Y-%m-%dT%H:%M:%S"))
            event = {
                'summary': ins.title,
                'location': 'India',
                'description': ins.description,
                'start': {
                    'dateTime': ins.date_posted.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': ins.deadline.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
                }
            #json_event = json.dumps(event)
            #event= json.dumps(set(event), default=serialize_sets)
            service.events().insert(calendarId='primary', body=event).execute()
            return redirect('work',name=name)
        else:
            b= WorkForm()
            
            return render(request,'creatework.html',{'form':b})
        
    else:
        b= WorkForm()
        
        return render(request,'creatework.html',{'form':b})

def issuetrack(request,name):
        if request.method == 'POST':
            today=request.POST['today']
            ins=IssueTrack.objects.create(description=today,date_posted=timezone.now(),user=User.objects.get(username=name))
            ins.save()
            postss= IssueTrack.objects.filter(user=request.user).order_by('-date_posted')
            page = request.GET.get('page', 1)
            paginator = Paginator(postss, 7)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            messages.success(request, f'Issue is added,You will soon get a reply from Autolink Team')

            return render(request, 'issuetrack.html', {'posts': posts})
        else:
            postss= IssueTrack.objects.filter(user=User.objects.get(username=name)).order_by('-date_posted')
            page = request.GET.get('page', 1)
            paginator = Paginator(postss, 7)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            return render(request, 'issuetrack.html', {'posts': posts})
    

@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('profileupdate',name=username)
    else:
        form = UserRegisterForm()
    print(11)
    return render(request, 'register.html', {'form': form})



@login_required
def updategoal(request,name):
    ins=Profile.objects.get(user__username=name)
    comment=request.GET['comment']
    ins.goal=comment
    name=ins.user.username
    ins.save()
    print(id,comment)
    messages.success(request, f'Goal Updated')

    return redirect('work',name=name)
