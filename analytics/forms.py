from django import forms
from .models import Profile,Work,Project
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets                                       
from django.utils import timezone
from django.db.models.functions import datetime
import datetime
from tags.models import Tags
from django.forms import CheckboxSelectMultiple

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name' ,'last_name','password1', 'password2','user_permissions','is_active','is_staff','is_superuser','date_joined']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['username', 'email','first_name' ,'last_name','user_permissions','is_active','is_staff','is_superuser']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','websites','link']
        widgets = { 'websites': forms.Textarea(attrs={'rows':15, 'cols':20}),}
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
def present_or_future_date(value):
        if value < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return value

class WorkForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WorkForm, self).__init__(*args, **kwargs)
        self.fields['assigned_user'].queryset=User.objects.filter(is_superuser=False,is_staff=True)
        self.fields['assigned_user'].widget = CheckboxSelectMultiple()
        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tags.objects.all()
    def clean_date(self):
        date = self.cleaned_data['deadline']
        if date < datetime.datetime.now():
            raise forms.ValidationError("The date cannot be in the past!")
        return date
    class Meta:
        model = Work
        fields = ['project','title','assigned_user','deadline','status','date_posted','description','subtask','link','priority','tags']
        widgets = {'description': forms.Textarea(attrs={'rows':10, 'cols':20}),
        'subtask': forms.Textarea(attrs={'rows':10, 'cols':20}),
            'deadline': forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',

        })}



class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['client'].queryset=User.objects.filter(is_superuser=False,is_staff=False)
        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tags.objects.all()
    class Meta:
        model = Project
        fields='__all__'
        



