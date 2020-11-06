from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Folder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from analytics.models import Project
from analytics.models import Work,Profile,Feed
from django.shortcuts import render, redirect
from analytics.forms import ProjectForm
from .forms import ProjectForm
from .models import Folder
# Create your views here.
def createlink(request,name):
    if request.method=='POST':
        b=ProjectForm(request.POST)
        if b.is_valid():
            event = b.save(commit=False)
            event.user = User.objects.get(username=name)
            event.save()
            
            return redirect('link:linklist',name=name)
    else:
        b= ProjectForm()
    context = {
        'form': b,
    }
    return render(request,'link/createlink.html',context)

class linkListView(ListView):
    model =Folder
    template_name = 'link/linklist.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super(linkListView, self).get_context_data(**kwargs)
        context.update({'name': self.kwargs.get('name')})
        return context
    def get_queryset(self):
        return Folder.objects.filter(user__username=self.kwargs.get('name')).order_by('-date_posted')


class linkUpdateView(LoginRequiredMixin, UpdateView):
    model = Folder
    fields = '__all__'
    template_name = 'update.html'
    def form_valid(self, form):
        form.instance.assigned_employee = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('link:linklist',name=name)
    #print(post.id)

     
class linkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Folder
    template_name='link/delete.html'
    def test_func(self):
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('link:linklist',name=name)
