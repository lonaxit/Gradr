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
  path('enroll', views.enrollStudent, name='enroll'),
  path('delete-enrollment/<str:pk>', views.deleteEnrollment, name='delete-enrollment'),
  path('classroom', views.myClassroom, name='classroom'),
  path('assessment-sheet', views.assessmentSheet, name='assessment-sheet'),
  path('export-sheet/<str:classroom>/<str:subject>', views.exportSheet, name='export-sheet'),
  path('import-assessment-sheet', views.importAssessmentSheet, name='import-assessment-sheet'),
  
  


  path('result-summary', views.resultSummary, name='result-summary'),
  path('annual-result', views.annualResultSummary, name='annual-result'),
  path('annual-result-detail', views.annualResultDetail, name='annual-result-detail'),
  
  path('submit-result/<str:classroom>/<str:term>/<str:session>', views.submitResult, name='submit-result'),
  # path('lg-json/<str:pk>', views.get_json_lg_data, name='lg-json'),
  # path('update-profile/<str:pk>', views.updateClient, name='update-profile'),

  path('result-pdf', views.render_pdf_view, name='result-pdf'),
  path('print-result/<str:pk>/', views.printResultHtml, name='print-result'),

  path('teacher-profile', views.teacherProfile, name='teacher-profile'),
  path('teacher-avatar', views.teacherAvatar, name='teacher-avatar'),

]
