from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tags.models import Tags
approval=[
       
        ('Pending Start','Pending Start'),
        ('In Progress','In Progress'),
        ('Pending for Review','Pending for Review'),
        ('Client Feedback','Client Feedback'),
        ('Completed','Completed')

    ]
priority=[
    ('1','Low'),
    ('2','Medium'),
    ('3','High')
]

# Create your models here.
class Feed(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    description=models.TextField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    link=models.URLField(max_length=1280,unique=False,null=True  ,blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    websites=models.TextField(max_length=1000)
    link=models.URLField(max_length=1280,unique=False,null=True  ,verbose_name="Your Google Drive Link",blank=True)
    def __str__(self):
        return f'{self.user.username} Profile'

class Project(models.Model):
    name = models.CharField(max_length=100)
    client = models.ManyToManyField(User)
    description = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now,verbose_name='Start Date')
    deadline=models.DateTimeField(default=timezone.now,null=True  ,blank=True)
    priority=models.CharField(max_length=20, choices=priority,default='Medium')
    tags=models.ManyToManyField(Tags,verbose_name='Add Tags')
    def __str__(self):
        return self.name
    def percentage(self):
        c=0
        total=0
        for i in Work.objects.filter(project=self):
            if i.status.lower()=='completed':
                c+=1
            total+=1
        if total==0 or c==0:
            return f' 0 Percent'
        
        return f'{round((c/total)*100, 2)} Percent'


class Work(models.Model):
    project = models.ForeignKey(Project, related_name='project_tasks',on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    assigned_user = models.ManyToManyField(User,verbose_name='Staff members ')
    deadline=models.DateTimeField(default=timezone.now,null=True  ,blank=True)
    status=models.CharField(max_length=20, choices=approval,default='Pending Start')
    date_posted = models.DateTimeField(default=timezone.now,verbose_name='Start Date')
    description = models.TextField(max_length=1000,null=True,blank=True)
    subtask = models.TextField(max_length=1000,blank=True)
    link=models.URLField(max_length=1280,unique=False,null=True  ,blank=True)
    count=models.IntegerField(default=0)
    priority=models.CharField(max_length=20, choices=priority,default='Medium')
    tags=models.ManyToManyField(Tags,verbose_name='Add Tags')
    def __str__(self):
        return self.title
    '''   
    def save(self, request, obj, form, change):
        update_fields = []
        update_fields.append(requet.user)
        for key, value in form.cleaned_data.items():
            # True if something changed in model
            if value != form.initial[key]:
                update_fields.append(key)

        obj.save(update_fields=update_fields)
        return super(Work, self).save(*args, **kwargs)'''


class Note(models.Model):
    description=models.TextField(max_length=500,null=True,blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    work=models.ForeignKey(Work, on_delete=models.CASCADE, related_name='works')
    date_posted = models.DateTimeField(default=timezone.now)


from django.contrib import admin
from django.forms import CheckboxSelectMultiple

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }