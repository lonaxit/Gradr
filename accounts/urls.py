from django.urls import path
from . import views


urlpatterns = [
  path('accounts/register', views.register, name='register'),
  path('accounts/login', views.loginPage, name='login'),
  path('accounts/logout', views.logoutUser, name='logout'),
  path('accounts/contact', views.contact, name='contact'),

  path('accounts/profile', views.profile, name='profile'),
  path('accounts/staff', views.staff),
  path('accounts/student', views.profile),
  path('accounts/student-list', views.studentList),
  path('admin-home', views.admin, name='admin'),
  path('users', views.users, name='users'),
]
