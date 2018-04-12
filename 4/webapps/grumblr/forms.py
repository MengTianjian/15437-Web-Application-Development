from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from grumblr.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address', 'type': 'email'}))
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'type': 'password'}))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if User.objects.filter(username=username).first() != None:
            raise forms.ValidationError('User already exists.')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'type': 'password'}))

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password1

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = User.objects.filter(username=username).first()
        if user == None:
            raise forms.ValidationError('User does not exist.')
        if not user.check_password(password):
            raise forms.ValidationError('Username and password do not match.')
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #exclude = ('user', 'time', 'image',)
        fields = ['text', 'image']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What\'s happening?'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'followed']
        widgets = {
            'profilephoto': forms.FileInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short bio (420 characters or less)'})
        }
