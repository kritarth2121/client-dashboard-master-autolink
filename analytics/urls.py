from django.urls import path,include
from . import views
from django.conf.urls import url, include

from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('',views.admi,name='home'),
    path('analytics/<str:name>',views.analytics,name="analytics"),
    path('change/<int:pk>',views.change,name='change'),
    path('changefilter',views.changefilter,name='changefilter'),
    path('client',views.client,name='client'),
    path('committouser/<int:id>',views.committouser,name='committouser'),
    path('createfeed/<str:name>',views.createfeed,name='createfeed'),
    path('delete/<str:username>', views.delete_user, name='delete-user'),
    path('feed/<str:name>',views.feed,name="feed"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('profile',views.profile,name="profile"),
    path('profile/<str:name>',views.profileup,name='profileup'),

    path('profileupdate/<str:name>',views.profileupdate,name="profileupdate"),
    path('register', views.register, name='register'),
    path('staff',views.staff,name='staff'),
    path('task/client/<str:name>',views.workclient,name='workclient'),
    path('work/<str:name>',views.work,name='work'),
    path('work/<str:name>/new',views.creatework,name='creatework'),
    path('worklist',views.worklist,name='worklist'),

    ]