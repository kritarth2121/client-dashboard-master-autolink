from django import forms
from django.contrib.admin import widgets                                       
from django.contrib.auth.models import User
from .models import IssueTrack
from analytics.models import Feed,Project,Work



class IssueTrackForm(forms.ModelForm):
    def __init__(self,user, *args, **kwargs):
        super(IssueTrackForm, self).__init__(*args, **kwargs)
        self.fields['work'].queryset=Work.objects.filter(client=user)
        self.fields['project'].queryset=Project.objects.filter(client=user)

    class Meta:
        model=IssueTrack
        fields=['project','work','title','description','image']