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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from analytics.models import Project
from analytics.models import Work,Profile,Feed
from django.shortcuts import render, redirect
from analytics.forms import ProjectForm
# Create your views here.
def createproject(request):
    if request.method=='POST':

        b=ProjectForm(request.POST)

        if b.is_valid():
            b.save()
            return redirect('creatework',name=request.user.username)
    else:
        b= ProjectForm()
    context = {
        'form': b,
    }
    return render(request,'project/createproject.html',context)

class ProjectListView(ListView):
    model =Project
    template_name = 'project/projectlist.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class WorkProjectListView(ListView):
    model=Work
    template_name='project/workproject.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return Work.objects.filter(project=project).order_by('-date_posted')



class ProjectDetailView(ListView):
    model = Project   
    template_name = 'project/projectdetail.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    def get_queryset(self):
        user = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        print(user.id)
        return Project.objects.filter(id=user.id)




class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
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
            return reverse_lazy('projectall:projectdetail', kwargs = {'pk': self.kwargs.get('pk')})
    #print(post.id)

     
class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name='project/delete.html'
    def test_func(self):
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('projectall:projectlist')
