from django.urls import path
from . import views


urlpatterns = [
  path('register', views.register, name='register'),
  path('login', views.loginPage, name='login'),
  path('logout', views.logoutUser, name='logout'),



  path('contact', views.contact, name='contact'),
  path('profile', views.profile, name='profile'),
  path('staff', views.staff),
  path('student', views.profile),
  path('student-list', views.studentList),
  path('admin-home', views.admin, name='admin'),
  path('users', views.users, name='users'),
]
