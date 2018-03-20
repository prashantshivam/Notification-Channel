from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^read-notification/' , views.read_notification , name ='read_notification'),
    url(r'^add-vehicle/' , views.add_vehicle , name ='add_vehicle'),
    url(r'^login1/' , views.login1 , name ='login'),
    url(r'^register/' , views.register, name ='register'),
    url(r'^$', views.index, name='index'),
    
]
