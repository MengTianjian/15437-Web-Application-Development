# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr.models import *
from datetime import datetime

# Create your views here.
@login_required
def home(request):
    context={}
    context['posts'] = Post.objects.all().order_by('-time')
    return render(request, 'GlobalStream.html', context)

@login_required
def post(request):
    context = {}
    errors = []
    context['errors'] = errors
    if request.method == 'GET':
        return render(request, 'GlobalStream.html', context)
    if not 'text' in request.POST or not request.POST['text']:
        errors.append('You must enter some text to post.')
    elif len(request.POST['text']) > 42:
        errors.append('You port must be no more than 42 characters.')
    else:
        new_post = Post(text=request.POST['text'], time=datetime.now(), user=request.user)
        new_post.save()
    #context['posts'] = Post.objects.all().order_by('-time')
    #return render(request, 'GlobalStream.html', context)
    if errors:
        return render(request, 'GlobalStream.html', context)
    return redirect('/')

@login_required
def profile(request):
    context = {}
    errors = []
    context['errors'] = errors
    if request.method == 'POST':
        return render(request, 'Profile.html', context)
    if request.GET.get('username'):
        user = User.objects.filter(username=request.GET.get('username')).first()
    else:
        user = request.user
    if user == None:
        errors.append("User does not exist.")
        context['posts'] = Post.objects.all().order_by('-time')
        return render(request, 'GlobalStream.html', context)
    context['posts'] = Post.objects.filter(user=user).order_by('-time')
    context['userprofile'] = user.userprofile
    return render(request, 'Profile.html', context)

def register(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'Registration.html', context)

    errors = []
    context['errors'] = errors

    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST and request.POST['password1'] and request.POST['password2'] and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if not 'firstname' in request.POST or not request.POST['firstname']:
        errors.append('First name is required.')
    if not 'lastname' in request.POST or not request.POST['lastname']:
        errors.append('Last name is required.')
    if not 'email' in request.POST or not request.POST['email']:
        errors.append('Email address is required.')

    if errors:
        return render(request, 'Registration.html', context)

    new_user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])
    new_user.save()
    new_user_profile = UserProfile(user=new_user, firstname=request.POST['firstname'], lastname=request.POST['lastname'], email=request.POST['email'])
    new_user_profile.save()
    new_user = authenticate(username = request.POST['username'], password = request.POST['password1'])
    login(request, new_user)
    return redirect('/')

def my_login(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'Login.html', context)
    errors = []
    context['errors'] = errors
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    elif User.objects.filter(username=request.POST['username']).first() == None:
        errors.append('Username does not exist.')
        return render(request, 'Login.html', context)
    if not 'password' in request.POST or not request.POST['password']:
        errors.append('Password is required.')
    user = authenticate(username = request.POST['username'], password = request.POST['password'])
    if user == None:
        errors.append('Username and password do not match.')
        return render(request, 'Login.html', context)
    else:
        login(request, user)
        return redirect('/')
