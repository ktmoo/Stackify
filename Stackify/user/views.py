from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login,logout
from .models import CustomUser
from django.contrib.auth.hashers import make_password, check_password
from .forms import UserForm,SignInForm
from django.contrib import messages
from friends.models import FriendList,FriendRequest



def about_page(request):
    return render(request, 'user/about.html')

def signup(request):
    form=UserForm(request.POST or None)
    context={"form":form,"url":reverse('signup')}
    if form.is_valid():
        username=form.cleaned_data.get("username")
        email=form.cleaned_data.get('email')
        pswd=form.cleaned_data.get('password')
        user=CustomUser.objects.create(username=username,email=email,password=make_password(pswd))
        return redirect('signin')
    return render(request,"user\signup.html",context)


def signin(request):
    form=SignInForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        pswd=form.cleaned_data.get("password")
        user = CustomUser.objects.filter(username=username).first()
        if user:
            if check_password(pswd, user.password):
                login(request,user)
                form=SignInForm(None)
                return redirect('home_page')
            else:
                messages.error(request,'Password is not correct')
                return redirect('signin')
        else:
            messages.error(request,'Username not found, please signup first!')
            return redirect('signin')
        
    return render(request,"user\signin.html",{"url":reverse('signin'),"form":form})


def home_page(request):
    user=request.user
    return render(request,"user\home.html",context={"user":user})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')


def profile_page(request,username):
    user=CustomUser.objects.get(username=username)
    # friends=Friend.objects.filter(username=username).first()
    return render(request,"user\profile.html",context={"user":user})

def add_friend(request,username):
    reciever=CustomUser.objects.filter(username=username).first()
    friend_request=FriendRequest.objects.create(sender=request.user,reciever=reciever)
    return render(request,"user\profile.html")