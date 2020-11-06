from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

from django.contrib import admin
from django.urls import path,include
from . import views
app_name='tags'
urlpatterns = [
    path('new', views.createtag, name='createtag'),
    path('filter',views.see,name='filtersee'),
    path('filter/<str:name>',views.filtername,name='filtername'),
]