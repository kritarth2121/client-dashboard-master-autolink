from django.urls import path, include
from django.conf import settings
from . import views
app_name='issuetrack'
urlpatterns = [
    path('new', views.issuecreate, name='createissue'),
    path('<str:name>/list',views.issuetrack,name='issuelist'),
    path('<int:id>/comment',views.issuetrackcomment,name="issuecomment"),
    path('filter',views.issuefilter,name='issuefilter'),

    path('<int:id>/close',views.issuetrackclose,name="issueclose"),

]