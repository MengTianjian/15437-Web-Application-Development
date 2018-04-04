# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profilephoto = models.ImageField(default="/static/images/images.png")
    firstname = models.TextField()
    lastname = models.TextField()
    email = models.EmailField()
    url = models.URLField(default="#")
    def __unicode__(self):
        return self.user.username

class Post(models.Model):
    text = models.CharField(max_length = 42)
    image = models.ImageField()
    time = models.DateTimeField()
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.text
