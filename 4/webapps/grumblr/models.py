# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profilephoto = models.ImageField(default="profile-photos/images.png", upload_to="profile-photos", blank=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField()
    age = models.PositiveIntegerField(default=0)
    bio = models.CharField(default="", max_length=420)
    followed = models.ManyToManyField(User,related_name='followed')
    def __unicode__(self):
        return self.user.username

class Post(models.Model):
    text = models.CharField(max_length=42)
    image = models.ImageField(upload_to="post-photos", blank=True)
    time = models.DateTimeField()
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.text
