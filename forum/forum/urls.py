"""forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^topics/$', views.topics, name='home'),
    url(r'^topics/new$', views.new_topic, name='new_topic'),
    url(r'^topic/(?P<topic_id>[0-9]+)/$', views.topic, name='topic'),
    url(r'^topic/(?P<topic_id>[0-9]+)/new/', views.new_thread, name='new_thread'),
    url(r'^posts/(?P<post_id>[0-9]+)/$', views.post, name='post'),
    url(r'^posts/new/$', views.create_post, name='new_post'),
    url(r'^user/(?P<user_id>[0-9]+)/', views.user, name='user'),
    url(r'^user/edit/', views.user_edit, name='user_edit'),
    url(r'^vote/(?P<post_id>[0-9]+)/', views.vote, name='vote'),
    url(r'^$', RedirectView.as_view(url='topics/', permanent=False)),


    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    # url(r'^login/', auth_views.LoginView.as_view(), name='login'),
    # url('^change-password/$', auth_views.PasswordChangeView.as_view(), name='password_reset'),
]
