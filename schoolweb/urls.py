"""schoolweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from account import urls as BaseAccountUrls
from friend import urls as FriendUrls
from unique import urls as UniqueUrls
from learner import urls as LearnerUrls
from teacher import urls as TeacherUrls
from blog import urls as BlogUrls



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(BaseAccountUrls)),
    path('', include(UniqueUrls)),
    path('', include(FriendUrls)),
    path('', include(LearnerUrls)),
    path('', include(TeacherUrls)),
    path('', include(BlogUrls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


