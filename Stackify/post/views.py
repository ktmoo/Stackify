from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseBadRequest,Http404
from django.contrib.auth.decorators import login_required
from user.models import CustomUser
from django.db.models import Q
from .forms import PostForm,CommentsForm
from .models import Post,Comments




def search_view(request):
    if request.method=='POST':
        query=request.POST.get('query') 
        if query is None or query == "":
            context=None
        else:
            lookups=Q(title__icontains=query) | Q(content__icontains=query) | Q(author_id__username__icontains=query) | Q(tags__icontains=query)
            post_list = Post.objects.filter(lookups)
            context = { "post_list":post_list}
        return render(request, "post/searchview.html", context=context)

@login_required
def create_a_post(request):
    form=PostForm(request.POST or None)
    url=reverse('create_a_post')
    if form.is_valid():
        post=form.save(commit=False)
        post.author_id=request.user
        post.save()
        form=PostForm(None)
        return redirect('posts')
    context={"form": form, "url": url}
    return render(request,'post/create_post.html',context)

def posts(request):
    posts=Post.objects.all()
    return render(request,'post/posts.html',{"posts": posts})

def post(request, slug):
    try:
        post_display=Post.objects.get(slug=slug)
        comments=Comments.objects.filter(post=post_display)
        form=CommentsForm(request.POST or None)
        url=reverse('post',kwargs={'slug':slug})
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author_id=request.user
            comment.post=post_display
            comment.save()
            form=CommentsForm(None)
            return HttpResponseRedirect(reverse('post',kwargs={"slug":post_display.slug}))
    except Post.DoesNotExist:
        return render(request, 'user/404.html')
    except :
        return render(request,'user/404.html')
    
    return render(request,'post/post.html',{"post": post_display,"form": form,"url":url,"comments":comments,"current_user":request.user})


def deletepost(request,slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    return HttpResponseRedirect(reverse('posts'))


def upvote(request,slug):
    post = Post.objects.get(slug=slug)
    post.upvotes=post.upvotes+1
    post.save()
    return HttpResponseRedirect(reverse('post',kwargs={"slug":post.slug}))