from django.urls import path, include
from django.conf import settings
from . import views
app_name='link'
urlpatterns = [
    path('<str:name>/new', views.createlink, name='createlink'),
    path('<str:name>/list',views.linkListView.as_view(),name='linklist'),
    path('<int:pk>/update',views.linkUpdateView.as_view(),name="linkupdate"),
    path('<int:pk>/delete',views.linkDeleteView.as_view(),name="linkdelete"),


]