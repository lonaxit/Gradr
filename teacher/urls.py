from django.urls import path
from . import views


urlpatterns = [
  path('teacher-home', views.teacherHome, name='teacher'),
  path('new-scores', views.addScores, name='new-scores'),
  path('my-subjects', views.mySubjects, name='my-subjects'),
    # path('country-json', views.get_json_country_data, name='country-json'),
  path('class-subjects/<str:pk>', views.get_subjects, name='class-subjects'),
  path('filter-scores', views.scoresFilter, name='filter-scores'),
  path('update-scores/<int:id>', views.editScores, name='update-scores'),
  path('remove-scores/<int:id>', views.deleteScores, name='delete-scores'),
  path('filter-result', views.resultFilter, name='filter-result'),
  path('add-attendance', views.addAttendance, name='add-attendance'),
  path('add-student-affective/<str:pk>', views.addStudentAffective, name='add-student-affective'),
  path('add-student-psycho/<str:pk>', views.addStudentPsycho, name='add-student-psycho'),
  path('back-to-result/<str:classroom>/<str:term>/<str:session>', views.resultComments, name='back-to-result'),
  path('result-summary', views.resultSummary, name='result-summary'),
  path('submit-result/<str:classroom>/<str:term>/<str:session>', views.submitResult, name='submit-result'),
  # path('lg-json/<str:pk>', views.get_json_lg_data, name='lg-json'),
  # path('update-profile/<str:pk>', views.updateClient, name='update-profile'),

]
