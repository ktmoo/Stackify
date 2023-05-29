from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.hashers import make_password, check_password
from .forms import UserForm,SignInForm
from django.contrib import messages
from Followers.models import FollowList
from post.models import Post
from django.db import IntegrityError



def about_page(request):
    return render(request, 'user/about.html')

def signup(request):
    if request.method == 'POST':
        form=UserForm(request.POST,request.FILES)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get('email')
            pswd=form.cleaned_data.get('password')
            image=form.cleaned_data.get('image')
            bio=form.cleaned_data.get('bio')
            user=CustomUser.objects.create(username=username,email=email,password=make_password(pswd),image=image,bio=bio)
            return redirect('signin')
    else:
        form = UserForm(None)
    context={"form":form,"url":reverse('signup')}
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
    latest_post = Post.objects.order_by('-date')[:3]
    most_upvotes=Post.objects.order_by('-upvotes')[:3]
    return render(request,"user\home.html",context={"user":user,"most_upvotes":most_upvotes,"latest_post":latest_post})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')

@login_required
def profile_page(request,username):
    if username==request.user.username:
        print(request.user)
        user=request.user
    else:
        print(username)
        print(request.user)
        user=CustomUser.objects.get(username=username)
    return render(request,"user\profile.html",context={"user":user})

def follow(request,account):
    try:
        acc=CustomUser.objects.get(username=account)
        if not acc in FollowList.objects.all():
                user_follow=FollowList.objects.create(user=acc)
                user_follow.friends.add(acc)
                user_follow.save()
        user=CustomUser.objects.get(username=acc.username)
        user.num_followers=(user.num_followers)+1
        user.save()
        messages.success(request,f"You are following {account}" )
    except IntegrityError:
        messages.error(request,f"You are already following {account} !" )
    return redirect(reverse('profile_page',kwargs={"username":account}))
 
def unfollow(request,account):
    account=CustomUser.objects.get(username=account)
    FollowList.unfollow(account)
    user=CustomUser.objects.get(username=request.user.username)
    user.num_followers-=1
    user.save()
