from django.urls import path
from . import views

urlpatterns = [
    path('group/create_a_group', views.create_a_groupt,name="create_a_group" ),
    path('group/groups', views.groups,name="groups" ),
]