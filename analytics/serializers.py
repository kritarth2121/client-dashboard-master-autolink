from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Work

from . import views 

class TaskSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="post-detail",lookup_field='pk')
    class Meta:
        model = Work
        fields ='__all__'
    def vaild_status(status):
        valid_list = ['pending', 'progress', 'pendingreview','feedback','completed','Pending Start','In Progress','Pending for Review','Client Feedback','Completed']
        if status not in valid_list:
            print('invalid')
            raise serializers.ValidationError('This field must be backlog, '
                                              'active or complete.')
    description = serializers.CharField()
    status = serializers.CharField(validators=[vaild_status])




class UserSerializer(serializers.ModelSerializer):

    task = serializers.PrimaryKeyRelatedField(many=True,queryset=Work.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'task')

