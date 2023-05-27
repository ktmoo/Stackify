from django.urls import path
from . import views

urlpatterns = [
    path('user/signup', views.signup,name="signup" ),
    path('user/signin', views.signin,name="signin" ),
    path('', views.about_page,name="about_page" ),
    path('home', views.home_page,name="home_page" ),
    path('user/profile/<str:username>', views.profile_page,name="profile_page" ),
    path('logout',views.logout_view,name="logout" ),
]
