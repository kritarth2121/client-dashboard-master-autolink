"""autolink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

from django.contrib import admin
from django.urls import path,include
from analytics import views 
from rest_framework import routers
router = routers.DefaultRouter()
router.register('task', views.TaskViewSet, 'task-list')


urlpatterns = [
    path('',include('analytics.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('issuetrack/',include('issuetrack.urls')),
    path('link/',include('link.urls')),
    path('comment/',include('comment.urls')),
    path('project/',include('projectall.urls')),
    path('tags/',include('tags.urls')),
    path('worklist',views.worklist,name='worklist'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)