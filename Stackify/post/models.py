from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
import random

class Post(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(max_length=50,blank=True,null=True)
    content=models.TextField()
    tags=models.CharField(max_length=30)
    author_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(auto_now_add=True)
    upvotes=models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def excerpt(self):
       return self.content[:100] + '...'
    
    def save(self,*args,**kwargs):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        self.slug=unique_slug[:50]
        super().save(*args,**kwargs)

    def get_absolute_url(self):
       return f'/post/posts/{self.slug}'
    

class Comments(models.Model):
    content=models.CharField(max_length=100)
    author_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(auto_now_add=True)
