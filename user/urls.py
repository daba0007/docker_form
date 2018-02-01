from django.conf.urls import url
from django.contrib import admin
from user import views as user_views

urlpatterns = [
    url(r'^login$', user_views.login, name='login'),
    url(r'^register$', user_views.register,name='register'),
    url(r'^check_code$', user_views.check_code,name='check_code'),
    url(r'^logout$', user_views.logout,name='logout'),
]
