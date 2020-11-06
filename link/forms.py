from django import forms
from .models import Folder


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields=['title','link']