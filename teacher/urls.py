from django.urls import path
from . import views


urlpatterns = [
  path('teacher-home', views.teacherHome, name='teacher'),
  path('new-scores', views.addScores, name='new-scores'),
    # path('country-json', views.get_json_country_data, name='country-json'),
  path('class-subjects/<str:pk>', views.get_subjects, name='class-subjects'),
  path('filter-scores', views.scoresFilter, name='filter-scores'),
  path('update-scores/<str:pk>', views.editScores, name='update-scores'),
  # path('lg-json/<str:pk>', views.get_json_lg_data, name='lg-json'),
  # path('update-profile/<str:pk>', views.updateClient, name='update-profile'),

]
