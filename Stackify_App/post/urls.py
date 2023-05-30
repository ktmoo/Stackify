from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post/create_a_post', views.create_a_post,name="create_a_post" ),
    path('post/posts', views.posts,name="posts" ),
    path('post/deletepost/<str:slug>', views.deletepost,name="deletepost" ),
    path('post/posts/<str:slug>', views.post,name="post" ),
    path('post/upvote/<str:slug>', views.upvote,name="upvote" ),
    path('post/search',views.search_view,name="search")
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
