# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr.models import *
from grumblr.forms import *
from datetime import datetime
from mimetypes import guess_type
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
@login_required
def home(request):
    context = {}
    context['form'] = PostForm()
    context['followed'] = request.user.userprofile.followed.all()
    context['posts'] = Post.objects.all().order_by('-time')
    return render(request, 'GlobalStream.html', context)

@login_required
def followerstream(request):
    context = {}
    context['form'] = PostForm()
    followed = request.user.userprofile.followed.all()
    context['posts'] = Post.objects.filter(user__in=followed).order_by('-time')
    return render(request, 'FollowerStream.html', context)

@login_required
def post(request):
    context = {}
    if request.method == 'GET':
        return redirect(reverse('home'))
    new_post = Post(user=request.user, time=datetime.now())
    form = PostForm(request.POST, request.FILES, instance=new_post)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'GlobalStream.html', context)
    form.save()
    return redirect(reverse('home'))

@login_required
def profile(request, id):
    context = {}
    if request.method == 'POST':
        return redirect(reverse('home'))
    user = get_object_or_404(User, id=id)
    context['posts'] = Post.objects.filter(user=user).order_by('-time')
    context['userprofile'] = user.userprofile
    return render(request, 'Profile.html', context)

@login_required
def edit_profile(request):
    context = {}
    context['userprofile'] = request.user.userprofile
    if request.method == 'GET':
        context['form'] = EditProfileForm(instance=request.user.userprofile)
        return render(request, 'EditProfile.html', context)
    form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'EditProfile.html', context)
    context['posts'] = Post.objects.filter(user=request.user).order_by('-time')
    form.save()
    return redirect(reverse('profile', kwargs={'id':request.user.id}))#render(request, 'Profile.html', context)

@login_required
def get_profilephoto(request, id):
    user = get_object_or_404(User, id=id)
    userprofile = user.userprofile
    if not userprofile.profilephoto:
        raise Http404
    content_type = guess_type(userprofile.profilephoto.name)
    return HttpResponse(userprofile.profilephoto, content_type=content_type)

@login_required
def get_postphoto(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.image:
        raise Http404
    content_type = guess_type(post.image.name)
    return HttpResponse(post.image, content_type=content_type)

@login_required
def follow(request):
    context = {}
    if request.method == 'GET':
        return redirect(reverse('home'))
    if not 'id' in request.POST or not request.POST['id']:
        return redirect(reverse('home'))
    followed = get_object_or_404(User, id=request.POST['id'])
    userprofile = request.user.userprofile
    userprofile.followed.add(followed)
    return redirect(reverse('home'))

@login_required
def unfollow(request):
    context = {}
    if request.method == 'GET':
        return redirect(reverse('home'))
    if not 'id' in request.POST or not request.POST['id']:
        return redirect(reverse('home'))
    followed = get_object_or_404(User, id=request.POST['id'])
    userprofile = request.user.userprofile
    userprofile.followed.remove(followed)
    return redirect(reverse('home'))

@login_required
def change_password(request):
    context = {}
    token = default_token_generator.make_token(request.user)
    email_body = """
    Welcome to Grumblr. Please click the link below to reset your password:
    http://%s%s
    """ % (request.get_host(), reverse('confirm_password', kwargs={'id':request.user.id, 'token':token}))
    send_mail(subject="Reset your password", message=email_body, from_email="admin@grumblr.com", recipient_list=[request.user.userprofile.email])
    context['text'] = 'Please reset your password in your email!'
    return render(request, 'NeedConfirmation.html', context)

def confirm_password(request, id, token):
    context = {}
    user = User.objects.filter(id=id).first()
    if user != None and default_token_generator.check_token(user, token):
        context['userprofile'] = request.user.userprofile
        context['form'] = PasswordChangeForm()
        return render(request, 'ChangePassword.html', context)

def update_password(request):
    context = {}
    context['userprofile'] = request.user.userprofile
    if request.method == 'GET':
        context['form'] = PasswordChangeForm()
        return render(request, 'ChangePassword.html', context)
    form = PasswordChangeForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'ChangePassword.html', context)
    user = request.user
    user.set_password(form.cleaned_data)
    user.save()
    return redirect(reverse('profile', kwargs={'id':request.user.id}))

def register(request):
    context = {}
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'Registration.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'Registration.html', context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
    new_user.is_active = False
    new_user.save()
    new_user_profile = UserProfile(user=new_user, firstname=form.cleaned_data['firstname'], lastname=form.cleaned_data['lastname'], email=form.cleaned_data['email'])
    new_user_profile.save()
    #new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])

    token = default_token_generator.make_token(new_user)
    email_body = """
    Welcome to Grumblr. Please click the link below to verify your email address and complete the registration of your account:
    http://%s%s
    """ % (request.get_host(), reverse('confirm', kwargs={'id':new_user.id, 'token':token}))
    send_mail(subject="Verify your email address", message=email_body, from_email="admin@grumblr.com", recipient_list=[new_user_profile.email])
    context['text'] = 'Please confirm your registration in your email!'
    return render(request, 'NeedConfirmation.html', context)
    #login(request, new_user)
    #return redirect(reverse('home'))

def my_login(request):
    context = {}
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'Login.html', context)
    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'Login.html', context)
    user = form.cleaned_data
    if not user.is_active:
        return render(request, 'NeedConfirmation.html', context)
    login(request, user)
    return redirect(reverse('home'))

def confirm_registration(request, id, token):
    user = User.objects.filter(id=id).first()
    if user != None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(reverse('home'))
    else:
        return render(request, 'NeedConfirmation.html', context)
