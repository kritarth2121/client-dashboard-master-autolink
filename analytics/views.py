from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from django.conf import settings
from django.db.models.query import QuerySet
# If modifying these scopes, delete the file token.pickle.
from django.urls import reverse_lazy
SCOPES = ['https://www.googleapis.com/auth/calendar']
timezone = 'Asia/Kolkata'
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404,redirect
# Create your views here.
from tags.models import Tags
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
from rest_framework import generics

from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Feed,Profile,Work,Project,Note
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,WorkForm,ProjectForm
from django.contrib.auth import logout
from .serializers import TaskSerializer, UserSerializer
from rest_framework import viewsets



@login_required
def admi(request):
    '''for i in Work.objects.all()[:4]:
        if i.status=='Pending Start' and i.date_posted.date()<datetime.datetime.now().date() and i.count==0:
            subject = 'Regarding your Pending work at Al-Dashboard'
            from_email = i.assigned_user.email
            message = 'Please login with your username and password and turn its status to another one '
            
            ins1=Work.objects.get(id=i.id)
            ins1.count=1
            ins1.save()
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [from_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')'''
    if request.user.is_superuser or request.user.is_staff:
        
        return render(request, 'team.html')
    
    else:
        return redirect('analytics',name=request.user.username)
@login_required
def analytics(request,name):
    if request.user.is_authenticated:
        return render(request,'index.html',{'name':name})
    else:
        return redirect('login')

@login_required
def change(request,pk):
            work=Work.objects.all()
            postss= Note.objects.filter(work__id=pk).order_by('-date_posted')
            page = request.GET.get('page', 1)
            paginator = Paginator(postss, 7)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            return render(request, 'changes/change.html', {'posts': posts,'work': work })
