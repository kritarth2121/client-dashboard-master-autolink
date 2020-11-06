from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
app_name='comment'
urlpatterns = [

    path('comment/<int:id>',views.comment,name='commen'),
    path('comment/task/<int:id>',views.commentTask,name='commentTask'),

    path('reply/<int:id1>/<int:id2>',views.reply,name='reply'),
]