from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/signup', views.signup,name="signup" ),
    path('user/signin', views.signin,name="signin" ),
    path('', views.about_page,name="about_page" ),
    path('home', views.home_page,name="home_page" ),
    path('user/profile/<str:username>', views.profile_page,name="profile_page" ),
    path('user/profile/follow/<str:account>', views.follow,name="follow" ),
    path('user/profile/unfollow/<str:account>', views.unfollow,name="unfollow" ),
    path('logout',views.logout_view,name="logout" ),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