class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows abilities to be viewed or edited.
    """
    serializer_class = TaskSerializer
    lookup_field='pk'
    

    def get_queryset(self):
        if self.request.query_params.get('name', None):
            print('name')
            
            return Work.objects.filter(assigned_user__username=self.request.query_params.get('name', None)).order_by('-status')
            
        elif self.request.query_params.get('pk', None):
            print('pk')
            return Work.objects.filter(pk=self.request.query_params.get('pk', None))
        else:
            
            return Work.objects.all().order_by('-status')
            


@login_required
def changefilter(request):
            work=Work.objects.all()
           
            return render(request, 'changes/change.html', {'work': work})


@login_required
def client(request):
    context = {
                'team':User.objects.filter(is_active=True,is_staff=False,is_superuser=False),
                'type':'Client',

            }
        
    return render(request, 'staff.html', context)


@login_required
def committouser(request,id):
    ins=Work.objects.get(id=id)
    ins1=Feed.objects.create(description=ins.description,date_posted=timezone.now(),link=ins.link,client=ins.client)
    ins1.save()
    messages.success(request, f'Updated to the mentioned client')
    return redirect('work',name=request.user.username)

def createfeed(request,name):
    today=request.GET['today']
    link=request.GET['link']
    ins=Feed.objects.create(description=today,date_posted=timezone.now(),client=User.objects.get(username=name),link=link)
    ins.save()
    messages.success(request, f'Your feed has been added')
    return redirect('feed',name=name)


def delete_user(request, username):
    
    try:
        u = User.objects.get(username=username)
        u.delete()
        messages.success(request, f'account has been deleted')    
    except User.DoesNotExist: 
        messages.failure(request, f'User does not exist.')
    except Exception as e: 
        messages.failure(request,  e.message)

    return redirect('home')



@login_required
def feed(request,name):
            post_unread=Feed.objects.filter(client__username=name,read=False).order_by('-date_posted')
            postss= Feed.objects.filter(client__username=name,read=True).order_by('-date_posted')
            page = request.GET.get('page', 1)
            paginator = Paginator(postss, 7)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            if not request.user.is_staff and not request.user.is_superuser:
                for i in post_unread:
                    ins=Feed.objects.get(pk=i.id)
                    ins.read=True
                    ins.save()
            return render(request, 'feed.html', {'post_unread':post_unread,'name':name,'posts': posts})






class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    
    model = Work
    form_class = WorkForm
    template_name ='update.html'
    
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('post-detail', kwargs = {'pk': self.kwargs.get('pk')})
    def form_valid(self, form):
            update_fields = []
            node_str=('<b>{field}:</b> changed ').format(
                    field=self.request.user,
                )

            #print(request.user.get_full_name)
            for key, value in form.cleaned_data.items():
            # True if something changed in model
                if value != form.initial[key]:
            # True if something changed in model
                    if isinstance(value, User):
                        ins1=User.objects.get(pk=form.initial[key])
                        if  ins1 != value:
                            
                            node_str +=('<b>{field}:</b> from <i>{orig_value}</i> '
                             '<b>&rarr;</b> {value} , ').format(
                    field=key,
                    orig_value=ins1,
                    value=value,
                )
                    

                    elif isinstance(value,Project):
                        ins2=Project.objects.get(pk=form.initial[key])
                        if ins2 != value:
                            update_fields.append(key)
                            node_str +=('<b>{field}:</b> from <i>{orig_value}</i> '
                             '<b>&rarr;</b> {value} , ').format(
                    field=key,
                    orig_value=ins2,
                    value=value,
                )
                    elif isinstance(value,QuerySet) or isinstance(form.initial[key],QuerySet):
                            if value!=form.initial[key]:
                                str2=''
                                str1=''
                                for i in value:
                                    try:
                                        str2+=i.username+' , '
                                    except:
                                        str2+=i.title+' , '
                                if form.initial[key]:
                                    for i in form.initial[key]:
                                        try:
                                            str1+=i.username+' , '
                                        except:
                                            str1+=i.title +' , '
                                if str1!=str2:
                                    node_str +=('<b>{field}:</b> from <i>{orig_value}</i> '
                                        '<b>&rarr;</b> {value} , ').format(
                                field=key,
                                orig_value=str1,
                                value=str2,
                            )


                            
                    else:                    
                        node_str +=('<b>{field}:</b> from <i>{orig_value}</i> '
                                '<b>&rarr;</b> {value} , ').format(
                        field=key,
                        orig_value=form.initial[key],
                        value=value,
                    )
            node_str +=('  <b>AT DATE AND TIME {value} </b>,').format(
                        
                        value=timezone.now(),
                    )
            print(node_str)
            ins=Note.objects.create(description=node_str,user=self.request.user,work=Work.objects.get(pk=self.kwargs.get('pk')))
            ins.save()
            '''
            obj=Work.objects.get(pk=self.kwargs.get('pk'))
            obj.save(update_fields=update_fields)
            d1 = form.cleaned_data
            d2 =form.initial
            diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
            print(dict(diffs))'''
            return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Work
    template_name ='post_confirm_delete.html'
    def test_func(self):
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('work', kwargs = {'name': self.request.user.username})

   


class PostDetailView(ListView):
    model = Work    
    template_name = 'detail.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    def get_queryset(self):
        return Work.objects.filter(pk=self.kwargs.get('pk'))
@login_required
def profile(request):
    return render(request, 'profile.html')


    return redirect('feed',name=name)


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
            '''
            update_fields = []
            
            for key, value in p_form.cleaned_data.items():
            # True if something changed in model
                if value != p_form.initial[key]:
                    update_fields.append(key)
            obj=Profile.objects.get(user__username=name)
            obj.save(update_fields=update_fields)
            '''
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
def profileup(request,name):
    context={
        'persons':User.objects.filter(username=name),
    }
    return render(request, 'profileup.html', context)

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
def staff(request):
    context = {
                'team':User.objects.filter(is_staff=True,is_superuser=False),
                'type':'Staff',

            }
        
    return render(request, 'staff.html', context)

@login_required
def workclient(request,name):
    ins=Project.objects.filter(client__username=name)
    return render(request, 'project/projectlist.html',{'name':name,'posts':ins} )
@login_required
def work(request,name):
    return render(request, 'kanban2.html',{'name':name} )


@login_required
def creatework(request,name):
    if request.method == 'POST':

        b=WorkForm(request.POST)
        if b.is_valid():
            b.save()
            update_fields = []
            node_str=('<b>{field}:</b> created ').format(
                    field=request.user,
                )

            #print(request.user.get_full_name)
            for key, value in b.cleaned_data.items():
            # True if something changed in model
                
            # True if something changed in model
                    if isinstance(value, User):
                            
                            node_str +=('<b>{field}:</b> with '
                             '<b>&rarr;</b> {value} , ').format(
                    field=key,
                    value=value,
                )
                    elif isinstance(value,Project):
                            update_fields.append(key)
                            node_str +=('<b>{field}:</b> '
                             '<b>&rarr;</b> {value} , ').format(
                    field=key,
                    value=value,
                )
                    elif isinstance(value,QuerySet):
                        
                            str2=''
                            for i in value:
                                try:
                                    str2+=i.username+' , '
                                except:
                                    str2+=i.title+' , '
                            
                            node_str +=('<b>{field}:</b> '
                                '<b>&rarr;</b> {value} , ').format(
                        field=key,
                        value=str2,
                    )


                            
                    else:                    
                        node_str +=('<b>{field}:</b> '
                                '<b>&rarr;</b> {value} , ').format(
                        field=key,
                        value=value,
                    )
            node_str +=('  <b>AT DATE AND TIME {value} </b>,').format(                        
                        value=datetime.datetime.now(),
                    )
            print(node_str)
            ins= Work.objects.all().order_by('-date_posted').first()
            inst=Note.objects.create(description=node_str,user=request.user,work=ins)
            inst.save()
            
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
            timezone = 'Asia/Kolkata'
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
            #pending= Work.objects.filter(assigned_user__username=name,status='Pending Start').order_by('-date_posted')
            #progress=Work.objects.filter(assigned_user__username=name,status='In Progress').order_by('-date_posted')
            #pendingreview=Work.objects.filter(assigned_user__username=name,status='Pending for Review').order_by('-date_posted')
            #feedback=Work.objects.filter(assigned_user__username=name,status='Client Feedback').order_by('-date_posted')
            #completed=Work.objects.filter(assigned_user__username=name,status='Completed').order_by('-date_posted')            
            #return render(request, 'kanban2.html', {'pending': pending,'progress':progress,'pendingreview':pendingreview,'feedback':feedback,'completed':completed,'name':name,'user1':User.objects.get(username=name)})
            return redirect('work',name=name)
            
        else:
            b= WorkForm()
            #pending= Work.objects.filter(assigned_user__username=name,status='Pending Start').order_by('-date_posted')
            #progress=Work.objects.filter(assigned_user__username=name,status='In Progress').order_by('-date_posted')
            #pendingreview=Work.objects.filter(assigned_user__username=name,status='Pending for Review').order_by('-date_posted')
            #feedback=Work.objects.filter(assigned_user__username=name,status='Client Feedback').order_by('-date_posted')
            #completed=Work.objects.filter(assigned_user__username=name,status='Completed').order_by('-date_posted')
            
            #return render(request, 'kanban2.html', {'pending': pending,'progress':progress,'pendingreview':pendingreview,'feedback':feedback,'completed':completed,'name':name,'user1':User.objects.get(username=name)})
            return render(request,'creatework.html',{'form':b})
        
    else:
        b= WorkForm()
        #pending= Work.objects.filter(assigned_user__username=name,status='Pending Start').order_by('-date_posted')
        #progress=Work.objects.filter(assigned_user__username=name,status='In Progress').order_by('-date_posted')
        #pendingreview=Work.objects.filter(assigned_user__username=name,status='Pending for Review').order_by('-date_posted')
        #feedback=Work.objects.filter(assigned_user__username=name,status='Client Feedback').order_by('-date_posted')
        #completed=Work.objects.filter(assigned_user__username=name,status='Completed').order_by('-date_posted')
        
        #return render(request, 'kanban2.html', {'pending': pending,'progress':progress,'pendingreview':pendingreview,'feedback':feedback,'completed':completed,'name':name,'user1':User.objects.get(username=name)})
        return render(request,'creatework.html',{'form':b})

@login_required
def worklist(request):
    posts=Work.objects.all()
    return render(request, 'work.html',{'posts':posts} )










