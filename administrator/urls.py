from django.urls import path
from . import views


urlpatterns = [
  path('setting', views.createClient, name='admin-setting'),
  path('add-term', views.addTerm, name='create-term'),
  path('profile', views.profile, name='admin-profile'),
  path('session', views.addSession, name='add-session'),
  path('class', views.addClass, name='add-class'),
  path('subject', views.addSubject, name='add-subject'),
]
