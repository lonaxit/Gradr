from django.urls import path
from . import views


urlpatterns = [
  path('home', views.home, name='home'),
  path('client-setting', views.loginPage, name='setting'),
  path('profile', views.logoutUser, name='profile'),
 
]