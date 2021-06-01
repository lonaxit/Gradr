from django.urls import path
from . import views


urlpatterns = [
  path('setting', views.createClient, name='admin-setting'),
  path('update-profile/<str:pk>', views.updateClient, name='update-profile'),
  path('add-term', views.addTerm, name='create-term'),
  path('update-term/<str:pk>', views.editTerm, name='update-term'),
  path('profile', views.profile, name='admin-profile'),
  path('session', views.addSession, name='add-session'),
  path('all-sessions', views.allSessions, name='all-sessions'),
  path('update-session/<str:pk>', views.updateSession, name='update-session'),
  path('class', views.addClass, name='add-class'),
  path('update-class/<str:pk>', views.updateClass, name='update-class'),
  path('all-classes', views.allClasses, name='all-classes'),
  path('subject', views.addSubject, name='add-subject'),
  path('update-subject/<str:pk>', views.updateSubject, name='update-subject'),
  path('all-subjects', views.allSubjects, name='all-subjects'),
  path('attendance-setting', views.attendance_settings, name='attendance-setting'),
  path('resumption-setting', views.resumption_settings, name='resumption-setting'),
  path('resumption-dates', views.resumptionDates, name='resumption-dates'),
  path('update-resumption/<str:pk>', views.updateResumption, name='update-resumption'),

  # path('student/<str:pk>/', views.student, name='student'),

]
