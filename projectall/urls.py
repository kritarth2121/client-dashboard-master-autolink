from django.urls import path, include
from django.conf import settings
from . import views
app_name='projectall'
urlpatterns = [
    path('new', views.createproject, name='createproject'),
    path('list',views.ProjectListView.as_view(),name='projectlist'),
    path('<int:pk>/detail/',views.ProjectDetailView.as_view(),name="projectdetail"),
    path('<int:pk>/detail/update',views.ProjectUpdateView.as_view(),name="projectupdate"),
    path('<int:pk>/detail/delete',views.ProjectDeleteView.as_view(),name="projectdelete"),
    path('<int:pk>/work',views.WorkProjectListView.as_view(),name='workproject'),


]