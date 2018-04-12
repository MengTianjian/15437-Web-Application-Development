"""webapps URL Configuration

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
from django.conf.urls import url

from django.contrib import admin

from django.contrib.auth.views import login, logout_then_login

import grumblr.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', grumblr.views.home, name='home'),
    url(r'^login$', grumblr.views.my_login, name='login'),#, {'template_name': 'Login.html'}),
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^register$', grumblr.views.register, name='register'),
    url(r'^post$', grumblr.views.post, name='post'),
    url(r'^profile-photo/(?P<id>\d+)$', grumblr.views.get_profilephoto, name='profile-photo'),
    url(r'^post-photo/(?P<id>\d+)$', grumblr.views.get_postphoto, name='post-photo'),
    url(r'^follow$', grumblr.views.follow, name='follow'),
    url(r'^unfollow$', grumblr.views.unfollow, name='unfollow'),
    url(r'^followerstream$', grumblr.views.followerstream, name='followerstream'),
    url(r'^profile/(?P<id>\d+)$', grumblr.views.profile, name='profile'),
    url(r'^edit_profile$', grumblr.views.edit_profile, name='edit_profile'),
    url(r'^confirm/(?P<id>\d+)/(?P<token>\w+-\w+)$', grumblr.views.confirm_registration, name='confirm'),
    url(r'^changepassword$', grumblr.views.change_password, name='change_password'),
    url(r'^updatepassword$', grumblr.views.update_password, name='update_password'),
    url(r'^confirmpassword/(?P<id>\d+)/(?P<token>\w+-\w+)$', grumblr.views.confirm_password, name='confirm_password')
]
