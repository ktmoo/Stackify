from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from .models import CustomUser

class UserForm(forms.Form):
    name=forms.CharField(label='Name',max_length=30,required=True, 
                     widget=forms.TextInput(attrs={'class': 'form-control'}))

    username=forms.CharField(label='Username',max_length=30, required=True,
                         widget=forms.TextInput(attrs={'class': 'form-control'}))

    email=forms.EmailField(label='Email',required=True,
                       widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password=forms.CharField(label='Password',max_length=20, required=True,  
                         widget=PasswordInput(attrs={'class': 'form-control'}))

    cpassword=forms.CharField(label='Confirm Password',max_length=20, required=True,
                          widget=PasswordInput(attrs={'class': 'form-control'}))

    bio=forms.CharField(label='Bio',max_length=250,
                    widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data=self.cleaned_data
        password=cleaned_data['password']
        username=self.cleaned_data['username']
        cpassword=cleaned_data['cpassword']
        if cpassword!=password:
            raise ValidationError("Passwords dont match!")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username already exsists!")
        return cleaned_data
            
        
    

class SignInForm(forms.Form):
    username=forms.CharField(label='Username',max_length=30, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password=forms.CharField(label='Password',max_length=20, required=True,widget=PasswordInput(attrs={'class': 'form-control'}))