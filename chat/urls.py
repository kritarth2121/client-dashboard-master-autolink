from django.urls import path, include
from django.conf import settings
from . import views
app_name='chat'
urlpatterns= [

    path('msg',views.msg,name='msg'),
    path('<str:room_name>/', views.room, name='room'),
]